import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.models.schemas import AuditReportExtractRequest
from app.services.lab_report_extractor import lab_report_extractor_service

def test_water_lab_report_extraction():
    sample_text = """
    CENTRAL LABORATORY SAHIBABAD (NABL ACCREDITED)
    TEST REPORT / CERTIFICATE OF COMPLIANCE
    Standard: IS 14543 : 2018 (Packaged Drinking Water)
    Customer: Himalayan Mineral Springs Ltd
    Batch No: HMS-2026-B402
    Tested by: BIS Regional Water Testing Facility

    TEST RESULTS:
    1. pH Value: 7.35
    2. Total Dissolved Solids (TDS): 125.0 mg/L
    3. Turbidity: 0.45 NTU
    4. Lead (as Pb): 0.003 mg/L
    5. Arsenic (as As): 0.002 mg/L
    6. Nitrate (as NO3): 14.2 mg/L
    7. Escherichia coli (E. coli): Nil cfu/250ml
    """
    
    print("\n--- Running Water Lab Report Extraction Test ---")
    result = lab_report_extractor_service.extract_and_verify(
        raw_text=sample_text,
        image_base64=None,
        auto_verify=True
    )

    print(f"Extracted IS Code: {result.standard_is_code}")
    print(f"Extracted Product: {result.product_name}")
    print(f"Extracted Batch: {result.batch_number}")
    print(f"Extracted Parameters Count: {len(result.parameters)}")
    for p in result.parameters:
        print(f"  - {p.parameter_name}: {p.tested_value} {p.unit}")

    assert "IS 14543" in result.standard_is_code
    assert result.batch_number == "HMS-2026-B402"
    assert len(result.parameters) >= 5
    
    # Check Auto Verification
    assert result.verification is not None
    print(f"Auto-Verification Verdict: {result.verification.overall_verdict}")
    print(f"Compliance Score: {result.verification.compliance_score_percent}%")
    print(f"Passed: {result.verification.passed_count}, Failed: {result.verification.failed_count}")
    assert result.verification.overall_verdict.value == "CONFORMING"
    print(">>> Water Lab Report Extraction & Auto-Verification: SUCCESS!")


def test_steel_lab_report_failure_extraction():
    sample_text = """
    METALLURGICAL TEST CERTIFICATE
    Standard: IS 1786:2008 (High Strength Deformed Steel Bars Fe 500D)
    Manufacturer: Deccan High-Tensile Steel Mills Ltd
    Batch No: DHSM-FE500D-FAIL-01
    Testing Lab: Central Metallurgy Lab

    OBSERVED MECHANICAL & CHEMICAL PROPERTIES:
    Carbon: 0.38 %
    Sulphur: 0.075 %
    Phosphorus: 0.040 %
    0.2% Proof Stress: 485.0 N/mm²
    Elongation: 12.0 %
    """

    print("\n--- Running Steel Lab Report (Non-Conforming) Extraction Test ---")
    result = lab_report_extractor_service.extract_and_verify(
        raw_text=sample_text,
        image_base64=None,
        auto_verify=True
    )

    print(f"Extracted IS Code: {result.standard_is_code}")
    print(f"Extracted Batch: {result.batch_number}")
    print(f"Parameters Count: {len(result.parameters)}")
    for p in result.parameters:
        print(f"  - {p.parameter_name}: {p.tested_value} {p.unit}")

    assert "IS 1786" in result.standard_is_code
    assert result.verification is not None
    print(f"Auto-Verification Verdict: {result.verification.overall_verdict}")
    print(f"Passed: {result.verification.passed_count}, Failed: {result.verification.failed_count}")
    assert result.verification.failed_count > 0
    print(">>> Steel Lab Report Failure Extraction & Auto-Verification: SUCCESS!")


if __name__ == "__main__":
    test_water_lab_report_extraction()
    test_steel_lab_report_failure_extraction()
    print("\n================ ALL TESTS PASSED ================\n")
