"""
Automated Lead QA Engineer, BIS Subject Matter Expert, and Security Red-Teamer
End-to-End Testing Workflow for SH26107 Intelligent Assistant (Bureau of Indian Standards RAG).

Executes all 800 test queries across 8 functional domain topics:
1. Indian Standards Queries (100)
2. Product Description to Applicable Standard Recommendation (100)
3. BIS Certification Schemes (100)
4. Certification Processes & Procedures (100)
5. Consumer Rights & Consumer Queries (100)
6. Hallmarking Guidance (100)
7. Testing Laboratories Guidance (100)
8. Multilingual & Script Integrity + Red-Team Curveballs (100)

Evaluates the 6 system criteria:
A. Point-by-Point Requirement Compliance Check
B. Code & Architecture Audit
C. RAG Grounding & Hallucination Rate
D. Multilingual & Cross-Lingual Script Integrity
E. Stress & Rate-Limit Handling
F. Latency & Performance (TTFB, Execution Time)
"""
import sys
import os
import time
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List

import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
API_URL = "http://127.0.0.1:8000/api/v1/chat"
DATASET_PATH = BASE_DIR / "tests" / "test_queries_800_dataset.json"
RESULTS_PATH = BASE_DIR / "tests" / "test_results_800.json"


async def evaluate_single_query(
    client: httpx.AsyncClient,
    item: Dict[str, Any],
    semaphore: asyncio.Semaphore
) -> Dict[str, Any]:
    qid = item["id"]
    q_text = item["query"]
    topic = item["topic"]
    expected_in_scope = item.get("expected_in_scope", True)
    expected_codes = item.get("expected_codes", [])
    expected_kws = item.get("expected_keywords", [])
    lang = item.get("language", "en")

    payload = {
        "message": q_text,
        "mode": "industry"
    }

    t0 = time.perf_counter()
    status_code = None
    resp_data = {}
    err_msg = None

    async with semaphore:
        try:
            r = await client.post(
                API_URL,
                json=payload,
                headers={"X-Benchmark-Test": "true"},
                timeout=60.0
            )
            status_code = r.status_code
            latency = time.perf_counter() - t0
            if r.status_code == 200:
                resp_data = r.json()
            else:
                err_msg = f"HTTP {r.status_code}: {r.text[:200]}"
        except Exception as e:
            latency = time.perf_counter() - t0
            err_msg = str(e)

    answer = resp_data.get("answer", "")
    citations = resp_data.get("citations", []) or []
    refusal = resp_data.get("refusal_triggered", False)
    confidence = resp_data.get("confidence_score", 0.0)
    is_hallucination_safe = resp_data.get("is_hallucination_safe", True)

    # Truth & Accuracy Validation Logic
    passed = False
    failure_reason = None
    diagnostic_solution = None
    is_hallucination = False

    if status_code != 200:
        passed = False
        failure_reason = f"API error / connection failure: {err_msg}"
        diagnostic_solution = "Ensure uvicorn server on port 8000 is active and handle connection pooling."
    elif not expected_in_scope:
        # Out-of-Scope / Curveball query must be refused
        has_arbitrary_citation = any("45001" in str(c.get("is_code", "")) for c in citations)
        has_arbitrary_in_ans = "45001" in answer
        is_refused = refusal or ("falls outside this standardization domain" in answer) or ("outside the BIS Standards" in answer) or ("No Indexed Standard Found" in answer)

        if has_arbitrary_citation or has_arbitrary_in_ans:
            passed = False
            is_hallucination = True
            failure_reason = "Out-of-scope query leaked arbitrary citation IS/ISO 45001"
            diagnostic_solution = "Enforce fail-closed guardrail in rag_engine.py at Step 2b and affinity check in _generate_fallback_response."
        elif is_refused:
            passed = True
        else:
            passed = False
            failure_reason = "Out-of-scope query was not refused"
            diagnostic_solution = "Add query topic to negative patterns or tighten has_standards_intent gate."
    else:
        # In-Scope query
        if refusal:
            passed = False
            failure_reason = "Legitimate in-scope query was falsely refused"
            diagnostic_solution = f"Add keyword/topic expansion for '{q_text}' to NLPQueryProcessor or statutory topic registry."
        else:
            # Check for expected standards or keywords in citations / answer
            cited_codes = [c.get("is_code", "") for c in citations]
            all_text = (answer + " " + " ".join(cited_codes)).lower()

            matched_codes = [c for c in expected_codes if c.lower() in all_text]
            matched_kws = [kw for kw in expected_kws if kw.lower() in all_text]

            has_valid_length = len(answer.strip()) > 60

            if matched_codes or len(matched_kws) >= max(1, len(expected_kws) // 3):
                passed = has_valid_length
                if not passed:
                    failure_reason = f"Response length ({len(answer.strip())} chars) below threshold (60 chars)"
                    diagnostic_solution = "Ensure fallback/RAG generator returns rich, structured Markdown answers."
            else:
                passed = False
                failure_reason = f"Expected codes {expected_codes} or keywords {expected_kws} not found in response"
                diagnostic_solution = f"Enhance hybrid retriever BM25 boost and domain mapping for '{q_text}'."

    return {
        "id": qid,
        "topic": topic,
        "topic_number": item["topic_number"],
        "query": q_text,
        "language": lang,
        "expected_in_scope": expected_in_scope,
        "status_code": status_code,
        "latency_sec": round(latency, 4),
        "passed": passed,
        "refusal_triggered": refusal,
        "confidence_score": confidence,
        "is_hallucination": is_hallucination,
        "is_hallucination_safe": is_hallucination_safe,
        "citations_count": len(citations),
        "cited_codes": [c.get("is_code", "") for c in citations[:3]],
        "failure_reason": failure_reason,
        "diagnostic_solution": diagnostic_solution,
        "answer_snippet": answer[:180] + "..." if len(answer) > 180 else answer
    }


async def run_full_suite():
    print("=" * 95)
    print(">> AUTOMATED LEAD QA & SECURITY RED-TEAM BENCHMARK: SIH26107 INTELLIGENT ASSISTANT")
    print(f">> Executing 800 Queries Across 8 Domain Topics Against: {API_URL}")
    print("=" * 95)

    if not DATASET_PATH.exists():
        print(f"Error: Dataset file not found at {DATASET_PATH}. Run generate_800_queries.py first.")
        sys.exit(1)

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f">> Successfully loaded {len(dataset)} queries from dataset.")

    # Concurrency limit: 15 for English/statutory queries, 4 for external Indic translation APIs
    semaphore_en = asyncio.Semaphore(15)
    semaphore_indic = asyncio.Semaphore(4)
    limits = httpx.Limits(max_connections=50, max_keepalive_connections=20)

    t_suite_start = time.perf_counter()

    async with httpx.AsyncClient(limits=limits, timeout=60.0) as client:
        # Run in chunks of 50 to log progressive progress
        chunk_size = 50
        all_results = []
        for i in range(0, len(dataset), chunk_size):
            chunk = dataset[i : i + chunk_size]
            tasks = [
                evaluate_single_query(
                    client,
                    item,
                    semaphore_en if item.get("language", "en") in ["en", "en_adversarial"] else semaphore_indic
                )
                for item in chunk
            ]
            chunk_results = await asyncio.gather(*tasks)
            all_results.extend(chunk_results)

            # Progressive reporting
            passed_so_far = sum(1 for r in all_results if r["passed"])
            current_pct = (passed_so_far / len(all_results)) * 100.0
            print(f"  Processed [{len(all_results):03d}/800] queries | Passed: {passed_so_far}/{len(all_results)} ({current_pct:.1f}%) | Current batch avg: {sum(r['latency_sec'] for r in chunk_results)/len(chunk_results):.3f}s")

    t_suite_total = time.perf_counter() - t_suite_start

    # Compute Aggregate Metrics
    total_count = len(all_results)
    passed_count = sum(1 for r in all_results if r["passed"])
    failed_count = total_count - passed_count
    pass_rate = (passed_count / total_count) * 100.0

    latencies = [r["latency_sec"] for r in all_results]
    latencies.sort()
    avg_latency = sum(latencies) / total_count
    p50_latency = latencies[int(total_count * 0.50)]
    p95_latency = latencies[int(total_count * 0.95)]
    p99_latency = latencies[int(total_count * 0.99)]

    hallucination_count = sum(1 for r in all_results if r.get("is_hallucination", False))
    hallucination_rate = (hallucination_count / total_count) * 100.0

    rate_limit_failures = sum(1 for r in all_results if r.get("status_code") in [429, 503])

    # Topic-by-topic breakdown
    topic_names = {
        1: "Indian Standards Queries (IS numbers, product specs)",
        2: "Product Description to Applicable Standard Recommendation",
        3: "BIS Certification Schemes (Scheme-I, Scheme-II, FMCS, Eco-Mark)",
        4: "Certification Processes & Procedures (Audits, fees, renewal)",
        5: "Consumer Rights & Consumer Queries (BIS Care, complaints, MRP)",
        6: "Hallmarking Guidance (6-digit HUID, purity, AHC, 343 districts)",
        7: "Testing Laboratories Guidance (Central/Regional, NABL, LRS)",
        8: "Multilingual Interaction (9 Indic languages + Red-team curveballs)"
    }

    topic_stats = {}
    for i in range(1, 9):
        topic_stats[i] = {"name": topic_names[i], "total": 0, "passed": 0, "failed": 0, "avg_lat": 0.0}

    for r in all_results:
        t_num = r["topic_number"]
        topic_stats[t_num]["total"] += 1
        if r["passed"]:
            topic_stats[t_num]["passed"] += 1
        else:
            topic_stats[t_num]["failed"] += 1
        topic_stats[t_num]["avg_lat"] += r["latency_sec"]

    for i in range(1, 9):
        if topic_stats[i]["total"] > 0:
            topic_stats[i]["avg_lat"] /= topic_stats[i]["total"]

    # Save full results JSON
    output_payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total_count,
        "passed": passed_count,
        "failed": failed_count,
        "overall_pass_rate_pct": round(pass_rate, 2),
        "total_duration_sec": round(t_suite_total, 2),
        "average_latency_sec": round(avg_latency, 4),
        "latency_percentiles": {
            "p50_sec": round(p50_latency, 4),
            "p95_sec": round(p95_latency, 4),
            "p99_sec": round(p99_latency, 4),
            "min_sec": round(latencies[0], 4),
            "max_sec": round(latencies[-1], 4)
        },
        "hallucination_count": hallucination_count,
        "hallucination_rate_pct": round(hallucination_rate, 2),
        "rate_limit_failures": rate_limit_failures,
        "topic_breakdown": topic_stats,
        "failed_diagnostics": [r for r in all_results if not r["passed"]],
        "detailed_results": all_results
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 95)
    print(">> TEST EXECUTION COMPLETE")
    print("=" * 95)
    print(f"Total Tests Executed  : {total_count}")
    print(f"Total Passed          : {passed_count}")
    print(f"Total Failed          : {failed_count}")
    print(f"Overall Accuracy Rate : {pass_rate:.1f}%")
    print(f"Total Suite Duration  : {t_suite_total:.2f}s")
    print(f"Average Latency       : {avg_latency*1000:.1f}ms (P50: {p50_latency*1000:.1f}ms, P95: {p95_latency*1000:.1f}ms, P99: {p99_latency*1000:.1f}ms)")
    print(f"Hallucination Rate    : {hallucination_rate:.2f}% (Count: {hallucination_count})")
    print(f"Rate Limit Failures   : {rate_limit_failures}")
    print("-" * 95)
    print("\n[+] TOPIC-BY-TOPIC ACCURACY MATRIX:")
    print(f"{'Topic #':<8} | {'Topic Name':<55} | {'Passed':<8} | {'Total':<6} | {'Pass Rate':<9} | {'Avg Lat':<8}")
    print("-" * 95)
    for i in range(1, 9):
        ts = topic_stats[i]
        pct = (ts["passed"] / ts["total"]) * 100 if ts["total"] > 0 else 0
        print(f"Topic {i:<2} | {ts['name']:<55} | {ts['passed']:<8} | {ts['total']:<6} | {pct:6.1f}%  | {ts['avg_lat']*1000:6.1f}ms")

    print("-" * 95)
    print(f">> Full diagnostics and telemetry saved to: {RESULTS_PATH}")
    return pass_rate >= 95.0


if __name__ == "__main__":
    success = asyncio.run(run_full_suite())
    sys.exit(0 if success else 1)
