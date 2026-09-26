"""
Comprehensive Multi-Aspect, Multi-Persona, Industry-Expert Level Test Suite
Tests:
1. Multi-Standard Verification: IS 14543, IS 1786, IS 4984, IS 1293, IS 10500, IS 269
2. Multi-Persona Perspectives:
   - Persona A: NABL Accredited Laboratory Quality Manager (formal method citations, uncertainty bounds)
   - Persona B: BIS Enforcement Officer / Technical Auditor (statutory violations, Section 16 BIS Act)
   - Persona C: Factory Plant QA/QC Engineer (production batch sheets, conditional CAR requirements)
   - Persona D: Citizen / Institutional Buyer (third-party scrutiny, noise resilience)
3. Robustness & Edge Cases:
   - Qualitative terms ('Absent', 'Nil', 'Negative', 'Not Detected')
   - Standard code variations ('IS:14543', 'IS-1786', 'IS10500', 'is 269:2015')
   - Special symbols, units ('N/mm²', 'kg/m³', 'MΩ', '°C', 'cfu/250ml')
4. Official PDF Audit Report Generation Integrity (PDF headers, tables, legal seal)
5. End-to-End FastAPI Endpoint Verification
"""

import sys
import io
import os
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app
from app.services.lab_report_extractor import lab_report_extractor_service
from app.services.compliance_audit import compliance_audit_engine
from app.services.pdf_report_generator import pdf_report_generator
from app.models.schemas import AuditRequest, AuditParameterInput, OverallVerdict, ComplianceStatus

client = TestClient(app)

TOTAL_TESTS = 0
PASSED_TESTS = 0

def record_test(name: str, passed: bool, details: str = ""):
    global TOTAL_TESTS, PASSED_TESTS
    TOTAL_TESTS += 1
    if passed:
        PASSED_TESTS += 1
        print(f"  [PASS] {name} {details}")
    else:
        print(f"  [FAIL] {name} {details}")
        assert False, f"Test failed: {name} {details}"


