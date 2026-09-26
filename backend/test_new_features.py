import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import asyncio
from app.services.bis_services_directory import search_testing_laboratories, TESTING_LABORATORIES_DIRECTORY
from app.services.license_verifier import license_verifier_service
from app.services.rag_engine import rag_engine
from app.models.schemas import ChatMode

def test_testing_laboratories():
    print("\n--- Testing Laboratories Suggestion Engine ---")
    assert len(TESTING_LABORATORIES_DIRECTORY) >= 12, "Expected at least 12 recognized laboratories"
    
    # Test search by IS standard
    water_labs = search_testing_laboratories(standard_code="IS 14543")
    print(f"Found {len(water_labs)} labs for IS 14543 (Packaged Drinking Water)")
    assert len(water_labs) >= 4, "Expected at least 4 labs for IS 14543"
    for lab in water_labs:
        assert "IS 14543" in lab["standards_supported"]
    
    # Test search by region
    south_labs = search_testing_laboratories(region="South")
    print(f"Found {len(south_labs)} labs in South region")
    assert len(south_labs) >= 2, "Expected at least 2 labs in South"
    for lab in south_labs:
        assert lab["region"] == "South"

    # Test search by discipline
    chem_labs = search_testing_laboratories(discipline="Chemical")
    print(f"Found {len(chem_labs)} labs with Chemical testing discipline")
    assert len(chem_labs) >= 5, "Expected at least 5 chemical labs"

    print(">>> Testing Laboratories Directory: ALL TESTS PASSED!")

def test_fssai_and_ocr_extraction():
    print("\n--- Testing FSSAI & Dual Verification & OCR Extraction ---")
    
    # 1. Registered FSSAI test (Bisleri 14-digit)
    res_fssai = license_verifier_service.verify_identifier("10012011000123", query_type="fssai")
    print(f"Verified Bisleri FSSAI: valid={res_fssai['is_valid']}, product={res_fssai['product_name']}")
    assert res_fssai["is_valid"] is True
    assert "Bisleri" in res_fssai["manufacturer"]
    assert res_fssai["details"].get("linked_bis_cml") == "8400152488"
    assert "IS 14543" in res_fssai["standard_code"]

    # 2. Structural valid FSSAI (State license in Gujarat: code 24)
    res_state = license_verifier_service.verify_identifier("22421001000789", query_type="fssai")
    print(f"Verified State FSSAI: valid={res_state['is_valid']}, lic_type={res_state['details'].get('license_type')}")
    assert res_state["is_valid"] is True
    assert "State License" in res_state["details"].get("license_type", "")
    assert "Gujarat" in res_state["details"].get("state_jurisdiction", "")

    # 3. Invalid FSSAI format
    res_inv = license_verifier_service.verify_identifier("99999", query_type="fssai")
    print(f"Verified Invalid FSSAI: valid={res_inv['is_valid']}, status={res_inv['status']}")
    assert res_inv["is_valid"] is False

    # 4. BIS CM/L with dual FSSAI harmonization
    res_cml = license_verifier_service.verify_identifier("8400152488", query_type="cml")
    print(f"Verified Bisleri CM/L: valid={res_cml['is_valid']}, dual_fssai={res_cml['details'].get('linked_fssai_lic')}")
    assert res_cml["is_valid"] is True
    assert res_cml["details"].get("linked_fssai_lic") == "10012011000123"

    # 5. OCR Text Identifier Extraction
    sample_ocr_text = """
    PURE NATURAL PACKAGED DRINKING WATER
    BIS CERTIFIED: IS 14543
    CM/L-8400152488
    LIC NO. 10012011000123
    FSSAI Central Lic No: 10012011000123
    HUID: AB12CD
    CRS: R-41001234
    BEST BEFORE 12 MONTHS
    """
    extracted = license_verifier_service.extract_identifiers_from_text(sample_ocr_text)
    print(f"Extracted Identifiers from OCR Text: {extracted}")
    types_found = {item["type"]: item["value"] for item in extracted["all"]}
    assert "cml" in types_found and types_found["cml"] == "8400152488", f"CM/L mismatch: {types_found}"
    assert "fssai" in types_found and types_found["fssai"] == "10012011000123", f"FSSAI mismatch: {types_found}"
    assert "crs" in types_found and types_found["crs"] == "R-41001234", f"CRS mismatch: {types_found}"
    assert "huid" in types_found and types_found["huid"] == "AB12CD", f"HUID mismatch: {types_found}"

    print(">>> FSSAI & Dual Verification & OCR Extraction: ALL TESTS PASSED!")

async def test_rag_laboratory_router():
    print("\n--- Testing RAG Laboratory Suggestion Engine ---")
    
    # Query 1: Suggest labs for IS 14543
    q1 = "Suggest recognized testing laboratories for IS 14543 packaged drinking water in North India"
    resp1 = await rag_engine.answer_query(q1, mode=ChatMode.INDUSTRY)
    print(f"Q1 Answer Length: {len(resp1.answer)} chars, Refusal: {resp1.refusal_triggered}")
    assert resp1.refusal_triggered is False
    assert "Sahibabad" in resp1.answer or "Central Laboratory" in resp1.answer
    assert "ISO/IEC 17025" in resp1.answer

    # Query 2: Steel testing in South
    q2 = "Where can I test Fe 500D TMT bars under IS 1786 in South region?"
    resp2 = await rag_engine.answer_query(q2, mode=ChatMode.INDUSTRY)
    print(f"Q2 Answer Length: {len(resp2.answer)} chars, Refusal: {resp2.refusal_triggered}")
    assert resp2.refusal_triggered is False
    assert "Bengaluru" in resp2.answer or "Chennai" in resp2.answer or "Southern Regional Laboratory" in resp2.answer

    print(">>> RAG Laboratory Suggestion Engine: ALL TESTS PASSED!")

async def main():
    test_testing_laboratories()
    test_fssai_and_ocr_extraction()
    await test_rag_laboratory_router()
    print("\n================================================================================")
    print(">>> ALL NEW SIH26107 EXTENDED FEATURES VERIFIED AT 100% SUCCESS! <<<")
    print("================================================================================")

if __name__ == "__main__":
    asyncio.run(main())
