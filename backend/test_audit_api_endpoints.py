import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_audit_extract_api():
    print("\n--- Testing /api/v1/audit/extract-lab-report ---")
    payload = {
        "raw_text": """
        CENTRAL LABORATORY SAHIBABAD
        TEST REPORT / CERTIFICATE OF COMPLIANCE
        Standard: IS 14543 : 2018 (Packaged Drinking Water)
        Manufacturer: Himalayan Mineral Springs Ltd
        Batch No: HMS-2026-B402
        Testing Lab: BIS Central Laboratory

        RESULTS:
        pH Value: 7.35
        Total Dissolved Solids (TDS): 125.0 mg/L
        Turbidity: 0.45 NTU
        Lead (as Pb): 0.003 mg/L
        Arsenic (as As): 0.002 mg/L
        """,
        "image_base64": None,
        "auto_verify": True
    }

    res = client.post("/api/v1/audit/extract-lab-report", json=payload)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    print("API Response Status:", data.get("status"))
    print("IS Code:", data.get("standard_is_code"))
    print("Batch:", data.get("batch_number"))
    print("Extracted Parameters:", len(data.get("parameters", [])))
    
    assert "IS 14543" in data["standard_is_code"]
    assert len(data["parameters"]) >= 5
    assert data["verification"] is not None
    print("Verification Verdict:", data["verification"]["overall_verdict"])
    print("Verification Score:", data["verification"]["compliance_score_percent"])
    assert data["verification"]["overall_verdict"] == "CONFORMING"
    print(">>> /api/v1/audit/extract-lab-report endpoint: PASSED!")


def test_audit_upload_api():
    print("\n--- Testing /api/v1/audit/upload-lab-report ---")
    dummy_img_content = b"RIFF\x24\x00\x00\x00WEBPVP8 \x18\x00\x00\x000\x01\x00\x9d\x01\x2a\x01\x00\x01\x00\x02\x00\x34\x25\xa4\x00\x03\x70\x00\xfe\xfb\xfd\x50\x00"
    
    files = {
        "file": ("lab_report.jpg", dummy_img_content, "image/jpeg")
    }
    data = {
        "auto_verify": "true"
    }

    res = client.post("/api/v1/audit/upload-lab-report", files=files, data=data)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    resp_data = res.json()
    print("Upload API Response Status:", resp_data.get("status"))
    assert resp_data["status"] == "IRRELEVANT_DATA"
    assert resp_data["is_relevant"] is False
    print("Relevance Reason:", resp_data.get("relevance_reason"))
    print(">>> /api/v1/audit/upload-lab-report endpoint: PASSED (Correctly flagged irrelevant dummy data)!")


if __name__ == "__main__":
    test_audit_extract_api()
    test_audit_upload_api()
    print("\n================ ALL API ROUTE TESTS PASSED ================\n")
