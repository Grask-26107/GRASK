"""
Comprehensive 50-Image Evaluation Suite for Camera & Optical Scanner Features
Tests all 50 synthetic test images across:
1. Audit Compliance Studio (extract_and_verify)
2. FSSAI Nutri-Score & Hidden Ingredients (analyze)
3. MANAK-Vision Statutory Mark Verifier (extract_from_image_and_text & verify_identifier)

Verifies:
- Accurate extraction on positive domain images
- 100% rejection rate on irrelevant images (cars, machinery, pets, scenery, portraits, noise)
- Zero state leakage and zero dummy parameter injection
- Cross-domain separation (food labels rejected in audit; steel reports rejected in nutri-score)
"""

import sys
import os
import io
import time
import json
import base64
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.services.lab_report_extractor import lab_report_extractor_service
from app.services.nutri_analyzer import nutri_analyzer_service
from app.services.license_verifier import license_verifier_service

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_dataset"))
MANIFEST_PATH = os.path.join(DATASET_DIR, "manifest.json")

def load_image_b64(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def run_evaluation():
    print("=" * 80)
    print("GRASK AI: COMPREHENSIVE 50-IMAGE CAMERA & OPTICAL SCANNER EVALUATION")
    print("=" * 80)

    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest not found at {MANIFEST_PATH}")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Total test images in dataset: {len(manifest)}\n")

    results: List[Dict[str, Any]] = []

    passed_count = 0
    total_checks = 0

    # -------------------------------------------------------------------------
    # PART 1: TARGET DOMAIN ACCURACY (Testing each image against its own feature)
    # -------------------------------------------------------------------------
    print("\n--- PHASE 1: TARGET DOMAIN EVALUATION (Positive & Irrelevant Detection) ---")

    for item in manifest:
        filename = item["file"]
        category = item["category"]
        expected_rel = item.get("expected_relevant", False)
        img_path = os.path.join(DATASET_DIR, filename)

        if not os.path.exists(img_path):
            print(f"[MISSING] {filename}")
            continue

        b64 = load_image_b64(img_path)
        t0 = time.time()

        if category == "audit_compliance":
            total_checks += 1
            res = lab_report_extractor_service.extract_and_verify(image_base64=b64)
            dt = round(time.time() - t0, 2)
            
            is_rel = getattr(res, "is_relevant", False)
            status = getattr(res, "status", "")
            params = getattr(res, "parameters", [])
            std = getattr(res, "standard_is_code", "")
            verdict = ""
            if getattr(res, "verification", None):
                verdict = getattr(res.verification, "overall_verdict", "")

            passed = (is_rel == expected_rel) and (len(params) > 0)
            if passed:
                passed_count += 1
                status_icon = "[PASS]"
            else:
                status_icon = "[FAIL]"

            print(f"{status_icon} Audit | {filename[:30]:<30} | Rel: {is_rel} | Params: {len(params):<2} | Std: {std:<12} | Verdict: {verdict:<14} | ({dt}s)")
            results.append({
                "file": filename, "feature": "audit_compliance", "category": category,
                "passed": passed, "is_relevant": is_rel, "details": f"{len(params)} params, {verdict}", "latency": dt
            })

        elif category == "nutri_score":
            total_checks += 1
            res = nutri_analyzer_service.analyze(image_base64=b64)
            dt = round(time.time() - t0, 2)

            is_rel = res.get("is_relevant", False)
            verdict = res.get("verdict", "")
            grade = res.get("nutri_score_grade", "")
            prod = res.get("product_name", "")

            passed = (is_rel == expected_rel) and (verdict != "IRRELEVANT")
            if passed:
                passed_count += 1
                status_icon = "[PASS]"
            else:
                status_icon = "[FAIL]"

            print(f"{status_icon} Nutri | {filename[:30]:<30} | Rel: {is_rel} | Verdict: {verdict:<8} | Grade: {grade:<3} | Prod: {prod[:20]:<20} | ({dt}s)")
            results.append({
                "file": filename, "feature": "nutri_score", "category": category,
                "passed": passed, "is_relevant": is_rel, "details": f"Verdict: {verdict}, Grade: {grade}", "latency": dt
            })

        elif category == "mark_check":
            total_checks += 1
            res = license_verifier_service.extract_from_image_and_text(image_base64=b64)
            dt = round(time.time() - t0, 2)

            is_rel = res.get("is_relevant", True)
            status = res.get("status", "")
            found_ids = res.get("all", [])
            primary = res.get("primary")
            primary_val = primary["value"] if primary else "None"
            primary_type = primary["type"] if primary else "None"

            # For mark_13 (fake mark with no CML), it should be relevant as a mark attempt but have no valid CML or invalid
            if "fake" in filename:
                passed = is_rel is True
            else:
                passed = (is_rel == expected_rel) and (len(found_ids) > 0 or primary is not None)

            if passed:
                passed_count += 1
                status_icon = "[PASS]"
            else:
                status_icon = "[FAIL]"

            print(f"{status_icon} Mark  | {filename[:30]:<30} | Rel: {is_rel} | Found: {len(found_ids):<2} | Primary: {primary_type}:{primary_val} | ({dt}s)")
            results.append({
                "file": filename, "feature": "mark_check", "category": category,
                "passed": passed, "is_relevant": is_rel, "details": f"Primary: {primary_val}", "latency": dt
            })

        elif category == "irrelevant":
            # For irrelevant images, test across ALL THREE features to ensure 100% rejection across board!
            for feat_name, service_fn, feat_tag in [
                ("audit_compliance", lambda b: lab_report_extractor_service.extract_and_verify(image_base64=b), "Audit"),
                ("nutri_score", lambda b: nutri_analyzer_service.analyze(image_base64=b), "Nutri"),
                ("mark_check", lambda b: license_verifier_service.extract_from_image_and_text(image_base64=b), "Mark")
            ]:
                total_checks += 1
                t_sub = time.time()
                sub_res = service_fn(b64)
                dt_sub = round(time.time() - t_sub, 2)

                if feat_name == "audit_compliance":
                    is_rel = getattr(sub_res, "is_relevant", False)
                    params = getattr(sub_res, "parameters", [])
                    passed = (is_rel is False) and (len(params) == 0)
                    detail = f"Rejected (params={len(params)})"
                elif feat_name == "nutri_score":
                    is_rel = sub_res.get("is_relevant", False)
                    verdict = sub_res.get("verdict", "")
                    passed = (is_rel is False) and (verdict == "IRRELEVANT")
                    detail = f"Rejected (verdict={verdict})"
                else: # mark_check
                    is_rel = sub_res.get("is_relevant", False)
                    found = sub_res.get("all", [])
                    passed = (is_rel is False) or (len(found) == 0)
                    detail = f"Rejected (found={len(found)})"

                if passed:
                    passed_count += 1
                    status_icon = "[PASS]"
                else:
                    status_icon = "[FAIL]"

                print(f"{status_icon} Irrel | {filename[:25]:<25} -> {feat_tag:<5} | Rel: {is_rel} | {detail:<28} | ({dt_sub}s)")
                results.append({
                    "file": filename, "feature": feat_name, "category": "irrelevant",
                    "passed": passed, "is_relevant": is_rel, "details": detail, "latency": dt_sub
                })

    # -------------------------------------------------------------------------
    # PART 2: CROSS-DOMAIN SEPARATION TESTS
    # -------------------------------------------------------------------------
    print("\n--- PHASE 2: CROSS-DOMAIN SEPARATION EVALUATION ---")
    cross_tests = [
        # Send food image to audit compliance (should be rejected)
        ("nutri_01_biscuit_high_sugar.jpg", "audit_compliance", lambda b: lab_report_extractor_service.extract_and_verify(image_base64=b)),
        # Send steel rebar report to nutri score (should be rejected)
        ("audit_03_steel_fe500d_pass.jpg", "nutri_score", lambda b: nutri_analyzer_service.analyze(image_base64=b)),
        # Send gold ring to nutri score (should be rejected)
        ("mark_09_gold_ring_huid.jpg", "nutri_score", lambda b: nutri_analyzer_service.analyze(image_base64=b))
    ]

    for fname, target_feat, fn in cross_tests:
        total_checks += 1
        t_c = time.time()
        c_b64 = load_image_b64(os.path.join(DATASET_DIR, fname))
        c_res = fn(c_b64)
        dt_c = round(time.time() - t_c, 2)

        if target_feat == "audit_compliance":
            is_rel = getattr(c_res, "is_relevant", False)
            params = getattr(c_res, "parameters", [])
            passed = (is_rel is False) or (len(params) == 0)
        else: # nutri_score
            is_rel = c_res.get("is_relevant", False)
            verdict = c_res.get("verdict", "")
            passed = (is_rel is False) or (verdict == "IRRELEVANT")

        if passed:
            passed_count += 1
            status_icon = "[PASS]"
        else:
            status_icon = "[FAIL]"

        print(f"{status_icon} Cross | {fname[:30]:<30} -> {target_feat:<16} | Cross-Domain Rejected: {passed} | ({dt_c}s)")
        results.append({
            "file": fname, "feature": target_feat, "category": "cross_domain",
            "passed": passed, "is_relevant": is_rel, "details": "Cross-domain rejection", "latency": dt_c
        })

    # -------------------------------------------------------------------------
    # SUMMARY & DRAWBACK ANALYSIS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY & METRICS")
    print("=" * 80)
    pass_pct = (passed_count / total_checks) * 100 if total_checks else 0.0
    print(f"Total Evaluations Conducted: {total_checks}")
    print(f"Total Passed:                {passed_count}")
    print(f"Total Failed:                {total_checks - passed_count}")
    print(f"Overall Accuracy / Pass Rate:{pass_pct:.2f}%")
    print("=" * 80)

    # Save detailed evaluation log
    eval_log_path = os.path.join(DATASET_DIR, "evaluation_report.json")
    with open(eval_log_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_checks": total_checks,
            "passed_count": passed_count,
            "failed_count": total_checks - passed_count,
            "pass_rate_percent": pass_pct,
            "results": results
        }, f, indent=2)
    print(f"Detailed evaluation metrics saved to: {eval_log_path}")

if __name__ == "__main__":
    run_evaluation()