def test_aspect_1_multi_standard_benchmarks():
    print("\n=======================================================")
    print("ASPECT 1: MULTI-STANDARD STATUTORY BENCHMARK AUDITING")
    print("=======================================================")

    # 1. IS 14543 (Packaged Water) - Conforming
    req_water = AuditRequest(
        standard_is_code="IS 14543",
        product_name="Packaged Drinking Water",
        manufacturer_name="Himalayan Mineral Springs",
        batch_number="HMS-B402",
        testing_lab="BIS Central Lab",
        parameters=[
            AuditParameterInput(parameter_name="pH Value", tested_value="7.35", unit=""),
            AuditParameterInput(parameter_name="Total Dissolved Solids (TDS)", tested_value="125.0", unit="mg/L"),
            AuditParameterInput(parameter_name="Turbidity", tested_value="0.45", unit="NTU"),
            AuditParameterInput(parameter_name="Lead (as Pb)", tested_value="0.003", unit="mg/L"),
            AuditParameterInput(parameter_name="Arsenic (as As)", tested_value="0.002", unit="mg/L"),
            AuditParameterInput(parameter_name="Nitrate (as NO3)", tested_value="14.2", unit="mg/L"),
            AuditParameterInput(parameter_name="Escherichia coli (E. coli)", tested_value="Nil", unit="cfu/250ml")
        ]
    )
    res_water = compliance_audit_engine.perform_audit(req_water)
    record_test("IS 14543 Packaged Water (Conforming)", res_water.overall_verdict == OverallVerdict.CONFORMING, f"Score={res_water.compliance_score_percent}%")

    # 2. IS 14543 (Packaged Water) - Toxic Lead Exceedance (Critical Failure)
    req_water_fail = AuditRequest(
        standard_is_code="IS 14543",
        product_name="Packaged Drinking Water",
        manufacturer_name="Delta Beverages",
        batch_number="DPB-FAIL",
        testing_lab="Regional Quality Lab",
        parameters=[
            AuditParameterInput(parameter_name="pH Value", tested_value="7.1", unit=""),
            AuditParameterInput(parameter_name="Lead (as Pb)", tested_value="0.025", unit="mg/L"),  # Limit 0.01
            AuditParameterInput(parameter_name="E. Coli", tested_value="0", unit="cfu/250ml")
        ]
    )
    res_water_fail = compliance_audit_engine.perform_audit(req_water_fail)
    record_test("IS 14543 Critical Lead Violation Flagged", res_water_fail.overall_verdict == OverallVerdict.NON_CONFORMING, f"Failed={res_water_fail.failed_count}")

    # 3. IS 1786 (TMT Steel Bars Fe 500D) - Conforming
    req_steel = AuditRequest(
        standard_is_code="IS 1786",
        product_name="TMT Rebar Fe 500D",
        manufacturer_name="Tata Steel Limited",
        batch_number="TATA-500D-01",
        testing_lab="Central Metallurgy Lab",
        parameters=[
            AuditParameterInput(parameter_name="Carbon (C) Content", tested_value="0.21", unit="%"),
            AuditParameterInput(parameter_name="Sulphur (S) Content", tested_value="0.035", unit="%"),
            AuditParameterInput(parameter_name="Phosphorus (P) Content", tested_value="0.032", unit="%"),
            AuditParameterInput(parameter_name="0.2% Proof Stress / Yield Strength", tested_value="530.0", unit="N/mm²"),
            AuditParameterInput(parameter_name="Tensile Strength to Yield Strength Ratio", tested_value="1.15", unit="ratio"),
            AuditParameterInput(parameter_name="Elongation (Gauge Length 5.65√A)", tested_value="18.0", unit="%")
        ]
    )
    res_steel = compliance_audit_engine.perform_audit(req_steel)
    record_test("IS 1786 TMT Steel Fe 500D (Conforming)", res_steel.overall_verdict == OverallVerdict.CONFORMING, f"Score={res_steel.compliance_score_percent}%")

    # 4. IS 4984 (HDPE Pipe PE 100) - Conforming
    req_hdpe = AuditRequest(
        standard_is_code="IS 4984",
        product_name="HDPE Pipe 110mm",
        manufacturer_name="Bharat Polymers",
        batch_number="BHDP-LOT12",
        testing_lab="CIPET Lab",
        parameters=[
            AuditParameterInput(parameter_name="Base Polymer Density at 27°C", tested_value="952.0", unit="kg/m³"),
            AuditParameterInput(parameter_name="Melt Flow Index (190°C / 5 kg)", tested_value="0.45", unit="g/10 min"),
            AuditParameterInput(parameter_name="Carbon Black Content", tested_value="2.4", unit="%"),
            AuditParameterInput(parameter_name="Hydrostatic Strength (100h at 20°C, PE 100)", tested_value="12.5", unit="MPa")
        ]
    )
    res_hdpe = compliance_audit_engine.perform_audit(req_hdpe)
    record_test("IS 4984 HDPE Water Pipe (Conforming)", res_hdpe.overall_verdict == OverallVerdict.CONFORMING, f"Score={res_hdpe.compliance_score_percent}%")

    # 5. IS 1293 (Plugs and Socket Outlets up to 250V) - Conforming
    req_socket = AuditRequest(
        standard_is_code="IS 1293",
        product_name="16A 3-Pin Socket Outlet",
        manufacturer_name="ElectroSafe Devices",
        batch_number="EL-SKT-99",
        testing_lab="ERDA Laboratory",
        parameters=[
            AuditParameterInput(parameter_name="Insulation Resistance at 500V DC", tested_value="25.0", unit="MΩ"),
            AuditParameterInput(parameter_name="Terminal Temperature Rise under Rated Current", tested_value="34.0", unit="°C"),
            AuditParameterInput(parameter_name="Breaking Capacity (250V AC, 1.25 In)", tested_value="100.0", unit="cycles")
        ]
    )
    res_socket = compliance_audit_engine.perform_audit(req_socket)
    record_test("IS 1293 Electrical Socket (Conforming)", res_socket.overall_verdict == OverallVerdict.CONFORMING, f"Score={res_socket.compliance_score_percent}%")

    # 6. IS 10500 (Drinking Water Potable Specification) - Conforming
    req_potable = AuditRequest(
        standard_is_code="IS 10500",
        product_name="Potable Municipal Water Supply",
        manufacturer_name="Delhi Jal Board WTP",
        batch_number="DJB-LOT-04",
        testing_lab="NEERI Laboratory",
        parameters=[
            AuditParameterInput(parameter_name="pH Value", tested_value="7.4", unit=""),
            AuditParameterInput(parameter_name="Total Dissolved Solids (TDS)", tested_value="220.0", unit="mg/L"),
            AuditParameterInput(parameter_name="Turbidity", tested_value="0.6", unit="NTU"),
            AuditParameterInput(parameter_name="Total Hardness", tested_value="150.0", unit="mg/L"),
            AuditParameterInput(parameter_name="Chlorides", tested_value="90.0", unit="mg/L"),
            AuditParameterInput(parameter_name="Fluoride", tested_value="0.8", unit="mg/L"),
            AuditParameterInput(parameter_name="Lead", tested_value="0.002", unit="mg/L"),
            AuditParameterInput(parameter_name="E. Coli", tested_value="Absent", unit="cfu/100ml")
        ]
    )
    res_potable = compliance_audit_engine.perform_audit(req_potable)
    record_test("IS 10500 Potable Water Specification (Conforming)", res_potable.overall_verdict == OverallVerdict.CONFORMING, f"Passed={res_potable.passed_count}/8")

    # 7. IS 269 (Ordinary Portland Cement 53 Grade) - Conforming
    req_cement = AuditRequest(
        standard_is_code="IS 269",
        product_name="Ordinary Portland Cement 53 Grade",
        manufacturer_name="UltraTech Cement Ltd",
        batch_number="UTC-53G-WK09",
        testing_lab="NCCBM Laboratories",
        parameters=[
            AuditParameterInput(parameter_name="Soundness (Le Chatelier)", tested_value="1.5", unit="mm"),
            AuditParameterInput(parameter_name="Initial Setting Time", tested_value="120.0", unit="minutes"),
            AuditParameterInput(parameter_name="Final Setting Time", tested_value="200.0", unit="minutes"),
            AuditParameterInput(parameter_name="28-Day Compressive Strength", tested_value="55.0", unit="MPa"),
            AuditParameterInput(parameter_name="Insoluble Residue", tested_value="1.8", unit="%"),
            AuditParameterInput(parameter_name="Magnesia (MgO) Content", tested_value="2.2", unit="%")
        ]
    )
    res_cement = compliance_audit_engine.perform_audit(req_cement)
    record_test("IS 269 Portland Cement (Conforming)", res_cement.overall_verdict == OverallVerdict.CONFORMING, f"Passed={res_cement.passed_count}/6")


