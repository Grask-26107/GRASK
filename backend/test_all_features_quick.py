import urllib.request
import json
import time
import sys

endpoints = [
    ('Verify Barcode 8906056351467', 'http://localhost:8000/api/v1/standards/verify-license', {'identifier': '8906056351467', 'query_type': 'barcode'}),
    ('Verify CM/L 8400152488', 'http://localhost:8000/api/v1/standards/verify-license', {'identifier': '8400152488', 'query_type': 'cml'}),
    ('Verify FSSAI 10012011000123', 'http://localhost:8000/api/v1/standards/verify-license', {'identifier': '10012011000123', 'query_type': 'fssai'}),
    ('Verify HUID AH78K2', 'http://localhost:8000/api/v1/standards/verify-license', {'identifier': 'AH78K2', 'query_type': 'huid'}),
    ('Verify CRS R-41292958', 'http://localhost:8000/api/v1/standards/verify-license', {'identifier': 'R-41292958', 'query_type': 'crs'}),
    ('Translate to Hindi', 'http://localhost:8000/api/v1/chat/translate', {'text': 'Bureau of Indian Standards', 'target_language': 'hi'}),
    ('OCR Extract Text', 'http://localhost:8000/api/v1/standards/ocr-extract', {'ocr_text': 'FSSAI: 10012011000123 CM/L: 8400152488'})
]

print("=== VERIFYING ALL AUXILIARY FEATURES LIVE ===")
for name, url, payload in endpoints:
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req, timeout=5)
        dt = (time.time() - t0) * 1000
        d = json.loads(res.read().decode('utf-8'))
        print(f"[PASS] {name:30s} | HTTP {res.status} | {dt:5.1f}ms")
    except Exception as e:
        print(f"[FAIL] {name:30s} | ERROR: {e}")
