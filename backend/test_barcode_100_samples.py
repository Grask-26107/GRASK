import sys
import io
import re
import time
from typing import Dict, Any, List

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.license_verifier import license_verifier_service, LicenseVerifierService, GENUINE_BARCODE_REGISTRY, GS1_PREFIX_DIRECTORY

# -------------------------------------------------------------------------------------
# 100 ORIGINAL & REALISTIC PACKAGING SAMPLES FOR HARDENED VERIFICATION
# -------------------------------------------------------------------------------------
# Each sample represents raw optical OCR text or scanner input from physical packaging:
# Format: (sample_text, expected_type, expected_id, test_category)
# -------------------------------------------------------------------------------------

SAMPLES_100: List[tuple] = [
    # ---------------------------------------------------------------------------
    # CATEGORY 1: Direct 13-Digit GS1 EAN-13 Barcodes (15 samples)
    # ---------------------------------------------------------------------------
    ("8901751022162", "barcode", "8901751022162", "GS1 EAN-13 Direct"),
    ("8902519001979", "barcode", "8902519001979", "GS1 EAN-13 Direct"),
    ("8904327600849", "barcode", "8904327600849", "GS1 EAN-13 Direct"),
    ("8901491101844", "barcode", "8901491101844", "GS1 EAN-13 Direct"),
    ("8905650102321", "barcode", "8905650102321", "GS1 EAN-13 Direct"),
    ("8901860010159", "barcode", "8901860010159", "GS1 EAN-13 Direct"),
    ("8906002005017", "barcode", "8906002005017", "GS1 EAN-13 Direct"),
    ("8901058000108", "barcode", "8901058000108", "GS1 EAN-13 Direct"),
    ("8901030010026", "barcode", "8901030010026", "GS1 EAN-13 Direct"),
    ("8901207040528", "barcode", "8901207040528", "GS1 EAN-13 Direct"),
    ("8901262010016", "barcode", "8901262010016", "GS1 EAN-13 Direct"),
    ("8901138500207", "barcode", "8901138500207", "GS1 EAN-13 Direct"),
    ("8901233014029", "barcode", "8901233014029", "GS1 EAN-13 Direct"),
    ("8901725131012", "barcode", "8901725131012", "GS1 EAN-13 Direct"),
    ("8901063012011", "barcode", "8901063012011", "GS1 EAN-13 Direct"),

    # ---------------------------------------------------------------------------
    # CATEGORY 2: Barcodes with Guard-Bar Noise (Tesseract extra '1's) (15 samples)
    # ---------------------------------------------------------------------------
    ("819017511022162", "barcode", "8901751022162", "Guard Bar Noise (Start/Center 1s)"),
    ("89017510221621", "barcode", "8901751022162", "Guard Bar Noise (Trailing 1)"),
    ("18901751022162", "barcode", "8901751022162", "Guard Bar Noise (Leading 1)"),
    ("819025191001979", "barcode", "8902519001979", "Guard Bar Noise (Classmate)"),
    ("89025190019791", "barcode", "8902519001979", "Guard Bar Noise (Classmate Trail)"),
    ("819043271600849", "barcode", "8904327600849", "Guard Bar Noise (MyFitness)"),
    ("89043276008491", "barcode", "8904327600849", "Guard Bar Noise (MyFitness Trail)"),
    ("819014911101844", "barcode", "8901491101844", "Guard Bar Noise (Lays)"),
    ("89014911018441", "barcode", "8901491101844", "Guard Bar Noise (Lays Trail)"),
    ("819056501102321", "barcode", "8905650102321", "Guard Bar Noise (boAt)"),
    ("89056501023211", "barcode", "8905650102321", "Guard Bar Noise (boAt Trail)"),
    ("819018601010159", "barcode", "8901860010159", "Guard Bar Noise (Fevicol)"),
    ("89010580001081", "barcode", "8901058000108", "Guard Bar Noise (Maggi)"),
    ("819012071040528", "barcode", "8901207040528", "Guard Bar Noise (Sunfeast)"),
    ("89011385002071", "barcode", "8901138500207", "Guard Bar Noise (Britannia)"),

    # ---------------------------------------------------------------------------
    # CATEGORY 3: Barcodes with Spaced/Hyphenated OCR Output (10 samples)
    # ---------------------------------------------------------------------------
    ("8 901751 022162", "barcode", "8901751022162", "Spaced EAN-13"),
    ("8 902519 001979", "barcode", "8902519001979", "Spaced EAN-13"),
    ("8 904327 600849", "barcode", "8904327600849", "Spaced EAN-13"),
    ("8-901491-101844", "barcode", "8901491101844", "Hyphenated EAN-13"),
    ("8 905650 102321", "barcode", "8905650102321", "Spaced EAN-13"),
    ("8 901860 010159", "barcode", "8901860010159", "Spaced EAN-13"),
    ("8 906002 005017", "barcode", "8906002005017", "Spaced EAN-13"),
    ("8 901058 000108", "barcode", "8901058000108", "Spaced EAN-13"),
    ("8 901030 010026", "barcode", "8901030010026", "Spaced EAN-13"),
    ("8 901207 040528", "barcode", "8901207040528", "Spaced EAN-13"),

    # ---------------------------------------------------------------------------
    # CATEGORY 4: Packaging with Batch No, Date & Barcode (Reject Batch) (15 samples)
    # ---------------------------------------------------------------------------
    ("BATCH NO: B2024 / PKG 08/24 / MRP RS 45.00 / 8901751022162", "barcode", "8901751022162", "Packaging with Batch & Date"),
    ("CLASSMATE LONG NOTEBOOK\nBATCH NO. B409218\nBARCODE: 8902519001979\nMRP Rs. 65.00", "barcode", "8902519001979", "Classmate Label with Batch"),
    ("MYFITNESS PEANUT BUTTER\nLOT NO: 9948201\nEXP: 02/2026\n8 904327 600849", "barcode", "8904327600849", "MyFitness with Lot No"),
    ("LAYS CLASSIC SALTED\nB.NO: 4910281\nMFG DATE: 12/2024\n8901491101844", "barcode", "8901491101844", "Lays with B.No"),
    ("BOAT AIRDOPES 141\nSERIAL NO: BT202409\nBATCH: 89104\n8905650102321", "barcode", "8905650102321", "boAt with Batch & Serial"),
    ("FEVISTIK SUPER GLUE\nBATCH NO. 7840192\nNET QTY: 15g\n8901860010159", "barcode", "8901860010159", "Fevistik with Batch"),
    ("SNICKERS BARS\nLOT: SN202488\nEXPIRY: 10/2025\n8906002005017", "barcode", "8906002005017", "Snickers with Lot"),
    ("MAGGI 2-MINUTE NOODLES\nBATCH NO: M8901\nMRP: 14.00\n8901058000108", "barcode", "8901058000108", "Maggi with Batch"),
    ("DOVE MOISTURE SHAMPOO\nB.NO. 8492019\nUSE BEFORE: 2027\n8901030010026", "barcode", "8901030010026", "Dove with B.No"),
    ("SUNFEAST DARK FANTASY\nBATCH NO. SF2049\n8901207040528", "barcode", "8901207040528", "Sunfeast with Batch"),
    ("PARACHUTE 100% PURE COCONUT OIL\nBATCH NO: PC4920\n8901262010016", "barcode", "8901262010016", "Parachute with Batch"),
    ("BRITANNIA GOOD DAY BUTTER\nLOT NO: GD84921\n8901138500207", "barcode", "8901138500207", "Britannia with Lot"),
    ("DABUR HONEY 100% PURE\nB.NO: DH10492\n8901233014029", "barcode", "8901233014029", "Dabur with B.No"),
    ("PARLE-G ORIGINAL GLUCOSE\nBATCH: PG8901\n8901725131012", "barcode", "8901725131012", "Parle-G with Batch"),
    ("GOOD KNIGHT POWER ACTIV+\nBATCH: GK89201\n8901063012011", "barcode", "8901063012011", "Good Knight with Batch"),

    # ---------------------------------------------------------------------------
    # CATEGORY 5: 14-Digit FSSAI Food Licenses (15 samples)
    # ---------------------------------------------------------------------------
    ("10012011000123", "fssai", "10012011000123", "FSSAI Central Direct"),
    ("10014047000100", "fssai", "10014047000100", "FSSAI Central Direct"),
    ("10012064000034", "fssai", "10012064000034", "FSSAI Central Direct"),
    ("10012022000258", "fssai", "10012022000258", "FSSAI Central Direct"),
    ("20819003000456", "fssai", "20819003000456", "FSSAI State Direct"),
    ("22718001000789", "fssai", "22718001000789", "FSSAI State Direct"),
    ("fssai lic no: 10012011000123", "fssai", "10012011000123", "FSSAI with Prefix"),
    ("FSSAI Lic. No. 10014047000100", "fssai", "10014047000100", "FSSAI with Punctuation"),
    ("Lic No: 100 120 640 000 34", "fssai", "10012064000034", "FSSAI with Spaces"),
    ("fssai 100-120-2200-0258", "fssai", "10012022000258", "FSSAI with Hyphens"),
    ("FSSAI: 20819003000456 / BATCH 89401", "fssai", "20819003000456", "FSSAI with Batch"),
    ("fssai lic: 22718001000789 / EXP 2026", "fssai", "22718001000789", "FSSAI with Expiry"),
    ("FOOD SAFETY LIC 10012011000123", "fssai", "10012011000123", "FSSAI Header"),
    ("FSSAI REGISTRATION: 10014047000100", "fssai", "10014047000100", "FSSAI Registration Header"),
    ("FSSAI 10012064000034 NET WT 500g", "fssai", "10012064000034", "FSSAI with Net Weight"),

    # ---------------------------------------------------------------------------
    # CATEGORY 6: BIS ISI Mark CM/L Numbers (7, 8, 10 digits) (15 samples)
    # ---------------------------------------------------------------------------
    ("CM/L-8400152488", "cml", "8400152488", "CM/L 10-digit Bisleri"),
    ("CM/L-8400123", "cml", "8400123", "CM/L 7-digit Aquafina"),
    ("CM/L-6200084512", "cml", "6200084512", "CM/L 10-digit Tata Tiscon"),
    ("CM/L-6200112", "cml", "6200112", "CM/L 7-digit JSW Steel"),
    ("CM/L-8800045210", "cml", "8800045210", "CM/L 10-digit Vega Helmet"),
    ("CM/L-8800145", "cml", "8800145", "CM/L 7-digit Steelbird"),
    ("CM/L 5100129", "cml", "5100129", "CM/L with Space"),
    ("CML-8400152488", "cml", "8400152488", "CM/L without slash"),
    ("IS 14543\nCM/L-8400123\nPACKAGED WATER", "cml", "8400123", "CM/L with Standard"),
    ("IS 1786\nCM/L 6200084512\nFE 500D", "cml", "6200084512", "CM/L with TMT Rebar"),
    ("IS 4151\nCM/L-8800045210\nHELMET", "cml", "8800045210", "CM/L with Helmet Standard"),
    ("cm/l: 8800145", "cml", "8800145", "CM/L lowercase colon"),
    ("CM/L - 8400152488", "cml", "8400152488", "CM/L spaced hyphen"),
    ("ISI MARK CM/L-6200112", "cml", "6200112", "ISI Mark CM/L"),
    ("CM/L 5100129 ULTRA CEMENT", "cml", "5100129", "CM/L Cement"),

    # ---------------------------------------------------------------------------
    # CATEGORY 7: Electronics BIS CRS R-Numbers (8 digits) (10 samples)
    # ---------------------------------------------------------------------------
    ("R-41292958", "crs", "R-41292958", "CRS Direct"),
    ("R-41000123", "crs", "R-41000123", "CRS Direct"),
    ("R-41012345", "crs", "R-41012345", "CRS Direct"),
    ("R-41154321", "crs", "R-41154321", "CRS Direct"),
    ("R-41029384", "crs", "R-41029384", "CRS Direct"),
    ("R 41292958", "crs", "R-41292958", "CRS with Space"),
    ("R: 41000123", "crs", "R-41000123", "CRS with Colon"),
    ("BIS CRS: R-41012345 / POWER BANK", "crs", "R-41012345", "CRS with Label"),
    ("R-41154321 / INPUT 100-240V", "crs", "R-41154321", "CRS with Voltage"),
    ("REGISTRATION NO: R-41029384", "crs", "R-41029384", "CRS with Registration"),

    # ---------------------------------------------------------------------------
    # CATEGORY 8: Gold Jewellery HUID (6 alphanumeric) (5 samples)
    # ---------------------------------------------------------------------------
    ("AH78K2", "huid", "AH78K2", "Gold HUID 22K"),
    ("KP49M1", "huid", "KP49M1", "Gold HUID 18K"),
    ("RT82B9", "huid", "RT82B9", "Gold HUID 20K"),
    ("MN34X8", "huid", "MN34X8", "Gold HUID 14K"),
    ("HUID: AH78K2 (HALLMARKED GOLD)", "huid", "AH78K2", "Gold HUID with Text"),
]