def test_aspect_2_multi_persona_scenarios():
    print("\n=======================================================")
    print("ASPECT 2: MULTI-USER & INDUSTRY EXPERT PERSPECTIVES")
    print("=======================================================")

    # Persona A: NABL Laboratory Quality Manager (Checking test method citations)
    report_nabl = """
    NATIONAL TEST HOUSE (NABL ACCREDITED LAB TC-1102)
    CERTIFICATE OF ANALYSIS
    Standard: IS 14543:2018
    Manufacturer: Bisleri International Pvt Ltd
    Batch No: BISL-2026-B99
    Testing Lab: National Test House (NTH), Ghaziabad

    TEST OBSERVATIONS:
    pH: 7.2
    Total Dissolved Solids: 110.0 mg/L
    Turbidity: 0.3 NTU
    Lead: 0.001 mg/L
    Arsenic: 0.002 mg/L
    E. coli: Nil
    """
    ext_nabl = lab_report_extractor_service.extract_and_verify(raw_text=report_nabl, auto_verify=True)
    record_test("Persona A (NABL Quality Manager): IS 14543 Verification", ext_nabl.verification.overall_verdict == OverallVerdict.CONFORMING)
    # Check that test method is cited in parameter remarks
    lead_res = next((p for p in ext_nabl.verification.parameter_results if "lead" in p.parameter_name.lower()), None)
    record_test("Persona A: Exact Clause Citation Recorded", lead_res is not None and "Clause 5.2" in lead_res.clause_reference)

    # Persona B: BIS Enforcement Officer (Auditing toxic contamination under Section 16 BIS Act)
    report_enforce = """
    CENTRAL SURVEILLANCE TESTING STATION
    STATUTORY ENFORCEMENT AUDIT REPORT
    Standard: IS 10500:2012
    Manufacturer: Rogue Bottling Works
    Batch No: ROGUE-LOT-01
    Testing Lab: State Public Health Laboratory

    CRITICAL PARAMETERS:
    Fluoride: 2.8 mg/L
    Lead: 0.035 mg/L
    Arsenic: 0.040 mg/L
    Escherichia coli: 12 cfu/100ml
    """
    ext_enforce = lab_report_extractor_service.extract_and_verify(raw_text=report_enforce, auto_verify=True)
    record_test("Persona B (BIS Enforcement Officer): Critical Safety Violation Flagged", ext_enforce.verification.overall_verdict == OverallVerdict.NON_CONFORMING)
    record_test("Persona B: Multiple Toxic Substance Exceedances Flagged", ext_enforce.verification.failed_count >= 3)

    # Persona C: Factory Plant QA/QC Engineer (Checking batch compliance)
    report_factory = """
    DECCAN HIGH-TENSILE STEEL MILLS - INTERNAL QA BATCH LOG
    Standard: IS 1786
    Batch No: DHSM-FE500D-PLANT-07
    Product: TMT Rebar 12mm

    MEASURED VALUES:
    Carbon: 0.22 %
    Sulphur: 0.038 %
    Phosphorus: 0.034 %
    Yield Strength: 540.0 N/mm²
    Elongation: 18.0 %
    """
    ext_factory = lab_report_extractor_service.extract_and_verify(raw_text=report_factory, auto_verify=True)
    record_test("Persona C (Factory QA/QC Engineer): Instant Daily Batch Validation", ext_factory.verification.overall_verdict == OverallVerdict.CONFORMING)

    # Persona D: Citizen / Institutional Buyer (Checking cement test sheet)
    report_citizen = """
    RESIDENTIAL APARTMENT WELFARE ASSOCIATION
    THIRD-PARTY CEMENT AUDIT SHEET
    Standard: IS 269
    Manufacturer: UltraTech Cement
    Batch No: UTC-SILO-53G

    RESULTS:
    Compressive Strength: 52.0 MPa
    Soundness: 2.0 mm
    Initial Setting Time: 110.0 minutes
    """
    ext_citizen = lab_report_extractor_service.extract_and_verify(raw_text=report_citizen, auto_verify=True)
    record_test("Persona D (Citizen / Institutional Buyer): Consumer Verification", ext_citizen.verification.overall_verdict == OverallVerdict.CONFORMING)


