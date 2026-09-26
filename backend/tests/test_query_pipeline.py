"""
Comprehensive Query Pipeline Test Suite
Tests all 12 pipeline steps across languages, difficulty levels, and domains.

Usage:
    python tests/test_query_pipeline.py

Categories:
  - Simple: single domain, clear language
  - Hard: multi-word, typos, ambiguous
  - Complex: multi-domain, regional language
  - Advanced: mixed scripts, Romanized + English blend
  - Edge: gibberish, empty, adversarial
"""

import sys
import json
import urllib.request
import urllib.error
import time
from dataclasses import dataclass
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api/v1/chat"

@dataclass
class TestCase:
    label: str
    query: str
    mode: str                         # 'consumer' or 'industry'
    expect_refusal: bool              # True = should refuse, False = should answer
    expect_keyword: Optional[str]     # keyword that must appear in answer if not refused
    category: str                     # simple/hard/complex/advanced/edge

TESTS = [
    # ─── SIMPLE ENGLISH ───────────────────────────────────────────────────────
    TestCase("Simple: Packaged water IS code", "What is IS 14543 for packaged drinking water?", "consumer", False, "14543", "simple"),
    TestCase("Simple: TMT steel", "TMT steel IS 1786 requirements", "industry", False, "1786", "simple"),
    TestCase("Simple: Gold hallmarking", "gold hallmarking HUID", "consumer", False, "hallmark", "simple"),
    TestCase("Simple: FSSAI license", "How to get FSSAI food license?", "consumer", False, "FSSAI", "simple"),
    TestCase("Simple: Helmet safety", "helmet safety standard", "consumer", False, "IS 4151", "simple"),
    TestCase("Simple: Cement grade", "OPC cement IS 269", "industry", False, "IS 269", "simple"),

    # ─── HARD ENGLISH (typos, informal) ──────────────────────────────────────
    TestCase("Hard: Typo paani plant", "paani plant license kaise milega", "industry", False, "IS 14543", "hard"),
    TestCase("Hard: Typo sariya", "sariya dukanam quality check", "industry", False, "IS 1786", "hard"),
    TestCase("Hard: Hinglish MRP", "shopkeeper MRP se zyada charge kar raha hai", "consumer", False, "MRP", "hard"),
    TestCase("Hard: Mixed food query", "doodh ki dukan kholni hai", "industry", False, "FSSAI", "hard"),
    TestCase("Hard: Typos in english", "packged drinkng watr standrd", "consumer", False, "14543", "hard"),
    TestCase("Hard: Chilling charge query", "kya cold drink pe chilling charge legal hai", "consumer", False, "MRP", "hard"),

    # ─── COMPLEX REGIONAL ROMANIZED ──────────────────────────────────────────
    TestCase("Complex: Telugu milk shop", "paala dukanam FSSAI rules", "industry", False, "FSSAI", "complex"),
    TestCase("Complex: Telugu gold shop", "bangaaram dukanam huid mandatory", "consumer", False, "hallmark", "complex"),
    TestCase("Complex: Telugu water plant", "neellu plant BIS license", "industry", False, "14543", "complex"),
    TestCase("Complex: Hindi cement shop", "cement ki dukan kholne ke liye kya chahiye", "industry", False, "IS 269", "complex"),
    TestCase("Complex: Hindi steel shop", "sariya ki dukan ke liye BIS certificate", "industry", False, "IS 1786", "complex"),
    TestCase("Complex: Tamil milk shop", "paal kadai FSSAI license", "industry", False, "FSSAI", "complex"),

    # ─── ADVANCED MULTI-LANGUAGE / INDIC SCRIPT ──────────────────────────────
    TestCase("Advanced: Hindi Devanagari gold", "सोना हॉलमार्क", "consumer", False, "hallmark", "advanced"),
    TestCase("Advanced: Tanglish water", "packaged water la lead limit enna", "consumer", False, "14543", "advanced"),
    TestCase("Advanced: Telugu vegetable market", "kuragayala kottu food safety", "consumer", False, None, "advanced"),
    TestCase("Advanced: Complex IS code search", "IS 1293 plug socket child safety", "consumer", False, "IS 1293", "advanced"),
    TestCase("Advanced: Organic food", "organic food jaivik bharat certification", "industry", False, "organic", "advanced"),

    # ─── OUT-OF-SCOPE (should refuse) ────────────────────────────────────────
    TestCase("Edge: Medicine shop Telugu", "mandhula dhukaanam", "consumer", True, None, "edge"),
    TestCase("Edge: Medicine shop Hindi", "dawai ki dukan", "consumer", True, None, "edge"),
    TestCase("Edge: Hospital Tamil", "marundhu kadai license", "consumer", True, None, "edge"),
    TestCase("Edge: Cricket score", "india vs australia cricket score", "consumer", True, None, "edge"),
    TestCase("Edge: Movie ticket", "how to book movie ticket online", "consumer", True, None, "edge"),
    TestCase("Edge: Stock market", "sensex nifty stock market today", "consumer", True, None, "edge"),
    TestCase("Edge: Driving license", "driving licence renew kaise kare", "consumer", True, None, "edge"),
    TestCase("Edge: Weather query", "what is the weather in Hyderabad today", "consumer", True, None, "edge"),
    TestCase("Edge: Recipe request", "how to make chocolate cake recipe", "consumer", True, None, "edge"),

    # ─── SEMANTIC / GIBBERISH (should refuse) ─────────────────────────────────
    TestCase("Edge: Keyboard gibberish", "asdfghjkl qwerty", "consumer", True, None, "edge"),
    TestCase("Edge: Random chars", "xyzxyzxyz 12312312", "consumer", True, None, "edge"),
    TestCase("Edge: Single char", "a", "consumer", True, None, "edge"),
]


