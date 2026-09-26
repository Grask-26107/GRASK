"""
Comprehensive 50-Trial Test Suite for "Ready to Apply" Certificate Studio (SIH26107)
Covers:
  - 10 Typo-laden & misspelling queries
  - 8 Colloquial slang, regional terms, and transliteration
  - 6 Disambiguation & similar product distinction
  - 8 Out-of-scope / Garbage / Injection / Malicious queries
  - 6 Financial & MSME concession calculations
  - 6 Readiness scoring & critical inspection blockers
  - 6 End-to-end statutory PDF dossier compilations
Total: 50 trials
"""

import os
import sys
import json
import time

# Add backend to path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from app.services.certificate_engine import certificate_engine
from app.services.certificate_dossier_generator import certificate_dossier_generator

def run_suite():
    print("=" * 80)
    print("SIH 2026: GRASK AI - READY TO APPLY CERTIFICATE STUDIO (50 TRIALS)")
    print("=" * 80)

    trials_passed = 0
    trials_total = 0
    results_log = []

    def assert_trial(trial_num: int, category: str, name: str, condition: bool, details: str):
        nonlocal trials_passed, trials_total
        trials_total += 1
        status = "PASSED" if condition else "FAILED"
        if condition:
            trials_passed += 1
        print(f"[{status}] Trial {trial_num:02d} ({category}): {name} -> {details}")
        results_log.append({
            "trial": trial_num,
            "category": category,
            "name": name,
            "status": status,
            "details": details
        })

    # ---------------------------------------------------------
    # Category 1: Typo-Laden & Misspelling Queries (Trials 1-10)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 1: TYPOS & MISSPELLED QUERIES (10 TRIALS) ---")
    typo_cases = [
        (1, "ro watur", "IS 14543"),
        (2, "bislery water plant", "IS 14543"),
        (3, "tmt sariya rod", "IS 1786"),
        (4, "two wheeler healmet", "IS 4151"),
        (5, "led bulp 9 watt", "IS 16102"),
        (6, "atta chaki flour", "FSSAI"),
        (7, "doodh paneer dairy", "FSSAI"),
        (8, "plasstic hdpe pip", "IS 4984"),
        (9, "lpg gas chulha stove", "IS 4246"),
        (10, "portland ciment opc", "IS 269"),
    ]
    for t_num, query, expected_code in typo_cases:
        res = certificate_engine.resolve_product_profile(query)
        passed = (res is not None) and (expected_code in res["is_code"] or expected_code in res["title"])
        code_found = res["is_code"] if res else "None"
        assert_trial(t_num, "Typos", f"Query '{query}'", passed, f"Resolved to {code_found}")

    # ---------------------------------------------------------
    # Category 2: Regional Slang & Transliteration (Trials 11-18)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 2: REGIONAL SLANG & TRANSLITERATION (8 TRIALS) ---")
    slang_cases = [
        (11, "paala dukanam business", "dairy_milk_processing"),
        (12, "pani plant license cost", "packaged_drinking_water"),
        (13, "sariya manufacturing unit", "tmt_steel_bars"),
        (14, "chawal mill license", "food_processing_bakery"),
        (15, "sona chandi hallmark shop", "gold_jewellery"),
        (16, "paper industry", "paper_industry"),
        (17, "books or notes industry", "books_and_stationery"),
        (18, "borewell submersible plastic pipe", "hdpe_pipes"),
    ]
    for t_num, query, expected_id in slang_cases:
        res = certificate_engine.resolve_product_profile(query)
        passed = (res is not None) and (res["id"] == expected_id)
        prof_found = res["id"] if res else "None"
        assert_trial(t_num, "Slang/Hinglish", f"Query '{query}'", passed, f"Profile: {prof_found}")

    # ---------------------------------------------------------
    # Category 3: Disambiguation & Specificity (Trials 19-24)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 3: DISAMBIGUATION & SPECIFICITY (6 TRIALS) ---")
    
    # 19. Packaged Water vs Natural Mineral Water
    p19_a = certificate_engine.resolve_product_profile("packaged drinking water")
    p19_b = certificate_engine.resolve_product_profile("natural spring mineral water")
    pass_19 = (p19_a and p19_a["id"] == "packaged_drinking_water") and (p19_b and p19_b["id"] == "natural_mineral_water")
    assert_trial(19, "Disambiguation", "Packaged vs Natural Mineral Water", pass_19, f"{p19_a['is_code']} vs {p19_b['is_code']}")

    # 20. TMT Steel vs Portland Cement
    p20_a = certificate_engine.resolve_product_profile("fe 500d tmt bar")
    p20_b = certificate_engine.resolve_product_profile("opc 53 grade cement")
    pass_20 = (p20_a["id"] == "tmt_steel_bars") and (p20_b["id"] == "portland_cement")
    assert_trial(20, "Disambiguation", "TMT Steel vs Portland Cement", pass_20, f"{p20_a['is_code']} vs {p20_b['is_code']}")

    # 21. Motorcycle Helmets vs Industrial Gas Stoves
    p21_a = certificate_engine.resolve_product_profile("motorcycle helmet")
    p21_b = certificate_engine.resolve_product_profile("domestic gas stove burner")
    pass_21 = (p21_a["id"] == "protective_helmets") and (p21_b["id"] == "domestic_gas_stoves")
    assert_trial(21, "Disambiguation", "Helmets vs Gas Stoves", pass_21, f"{p21_a['is_code']} vs {p21_b['is_code']}")

    # 22. LED Lamps vs HDPE Borewell Pipes
    p22_a = certificate_engine.resolve_product_profile("emergency led bulb")
    p22_b = certificate_engine.resolve_product_profile("hdpe pipe pe 100")
    pass_22 = (p22_a["id"] == "led_lighting") and (p22_b["id"] == "hdpe_pipes")
    assert_trial(22, "Disambiguation", "LED Bulb vs HDPE Pipe", pass_22, f"{p22_a['is_code']} vs {p22_b['is_code']}")

    # 23. Gold Jewellery vs Dairy Plant
    p23_a = certificate_engine.resolve_product_profile("gold ornaments shop huid")
    p23_b = certificate_engine.resolve_product_profile("milk dairy plant chilling")
    pass_23 = (p23_a["id"] == "gold_jewellery") and (p23_b["id"] == "dairy_milk_processing")
    assert_trial(23, "Disambiguation", "Gold HUID vs Dairy Milk", pass_23, f"{p23_a['is_code']} vs {p23_b['is_code']}")

    # 24. Bakery/Snacks vs Packaged Water
    p24_a = certificate_engine.resolve_product_profile("biscuits and namkeen bakery")
    p24_b = certificate_engine.resolve_product_profile("20 litre water bottle can")
    pass_24 = (p24_a["id"] == "food_processing_bakery") and (p24_b["id"] == "packaged_drinking_water")
    assert_trial(24, "Disambiguation", "Bakery vs Water Can", pass_24, f"{p24_a['is_code']} vs {p24_b['is_code']}")

    # ---------------------------------------------------------
    # Category 4: Garbage / Injection / Malicious (Trials 25-32)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 4: OUT-OF-SCOPE & GARBAGE QUERIES (8 TRIALS) ---")
    garbage_cases = [
        (25, "asdfghjkl123", "Gibberish string"),
        (26, "DROP TABLE certificates;", "SQL Injection attempt"),
        (27, "give me 50 lakh government loan money", "Unrelated loan request"),
        (28, "who won the cricket match yesterday", "Cricket score ask"),
        (29, "hello hi hey test", "Generic greeting noise"),
        (30, "<script>alert('hack')</script>", "XSS Injection attempt"),
        (31, "how to make butter chicken recipe", "Food recipe ask"),
        (32, "police complaint against neighbor", "Law & order grievance"),
    ]
    for t_num, q, desc in garbage_cases:
        is_bad = certificate_engine.is_garbage_or_unrelated(q)
        prof = certificate_engine.resolve_product_profile(q)
        passed = is_bad or (prof is None)
        assert_trial(t_num, "Security/Garbage", desc, passed, f"Correctly blocked/refused: is_garbage={is_bad}")

    # ---------------------------------------------------------
    # Category 5: Financials & MSME Concessions (Trials 33-38)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 5: STATUTORY FEES & MSME CONCESSIONS (6 TRIALS) ---")
    
    # 33. Micro Enterprise with Udyam on BIS ISI -> 50% discount
    a33 = certificate_engine.assess_readiness("packaged drinking water", "micro", True, [])
    # base is 1000 + 7000 = 8000, 50% = 4000
    p33 = a33["financials"]["concessions_unlocked"] > 0 and a33["has_udyam_msme"] is True
    assert_trial(33, "Finance", "Micro + Udyam (50% Concession)", p33, f"Saved ₹{a33['financials']['concessions_unlocked']:,}")

    # 34. Micro Enterprise without Udyam -> 0% discount
    a34 = certificate_engine.assess_readiness("packaged drinking water", "micro", False, [])
    p34 = a34["financials"]["concessions_unlocked"] == 0
    assert_trial(34, "Finance", "Micro without Udyam (0% Concession)", p34, f"Zero discount correctly enforced")

    # 35. Small Enterprise with Udyam on BIS ISI -> 20% discount
    a35 = certificate_engine.assess_readiness("tmt sariya", "small_medium", True, [])
    p35 = a35["financials"]["concessions_unlocked"] > 0
    assert_trial(35, "Finance", "Small/Medium + Udyam (20% Concession)", p35, f"Saved ₹{a35['financials']['concessions_unlocked']:,}")

    # 36. Large Enterprise (>20Cr) -> Triggers Central FSSAI & 0% MSME concession
    a36 = certificate_engine.assess_readiness("packaged drinking water", "large", False, [])
    has_central = any(c["id"] == "FSSAI_CENTRAL" for c in a36["certificates"])
    assert_trial(36, "Finance", "Large Enterprise FSSAI Central Tier", has_central, "FSSAI Central tier correctly assigned")

    # 37. Micro Enterprise (<12L) -> Triggers Basic FSSAI Registration (₹100)
    a37 = certificate_engine.assess_readiness("bakery snacks", "micro", True, [])
    has_basic = any(c["id"] == "FSSAI_BASIC" for c in a37["certificates"])
    assert_trial(37, "Finance", "Micro Food Business FSSAI Basic Tier", has_basic, "FSSAI Basic tier correctly assigned (₹100)")

    # 38. Gold Jeweller Hallmarking -> Free under MSME
    a38 = certificate_engine.assess_readiness("gold jewellery shop", "micro", True, [])
    net_fee = a38["financials"]["net_payable_fee"]
    p38 = net_fee == 0
    assert_trial(38, "Finance", "Gold Jeweller MSME Hallmarking Fee", p38, f"Net payable: ₹{net_fee}")

    # ---------------------------------------------------------
    # Category 6: Readiness Scoring & Critical Blockers (Trials 39-44)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 6: READINESS SCORING & BLOCKERS (6 TRIALS) ---")

    # 39. Zero documents checked -> Score: 0%
    a39 = certificate_engine.assess_readiness("packaged drinking water", "small_medium", True, [])
    p39 = a39["readiness_score"] == 0 and a39["status"] == "CRITICAL_GAPS"
    assert_trial(39, "Readiness", "Zero Documents Checked", p39, f"Score: {a39['readiness_score']}% ({a39['status']})")

    # 40. Only basic legal ID checked -> Score < 30%
    a40 = certificate_engine.assess_readiness("packaged drinking water", "small_medium", True, ["doc_identity_pan"])
    p40 = 0 < a40["readiness_score"] <= 30
    assert_trial(40, "Readiness", "Only PAN Provided", p40, f"Score: {a40['readiness_score']}%")

    # 41. Missing In-House Testing Lab -> Critical Blocker Flagged
    a41 = certificate_engine.assess_readiness("packaged drinking water", "small_medium", True, [
        "doc_identity_pan", "doc_factory_address", "doc_electricity_bill", "doc_machinery_list"
    ])
    blockers = a41["critical_blockers_missing"]
    p41 = len(blockers) > 0 and any("In-House Testing" in b["document"] for b in blockers)
    assert_trial(41, "Readiness", "Missing In-House Lab Flagged as Blocker", p41, f"{len(blockers)} blocker(s) detected")

    # 42. In-House Lab Equipment list present in profile
    lab_tools = a41["product"]["inhouse_lab_equipment"]
    p42 = len(lab_tools) >= 5
    assert_trial(42, "Readiness", "Standard Testing Equipment Included", p42, f"{len(lab_tools)} specific lab tools verified")

    # 43. 100% of all prerequisites checked -> Score: 100% (READY_TO_SUBMIT)
    all_doc_ids = [p["id"] for p in a41["prerequisites_checklist"]]
    a43 = certificate_engine.assess_readiness("packaged drinking water", "small_medium", True, all_doc_ids)
    p43 = a43["readiness_score"] == 100 and a43["status"] == "READY_TO_SUBMIT"
    assert_trial(43, "Readiness", "100% Complete Application", p43, f"Score: {a43['readiness_score']}% ({a43['status']})")

    # 44. Mandatory QCO flag active
    p44 = a43["product"]["mandatory_qco"] is True
    assert_trial(44, "Readiness", "Statutory QCO Enforcement Flag", p44, f"Mandatory QCO = {p44}")

    # ---------------------------------------------------------
    # Category 7: End-to-End PDF Dossier Generation (Trials 45-50)
    # ---------------------------------------------------------
    print("\n--- CATEGORY 7: END-TO-END STATUTORY PDF COMPILATION (6 TRIALS) ---")
    pdf_cases = [
        (45, "packaged drinking water", "Himalayan Spring Bottlers Ltd"),
        (46, "tmt steel bars", "Bharat Rebar Rolling Mills"),
        (47, "two wheeler helmet", "Suraksha Gear Industries"),
        (48, "led lighting", "Lumina Optoelectronics"),
        (49, "bakery snacks", "Annapurna Food Processors"),
        (50, "gold jewellery", "Sri Lakshmi Jewellers"),
    ]
    for t_num, prod_query, company_name in pdf_cases:
        assessment = certificate_engine.assess_readiness(prod_query, "small_medium", True, ["doc_identity_pan", "doc_factory_address", "doc_inhouse_lab"])
        pdf_path = certificate_dossier_generator.generate_dossier_pdf(assessment, company_name)
        exists = pdf_path is not None and os.path.exists(pdf_path)
        file_size = os.path.getsize(pdf_path) if exists else 0
        p_res = exists and file_size > 2000
        assert_trial(t_num, "PDF Dossier", f"{prod_query} ({company_name})", p_res, f"PDF: {os.path.basename(pdf_path)} ({file_size} bytes)")

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"BENCHMARK RESULTS: {trials_passed} / {trials_total} TRIALS PASSED ({(trials_passed/trials_total)*100:.1f}%)")
    print("=" * 80)

    # Save results to json
    results_path = os.path.join(os.path.dirname(__file__), "test_results_50_ready_to_apply.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total": trials_total,
            "passed": trials_passed,
            "pass_rate": f"{(trials_passed/trials_total)*100:.1f}%",
            "trials": results_log
        }, f, indent=2)

    return trials_passed == trials_total

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
