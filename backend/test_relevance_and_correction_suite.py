import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.services.domain_relevance_guard import domain_relevance_guard
from app.services.license_verifier import license_verifier_service
from app.services.nutri_analyzer import nutri_analyzer_service
from app.services.lab_report_extractor import lab_report_extractor_service

def run_tests():
    print("=" * 70)
    print("RUNNING RELEVANCE GUARD & GRAMMAR / SPELLING CORRECTION SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Grammar, Spelling & Typo Correction
    # -------------------------------------------------------------
    print("\n--- 1. Testing Typo & Semantic Correction ---")
    test_text_nutri = "energe 450 kcal, proteen 8g, sugr 25g, sodum 400mg, ingridients: palmoil, maida"
    clean_nutri = domain_relevance_guard.clean_and_correct_text(test_text_nutri, feature="nutri_score")
    print("Original:", test_text_nutri)
    print("Corrected:", clean_nutri["corrected_text"])
    assert "protein" in clean_nutri["corrected_text"].lower(), "Protein typo was not corrected!"
    assert "palm oil" in clean_nutri["corrected_text"].lower(), "Palm oil was not normalized!"
    print("✅ Typo correction passed.")

    # -------------------------------------------------------------
    # 2. Text Relevance Checks
    # -------------------------------------------------------------
    print("\n--- 2. Testing Domain Relevance Checks ---")
    car_text = "Check this photo of a red Toyota Corolla sedan car with alloy wheels"
    
    is_rel_audit, reason_audit, _ = domain_relevance_guard.check_text_relevance(car_text, feature="audit_compliance")
    print(f"Audit Compliance on car text -> is_relevant={is_rel_audit}, reason='{reason_audit}'")
    assert not is_rel_audit, "Car text should NOT be relevant to audit compliance!"

    is_rel_nutri, reason_nutri, _ = domain_relevance_guard.check_text_relevance(car_text, feature="nutri_score")
    print(f"Nutri Score on car text -> is_relevant={is_rel_nutri}, reason='{reason_nutri}'")
    assert not is_rel_nutri, "Car text should NOT be relevant to nutri score!"

    is_rel_mark, reason_mark, _ = domain_relevance_guard.check_text_relevance(car_text, feature="mark_check")
    print(f"Mark Check on car text -> is_relevant={is_rel_mark}, reason='{reason_mark}'")
    assert not is_rel_mark, "Car text should NOT be relevant to mark check!"
    print("✅ Negative vehicle keyword detection passed across all features.")

    # -------------------------------------------------------------
    # 3. License Verifier Guard & Anti-Hallucination
    # -------------------------------------------------------------
    print("\n--- 3. Testing License Verifier Guard ---")
    # A. Car name "TOYOTA" should not match HUID
    toyota_res = license_verifier_service.verify_identifier("TOYOTA")
    print(f"Verify 'TOYOTA' -> status='{toyota_res.get('status')}', is_relevant={toyota_res.get('is_relevant')}")
    assert toyota_res.get("status") == "IRRELEVANT_DATA" or not toyota_res.get("is_relevant"), "TOYOTA must be rejected as irrelevant!"

    # B. Vehicle sentence
    car_query_res = license_verifier_service.verify_identifier("my honda civic car engine")
    print(f"Verify 'my honda civic' -> status='{car_query_res.get('status')}', is_relevant={car_query_res.get('is_relevant')}")
    assert car_query_res.get("status") == "IRRELEVANT_DATA", "Honda civic query must return IRRELEVANT_DATA!"

    # C. Genuine HUID "AB12CD"
    huid_res = license_verifier_service.verify_identifier("AB12CD")
    print(f"Verify 'AB12CD' -> status='{huid_res.get('status')}', is_valid={huid_res.get('is_valid')}")
    assert huid_res.get("is_valid") is True, "AB12CD should be valid genuine hallmark!"

    # D. Genuine Barcode "8905650102321"
    barcode_res = license_verifier_service.verify_identifier("8905650102321")
    print(f"Verify '8905650102321' -> brand='{barcode_res.get('brand_name')}', is_valid={barcode_res.get('is_valid')}")
    assert barcode_res.get("is_valid") is True, "boAt barcode should be authentic!"

    print("✅ License Verifier guard passed.")

    # -------------------------------------------------------------
    # 4. Nutri Score Guard & Anti-Hallucination
    # -------------------------------------------------------------
    print("\n--- 4. Testing Nutri Score Guard ---")
    nutri_car_res = nutri_analyzer_service.analyze(text="toyota corolla v8 engine gearbox")
    print(f"Nutri analyze car -> status='{nutri_car_res.get('status')}', verdict='{nutri_car_res.get('verdict')}', is_relevant={nutri_car_res.get('is_relevant')}")
    assert nutri_car_res.get("status") == "IRRELEVANT_DATA", "Nutri analyze on car should return IRRELEVANT_DATA!"
    assert nutri_car_res.get("is_relevant") is False, "is_relevant must be False!"

    nutri_food_res = nutri_analyzer_service.analyze(text="Energy: 480 kcal, Sugar: 30g, Palm Oil, Sodium: 520mg, Wheat flour")
    print(f"Nutri analyze food -> status='{nutri_food_res.get('status')}', verdict='{nutri_food_res.get('verdict')}', is_relevant={nutri_food_res.get('is_relevant')}")
    assert nutri_food_res.get("is_relevant") is True, "Food text should be relevant!"
    assert nutri_food_res.get("verdict") in ["HARMFUL", "CAUTION"], "High sugar/palm oil should be HARMFUL or CAUTION!"

    print("✅ Nutri Score guard passed.")

    # -------------------------------------------------------------
    # 5. Lab Report Audit Extractor Guard & Anti-Hallucination
    # -------------------------------------------------------------
    print("\n--- 5. Testing Lab Report Extractor Guard ---")
    audit_car_res = lab_report_extractor_service.extract_lab_report(raw_text="This is a photograph of my sports car driving on the highway", auto_verify=True)
    print(f"Audit extract car -> status='{audit_car_res.status}', is_relevant={audit_car_res.is_relevant}, params_count={len(audit_car_res.parameters)}")
    assert audit_car_res.status == "IRRELEVANT_DATA", "Car text must return IRRELEVANT_DATA!"
    assert audit_car_res.is_relevant is False, "is_relevant must be False!"
    assert len(audit_car_res.parameters) == 0, "No dummy parameters must be injected!"

    # Relevant lab report text
    lab_text = """
    NATIONAL ENVIRONMENTAL LABORATORY
    TEST REPORT FOR PACKAGED DRINKING WATER (IS 14543)
    Batch: NEL-2026-991
    1. pH Value: 7.2
    2. Total Dissolved Solids: 110 mg/L
    3. Lead (as Pb): 0.002 mg/L
    4. Turbidity: 0.4 NTU
    """
    audit_valid_res = lab_report_extractor_service.extract_lab_report(raw_text=lab_text, auto_verify=True)
    print(f"Audit extract valid -> status='{audit_valid_res.status}', is_relevant={audit_valid_res.is_relevant}, params_count={len(audit_valid_res.parameters)}")
    assert audit_valid_res.is_relevant is True, "Valid lab text should be relevant!"
    assert len(audit_valid_res.parameters) >= 3, "Parameters must be parsed!"

    print("✅ Lab Report Extractor guard passed.")

    print("\n" + "=" * 70)
    print("ALL SUITE TESTS PASSED 100%!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