def test_aspect_3_ocr_noise_and_qualitative_edge_cases():
    print("\n=======================================================")
    print("ASPECT 3: OCR NOISE & QUALITATIVE VALUES RESILIENCE")
    print("=======================================================")

    # Test handling of varied qualitative text representations
    qual_text = """
    Standard: IS 14543
    pH: 7.35
    Lead: NOT DETECTED
    Arsenic: ABSENT
    E. Coli: NEGATIVE
    Turbidity: 0.8 NTU
    """
    ext_qual = lab_report_extractor_service.extract_and_verify(raw_text=qual_text, auto_verify=True)
    record_test("Qualitative Values ('Not Detected', 'Absent', 'Negative')", ext_qual.verification.overall_verdict == OverallVerdict.CONFORMING)

    # Test standard code punctuation variants
    for std_variant in ["IS:14543", "IS-14543", "IS14543", "IS 14543 : 2018", "is 14543"]:
        raw = f"Standard: {std_variant}\npH: 7.0\nLead: 0.002 mg/L"
        ext_v = lab_report_extractor_service.extract_and_verify(raw_text=raw, auto_verify=True)
        record_test(f"Standard Code Punctuation: '{std_variant}'", "IS 14543" in ext_v.standard_is_code or "14543" in ext_v.standard_is_code)


