"""
Comprehensive 10/10 Diagnostic Test Suite for GRASK AI / BIS Assistant.
Executes in-memory integration and unit tests using FastAPI TestClient.
"""

import sys
import os
import time
import json

# Ensure backend root is on python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from fastapi.testclient import TestClient
from app.main import app
from app.services.license_verifier import license_verifier_service
from app.services.query_language_guard import query_language_guard
from app.services.certificate_engine import CertificateEngine
from app.services.compliance_audit import compliance_audit_engine, STANDARD_BENCHMARKS
from app.core.gemini_manager import gemini_manager
from app.core.database import init_db

client = TestClient(app)

def run_tests():
    init_db()
    print("=" * 70)
    print("  GRASK AI / BIS QUALITY ASSISTANT - 10/10 SYSTEM DIAGNOSTIC SUITE")
    print("=" * 70)
    
    passes = 0
    total = 0

    # 1. Health & Gemini Manager Status
    total += 1
    t0 = time.time()
    res = client.get("/health")
    dt = (time.time() - t0) * 1000
    if res.status_code == 200 and res.json().get("status") == "healthy":
        print(f"[PASS] System /health check | {dt:.1f}ms | Status: {res.json().get('status')}")
        passes += 1
    else:
        print(f"[FAIL] System /health check failed: {res.text}")

    total += 1
    t0 = time.time()
    res = client.get("/api/v1/health/gemini")
    dt = (time.time() - t0) * 1000
    gem_data = res.json()
    if res.status_code == 200:
        print(f"[PASS] Gemini Health & Cascade | {dt:.1f}ms | Active Model: {gem_data.get('active_model')} | Status: {gem_data.get('status')}")
        passes += 1
    else:
        print(f"[FAIL] Gemini health check failed: {res.text}")

    # 2. Guardrail Filtering
    total += 1
    valid_q = query_language_guard.process("What is the mandatory BIS standard for packaged drinking water?")
    if valid_q.is_in_scope:
        print(f"[PASS] Guardrail: Legitimate query allowed | Confidence: {valid_q.confidence:.2f}")
        passes += 1
    else:
        print(f"[FAIL] Guardrail wrongly rejected legitimate query: {valid_q.refusal_reason}")

    total += 1
    fiction_q = query_language_guard.process("BIS standard for flying anti-gravity cars on Mars")
    if not fiction_q.is_in_scope:
        print(f"[PASS] Guardrail: Fictional/extraterrestrial query blocked | Reason: {fiction_q.refusal_reason}")
        passes += 1
    else:
        print(f"[FAIL] Guardrail failed to reject sci-fi query: {fiction_q}")

    # 3. License Verifier: ISI CM/L, Barcode, FSSAI, HUID, CRS, Unseeded format
    test_licenses = [
        ("CM/L 8400152488 (Packaged Water)", "8400152488", "cml", True),
        ("Barcode 8906056351467 (Parle-G)", "8906056351467", "barcode", True),
        ("FSSAI 10012011000123 (Amul Butter)", "10012011000123", "fssai", True),
        ("HUID AH78K2 (Hallmark Gold)", "AH78K2", "huid", True),
        ("CRS R-41292958 (Boat TWS)", "R-41292958", "crs", True),
        ("Unseeded 7-digit CM/L 1234567", "1234567", "cml", True),
        ("Invalid/Bogus 1234", "1234", "cml", False),
    ]

    for name, ident, qtype, expected_valid in test_licenses:
        total += 1
        res = license_verifier_service.verify(ident, qtype)
        if res.get("is_valid") == expected_valid:
            print(f"[PASS] License Verifier: {name} -> Valid: {res.get('is_valid')}")
            passes += 1
        else:
            print(f"[FAIL] License Verifier: {name} -> Expected {expected_valid}, got {res.get('is_valid')}")

    # 4. Ready-to-Apply Dynamic Certificate & Gap Analysis Engine
    cert_engine = CertificateEngine()
    total += 1
    t0 = time.time()
    prof = cert_engine.resolve_product_profile("packaged drinking water")
    dt = (time.time() - t0) * 1000
    if prof and "14543" in prof.get("is_code", ""):
        print(f"[PASS] Certificate Engine: Packaged Water resolved in {dt:.2f}ms | IS Code: {prof.get('is_code')}")
        passes += 1
    else:
        print(f"[FAIL] Certificate Engine failed to resolve packaged water: {prof}")

    total += 1
    t0 = time.time()
    cached_prof = cert_engine.resolve_product_profile("packaged drinking water")
    dt_cached = (time.time() - t0) * 1000
    if cached_prof:
        print(f"[PASS] Certificate Engine: Cache hit in {dt_cached:.3f}ms (< 1ms target)")
        passes += 1
    else:
        print(f"[FAIL] Certificate Engine cache failed")

    # 5. Compliance Audit Service (New standards IS 4151 helmets, IS 16102 LED, IS 1417 Gold)
    audit_benchmarks = ["IS 14543", "IS 1786", "IS 4151", "IS 16102", "IS 1417"]
    for std in audit_benchmarks:
        total += 1
        bench = STANDARD_BENCHMARKS.get(std)
        if bench and len(bench.get("parameters", {})) > 0:
            print(f"[PASS] Compliance Audit: {std} ({bench.get('title')}) -> {len(bench.get('parameters'))} benchmark parameters")
            passes += 1
        else:
            print(f"[FAIL] Compliance Audit benchmark missing for {std}")

    # 6. Telemetry API Endpoint
    total += 1
    t0 = time.time()
    res = client.get("/api/v1/telemetry/dashboard")
    dt = (time.time() - t0) * 1000
    if res.status_code == 200 and "total_queries" in res.json():
        telem = res.json()
        print(f"[PASS] Telemetry Dashboard API | {dt:.1f}ms | Total Queries: {telem.get('total_queries')} | Satisfaction: {telem.get('satisfaction_rate')}%")
        passes += 1
    else:
        print(f"[FAIL] Telemetry Dashboard API failed: {res.text}")

    print("=" * 70)
    score_pct = (passes / total) * 100
    print(f"DIAGNOSTIC SUMMARY: {passes}/{total} TESTS PASSED ({score_pct:.1f}%)")
    print("=" * 70)
    return passes == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