def query_api(message: str, mode: str) -> dict:
    body = json.dumps({"message": message, "mode": mode}).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"}
    except Exception as e:
        return {"error": str(e)}


def run_tests():
    results = {"passed": 0, "failed": 0, "errors": 0, "details": []}
    categories = {}

    print("\n" + "="*70)
    print("  BIS ASSISTANT — COMPREHENSIVE QUERY PIPELINE TEST SUITE")
    print("="*70)

    for i, tc in enumerate(TESTS, 1):
        print(f"\n[{i:02d}/{len(TESTS)}] {tc.label}")
        print(f"       Query: \"{tc.query}\"")

        start = time.time()
        data = query_api(tc.query, tc.mode)
        elapsed = time.time() - start

        if "error" in data:
            print(f"       ❌ ERROR: {data['error']}")
            results["errors"] += 1
            results["details"].append({"label": tc.label, "status": "ERROR", "error": data["error"]})
            categories.setdefault(tc.category, {"passed": 0, "failed": 0, "errors": 0})
            categories[tc.category]["errors"] += 1
            continue

        refusal = data.get("refusal_triggered", False)
        confidence = data.get("confidence_score", 0)
        answer = data.get("answer", "")
        is_safe = data.get("is_hallucination_safe", True)

        # Determine pass/fail
        passed = True
        fail_reasons = []

        # Refusal check
        if tc.expect_refusal and not refusal:
            passed = False
            fail_reasons.append(f"Expected REFUSAL but got answer (confidence={confidence})")
        elif not tc.expect_refusal and refusal:
            passed = False
            fail_reasons.append(f"Expected ANSWER but got REFUSED")

        # Keyword check (only when not expecting refusal)
        if not tc.expect_refusal and not refusal and tc.expect_keyword:
            if tc.expect_keyword.lower() not in answer.lower():
                passed = False
                fail_reasons.append(f"Expected keyword '{tc.expect_keyword}' not found in answer")

        # Status
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"       {status} | Refusal={refusal} | Conf={confidence:.2f} | Safe={is_safe} | Time={elapsed:.1f}s")
        if fail_reasons:
            for r in fail_reasons:
                print(f"       ⚠️  {r}")
        if not passed and not refusal:
            print(f"       Answer preview: {answer[:200]}")

        categories.setdefault(tc.category, {"passed": 0, "failed": 0, "errors": 0})
        if passed:
            results["passed"] += 1
            categories[tc.category]["passed"] += 1
        else:
            results["failed"] += 1
            categories[tc.category]["failed"] += 1

        results["details"].append({
            "label": tc.label,
            "query": tc.query,
            "category": tc.category,
            "status": "PASS" if passed else "FAIL",
            "refusal_triggered": refusal,
            "confidence": confidence,
            "is_hallucination_safe": is_safe,
            "time_s": round(elapsed, 2),
            "fail_reasons": fail_reasons,
        })

    # ── Summary ──────────────────────────────────────────────────────────────
    total = results["passed"] + results["failed"] + results["errors"]
    pass_rate = (results["passed"] / total * 100) if total else 0

    print("\n" + "="*70)
    print("  RESULTS SUMMARY")
    print("="*70)
    print(f"  Total  : {total}")
    print(f"  ✅ Pass : {results['passed']} ({pass_rate:.1f}%)")
    print(f"  ❌ Fail : {results['failed']}")
    print(f"  💥 Error: {results['errors']}")

    print("\n  By Category:")
    for cat, counts in sorted(categories.items()):
        cat_total = counts["passed"] + counts["failed"] + counts["errors"]
        cat_rate = (counts["passed"] / cat_total * 100) if cat_total else 0
        print(f"    {cat:10s} → {counts['passed']}/{cat_total} ({cat_rate:.0f}%)")

    # Save JSON results
    import os
    os.makedirs("tests", exist_ok=True)
    out_path = "tests/pipeline_test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n  Full results saved → {out_path}")
    print("="*70)

    return results["failed"] == 0 and results["errors"] == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