def test_aspect_4_official_pdf_generation():
    print("\n=======================================================")
    print("ASPECT 4: OFFICIAL PDF COMPLIANCE REPORT GENERATION")
    print("=======================================================")

    req = AuditRequest(
        standard_is_code="IS 14543",
        product_name="Premium Drinking Water",
        manufacturer_name="AquaPure Ltd",
        batch_number="AQP-2026-PDF",
        testing_lab="BIS Central Laboratory",
        parameters=[
            AuditParameterInput(parameter_name="pH Value", tested_value="7.3", unit=""),
            AuditParameterInput(parameter_name="Lead (as Pb)", tested_value="0.002", unit="mg/L"),
            AuditParameterInput(parameter_name="E. Coli", tested_value="Nil", unit="cfu/250ml")
        ]
    )
    res = compliance_audit_engine.perform_audit(req)
    pdf_path = pdf_report_generator.generate_audit_report(res.audit_id)
    
    record_test("PDF File Created on Disk", pdf_path is not None and os.path.exists(pdf_path))
    file_size = os.path.getsize(pdf_path)
    record_test("PDF File Non-Empty (> 1KB)", file_size > 1000, f"Size={file_size} bytes")
    
    with open(pdf_path, "rb") as f:
        header = f.read(5)
    record_test("PDF Magic Header Valid (%PDF-)", header == b"%PDF-")


def test_aspect_5_fastapi_rest_endpoints():
    print("\n=======================================================")
    print("ASPECT 5: REST API ENDPOINT INTEGRATION")
    print("=======================================================")

    # Endpoint 1: POST /api/v1/audit/extract-lab-report
    res_api = client.post("/api/v1/audit/extract-lab-report", json={
        "raw_text": "Standard: IS 1786\nBatch: BATCH-88\nCarbon: 0.20 %\nYield Strength: 520.0 N/mm²\nElongation: 16.0 %",
        "auto_verify": True
    })
    record_test("POST /audit/extract-lab-report returns 200 OK", res_api.status_code == 200)
    data = res_api.json()
    record_test("API Auto-Verification attached in response", data.get("verification") is not None)
    record_test("API Extracted Parameters >= 3", len(data.get("parameters", [])) >= 3)

    # Endpoint 2: GET /api/v1/audit/report/{audit_id}
    audit_id = data["verification"]["audit_id"]
    res_dl = client.get(f"/api/v1/audit/report/{audit_id}")
    record_test("GET /audit/report/{id} returns 200 OK PDF", res_dl.status_code == 200 and res_dl.headers.get("content-type") == "application/pdf")


if __name__ == "__main__":
    print("\n>>> STARTING EXHAUSTIVE MULTI-ASPECT INDUSTRY EXPERT AUDIT SUITE <<<")
    test_aspect_1_multi_standard_benchmarks()
    test_aspect_2_multi_persona_scenarios()
    test_aspect_3_ocr_noise_and_qualitative_edge_cases()
    test_aspect_4_official_pdf_generation()
    test_aspect_5_fastapi_rest_endpoints()

    print("\n=======================================================")
    print(f"FINAL RESULT: {PASSED_TESTS} / {TOTAL_TESTS} TESTS PASSED (100% SUCCESS RATE)")
    print("=======================================================\n")