def run_100_sample_battery():
    print(f"=" * 90)
    print(f"🚀 RUNNING 100-SAMPLE RIGOROUS VERIFICATION BATTERY ACROSS ALL PRODUCT CATEGORIES")
    print(f"=" * 90)

    total = len(SAMPLES_100)
    passed = 0
    failed = 0
    start_time = time.time()

    for idx, (raw_input, exp_type, exp_id, cat_name) in enumerate(SAMPLES_100, 1):
        # 1. Optical Extraction
        extracted = license_verifier_service.extract_identifiers_from_text(raw_input)
        primary = extracted.get("primary")

        if not primary:
            print(f"❌ [Sample {idx:02d}/100] FAILED: No identifier extracted from '{raw_input}' ({cat_name})")
            failed += 1
            continue

        detected_type = primary.get("type")
        detected_val = primary.get("value")

        # Strip prefixes for comparison
        clean_exp = exp_id.replace("CM/L-", "")
        clean_det = detected_val.replace("CM/L-", "")

        match_ok = (detected_type == exp_type and clean_det == clean_exp)

        # 2. Statutory Verification Engine
        verif = license_verifier_service.verify_identifier(
            identifier=detected_val,
            query_type=detected_type
        )

        valid_ok = verif.get("is_valid", False)
        brand_ok = bool(verif.get("brand_name") or verif.get("brand"))
        parent_comp_ok = bool(verif.get("parent_company"))
        comp_name_ok = bool(verif.get("company_name") or verif.get("company"))
        prod_name_ok = bool(verif.get("product_name"))
        prod_type_ok = bool(verif.get("product_type"))
        structure_ok = bool(verif.get("structure_breakdown"))

        all_fields_ok = (match_ok and valid_ok and brand_ok and parent_comp_ok and 
                         comp_name_ok and prod_name_ok and prod_type_ok and structure_ok)

        if all_fields_ok:
            passed += 1
            brand_str = verif.get('brand_name') or verif.get('brand', 'Verified Brand')
            parent_str = verif.get('parent_company', 'N/A')
            prod_str = verif.get('product_name', 'N/A')
            type_str = verif.get('product_type', 'N/A')
            print(f"✅ [Sample {idx:02d}/100] PASS | {cat_name:<28} | Code: {detected_val:<15} | Brand: {brand_str[:18]:<18} | Parent: {parent_str[:20]:<20} | Type: {type_str[:22]}")
        else:
            failed += 1
            print(f"❌ [Sample {idx:02d}/100] FAILED | {cat_name} | Match: {match_ok}, Valid: {valid_ok}, Brand: {brand_ok}, ParentComp: {parent_comp_ok}, CompName: {comp_name_ok}, ProdName: {prod_name_ok}, ProdType: {prod_type_ok}")

    elapsed = time.time() - start_time
    print(f"=" * 90)
    print(f"📊 100-SAMPLE RIGOROUS TEST REPORT:")
    print(f"   Total Tested Samples: {total}")
    print(f"   Passed:               {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"   Failed:               {failed}/{total}")
    print(f"   Execution Time:       {elapsed:.2f} seconds ({elapsed/total*1000:.2f} ms/sample)")
    print(f"=" * 90)

    # 100-Cycle Endurance Stress Test (100 x 100 = 10,000 total evaluations)
    print(f"\n🔄 EXECUTING 100-CYCLE ENDURANCE STRESS TEST (10,000 Evaluations)...")
    stress_start = time.time()
    cycle_errors = 0
    total_stress_evals = 100 * total

    for cycle in range(100):
        for raw_input, exp_type, exp_id, cat_name in SAMPLES_100:
            ext = license_verifier_service.extract_identifiers_from_text(raw_input)
            prim = ext.get("primary")
            if not prim:
                cycle_errors += 1
                continue
            res = license_verifier_service.verify_identifier(prim["value"], prim["type"])
            if not res.get("is_valid") or not res.get("parent_company") or not res.get("product_type"):
                cycle_errors += 1

    stress_elapsed = time.time() - stress_start
    print(f"🏁 100-Cycle Stress Test Finished in {stress_elapsed:.2f} seconds!")
    print(f"   Total Stress Queries: {total_stress_evals}")
    print(f"   Errors Encountered:   {cycle_errors}")
    print(f"   Throughput:           {total_stress_evals / stress_elapsed:.0f} verifications/second")
    print(f"=" * 90)

    if passed == total and cycle_errors == 0:
        print(f"🎉 ALL CHECKS PASSED: 100% SUCCESSFUL TEST CONFORMANCE & 0 STRESS ERRORS across all 5 statutory identity fields!")
    else:
        print(f"⚠️ Test completed with issues: {failed} single-sample failures, {cycle_errors} stress errors.")

if __name__ == "__main__":
    run_100_sample_battery()
