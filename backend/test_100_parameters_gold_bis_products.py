import sys
import io
import asyncio
import time
from typing import List, Tuple, Dict, Any

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.rag_engine import rag_engine
from app.models.schemas import ChatMode

# -------------------------------------------------------------------------------------
# 100 BRAND NEW, PREVIOUSLY UNTESTED PARAMETERS: GOLD, BIS, PRODUCTS & DOUBTS
# -------------------------------------------------------------------------------------
# Format: (query_text, mode, category)
# -------------------------------------------------------------------------------------
TEST_100_PARAMETERS: List[Tuple[str, ChatMode, str]] = [
    # -------------------------------------------------------------
    # QUADRANT 1: GOLD & HALLMARKING (25 Parameters)
    # -------------------------------------------------------------
    ("6-digit HUID verification on BIS Care app", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("difference between 22K916 and 18K750 hallmarked gold", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("statutory hallmarking fee per gold jewellery article", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("is hallmarking mandatory for 24 karat gold bullion and coins", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("how to check registration of Assaying and Hallmarking Centre AHC", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("what to do if jeweller refuses to provide bill with 6 digit HUID", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("penalties for selling un-hallmarked gold under BIS Act 2016", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("can a consumer get their existing old gold jewellery hallmarked", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("where can a common citizen test purity of gold jewellery at BIS lab", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("consumer compensation formula if gold purity is found lower than marked karatage", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("is 14 karat gold eligible for BIS hallmarking", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("mandatory hallmarking districts phase 1 to 4 implementation in India", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("laser marking specifications and dimensions for 6 character HUID on rings", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("silver hallmarking purity grades under IS 2112 999 970 925", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("role of XRF X-ray fluorescence spectrometry in non-destructive gold assaying", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("fire assay cupellation test method for gold under IS 1418", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("exemptions from mandatory gold hallmarking for artisans under 40 lakh turnover", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("export and international exhibition gold hallmarking exemptions", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("difference between BIS logo, karatage mark, and HUID code on jewellery", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("how to verify jeweller certificate of registration on Manakonline", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("is hallmarking mandatory for gold watches and fountain pens", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("how to report fake hallmark laser engraving on National Consumer Helpline 1915", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("can gold jewellery have mixed karats in soldering alloys under IS 1417", ChatMode.INDUSTRY, "Gold & Hallmarking"),
    ("how to calculate exact gold value using 916 purity and live MCX gold rate", ChatMode.CONSUMER, "Gold & Hallmarking"),
    ("statutory records and registers required to be maintained by certified jewellers", ChatMode.INDUSTRY, "Gold & Hallmarking"),

    # -------------------------------------------------------------
    # QUADRANT 2: BIS SCHEMES & STATUTORY GOVERNANCE (25 Parameters)
    # -------------------------------------------------------------
    ("difference between Scheme-I ISI Mark and Scheme-II CRS registration", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("Foreign Manufacturers Certification Scheme FMCS eligibility and factory audit", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("Eco-mark scheme criteria for environmentally friendly products under BIS", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("Scheme-IV Certificate of Conformity for batch-wise industrial inspection", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("how to apply for BIS license on official Manakonline portal step by step", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("50 percent testing fee concession for MSMEs and DPIIT startups under BIS", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("mandatory Quality Control Orders QCO issued by DPIIT and Ministry of Steel", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("how to check operative vs expired CM/L licenses on Manakonline directory", ChatMode.CONSUMER, "BIS Statutory Schemes"),
    ("Laboratory Recognition Scheme LRS 2020 criteria for private testing labs", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("National Institute of Training for Standardization NITS courses and fee schedule", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("Standards Clubs in schools and colleges financial grant of 10000 rupees", ChatMode.CONSUMER, "BIS Statutory Schemes"),
    ("BIS Act 2016 Section 14 power to prohibit manufacture without Standard Mark", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("BIS Act 2016 Section 29 search seizure and compounding of offenses", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("validity period and renewal procedure for BIS Scheme-I license", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("surveillance audits and market sample drawing protocol by BIS officers", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("in-house testing laboratory requirements for factory grant of license", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("role of NABL accreditation ISO IEC 17025 in BIS third party test reports", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("how to become a BIS certified auditor or technical expert", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("BIS division councils matrix and 17 technical standardization departments", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("how Indian Standards IS codes are formulated through sectional committees", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("harmonization of Indian Standards with ISO and IEC international standards", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("consequences of misuse of ISI mark by unauthorized factories", ChatMode.CONSUMER, "BIS Statutory Schemes"),
    ("how to obtain duplicate BIS license certificate on Manakonline", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("statutory marking fee structure based on annual production turnover", ChatMode.INDUSTRY, "BIS Statutory Schemes"),
    ("public consultation and draft standard commenting process on BIS portal", ChatMode.INDUSTRY, "BIS Statutory Schemes"),

    # -------------------------------------------------------------
    # QUADRANT 3: PRODUCTS ACROSS DIVERSE SECTORS (25 Parameters)
    # -------------------------------------------------------------
    ("packaged natural mineral water requirements under IS 13428", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("structural steel for general construction requirements under IS 2062", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("Portland Pozzolana Cement PPC specifications under IS 1489 Part 1", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("safety requirements for electric immersion water heaters under IS 302 Part 2", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("energy efficiency star rating and safety for frost free refrigerators under IS 17550", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("safety of electric ceiling fans and regulators under IS 374", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("self-ballasted LED lamps for general lighting services under IS 16102 Part 1", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("PVC insulated electric cables for working voltages up to 1100V under IS 694", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("plugs and socket outlets for domestic and similar purposes under IS 1293", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("safety of toys mechanical and physical properties under IS 9873 Part 1", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("safety of toys flammability requirements under IS 9873 Part 2", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("crystalline silicon terrestrial photovoltaic solar PV modules under IS 14286", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("secondary lithium cells and batteries for portable applications under IS 16046", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("LPG cylinders for domestic use specifications under IS 3196 Part 1", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("low pressure regulators for domestic LPG cylinders under IS 9798", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("domestic pressure cookers safety and burst pressure test under IS 2347", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("infant milk food specifications and protein requirements under IS 14433", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("baby skin care oil specifications and acid value under IS 7123", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("skin creams and fairness lotions requirements under IS 6608", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("toilet soap specifications and Total Fatty Matter TFM grades under IS 2888", ChatMode.CONSUMER, "Products & Technical Standards"),
    ("portable fire extinguishers water and foam type specifications under IS 15683", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("unplasticized PVC pipes for potable water supplies under IS 4985", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("galvanized steel sheets plain and corrugated under IS 277", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("aluminium and aluminium alloy foil for pharmaceutical packaging under IS 15392", ChatMode.INDUSTRY, "Products & Technical Standards"),
    ("protective footwear for industrial workers specifications under IS 15298", ChatMode.INDUSTRY, "Products & Technical Standards"),

    # -------------------------------------------------------------
    # QUADRANT 4: CONSUMER DOUBTS & GRIEVANCES (25 Parameters)
    # -------------------------------------------------------------
    ("how to verify whether an ISI logo on an electrical appliance is genuine or fake", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("why an ISI mark without a 7 or 8 digit CM/L number is illegal and counterfeit", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to download and use the official BIS Care mobile app on Android and iOS", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to file a consumer complaint against substandard cement or steel on BIS Care app", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("consumer redressal timeline and tracking complaint status on Manakonline", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("National Consumer Helpline 1915 integration for defective certified products", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("what compensation can a consumer claim under Section 16 for injury caused by fake ISI goods", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to identify genuine GS1 India barcode prefix 890 vs counterfeit barcode stickers", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("does a barcode starting with 890 guarantee that the product was manufactured in India", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to search for a genuine manufacturer using company name on BIS website", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("what to do if packaged drinking water bottle has broken tamper evident seal", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("is selling loose unbranded cooking oil prohibited under statutory regulations", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to verify FSSAI 14 digit license number validity on FoSCoS portal", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("what mandatory declarations must appear on prepackaged commodities under Legal Metrology", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("can a shopkeeper charge more than the Maximum Retail Price MRP printed on the box", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to report dual MRP charging at airports, railway stations, and multiplexes", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("difference between voluntary standards and mandatory Quality Control Orders QCO", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("how to check if an imported toy has mandatory BIS certification clearance at customs", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("can a manufacturer use the ISI mark while their renewal application is pending", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("what happens during a BIS raid and factory seizure for unauthorized ISI marking", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("how to verify if an electric vehicle EV charger is certified under Indian Standards", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("how to check if a laboratory test report has genuine NABL ULR QR code", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("what is the penalty for tampering with weights and measures under Legal Metrology Act", ChatMode.INDUSTRY, "Consumer Doubts & Grievance"),
    ("can a consumer directly send a market sample to a BIS recognized laboratory for testing", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
    ("rights of consumers under Consumer Protection Act 2019 regarding certified goods", ChatMode.CONSUMER, "Consumer Doubts & Grievance"),
]


async def run_100_parameter_suite():
    print("=" * 90)
    print("🚀 EXECUTING 100-PARAMETER BENCHMARK (GOLD, BIS, PRODUCTS & DOUBTS)")
    print("=" * 90)

    start_total = time.time()
    passed = 0
    failed = 0
    failures: List[Dict[str, Any]] = []

    for idx, (query, mode, category) in enumerate(TEST_100_PARAMETERS, 1):
        t0 = time.time()
        try:
            res = await rag_engine.answer_query(query=query, mode=mode)
            elapsed = time.time() - t0

            # Verification assertions:
            # 1. Answer must be non-empty and substantive (> 100 characters)
            # 2. Refusal must NOT be triggered (these are all 100% valid in-domain queries)
            # 3. Confidence score must be >= 0.70
            is_substantive = len(res.answer.strip()) > 100
            no_refusal = not res.refusal_triggered
            has_confidence = res.confidence_score >= 0.70

            if is_substantive and no_refusal and has_confidence:
                passed += 1
                snippet = res.answer.replace('\n', ' ')[:75]
                print(f"✅ [{idx:03d}/100] PASS ({elapsed*1000:4.0f}ms) | {category:<28} | {query[:35]:<35} | Conf: {res.confidence_score:.2f}")
            else:
                failed += 1
                reasons = []
                if not is_substantive: reasons.append("Answer too short (<100 chars)")
                if not no_refusal: reasons.append("Refusal unexpectedly triggered")
                if not has_confidence: reasons.append(f"Low confidence ({res.confidence_score:.2f})")
                
                fail_info = {
                    "index": idx,
                    "query": query,
                    "category": category,
                    "reasons": reasons,
                    "answer_snippet": res.answer[:120]
                }
                failures.append(fail_info)
                print(f"❌ [{idx:03d}/100] FAIL ({elapsed*1000:4.0f}ms) | {category:<28} | {query[:35]:<35} | Reasons: {', '.join(reasons)}")

        except Exception as e:
            failed += 1
            elapsed = time.time() - t0
            failures.append({
                "index": idx,
                "query": query,
                "category": category,
                "reasons": [f"Exception: {str(e)}"],
                "answer_snippet": "CRASH"
            })
            print(f"💥 [{idx:03d}/100] CRASH ({elapsed*1000:4.0f}ms) | {category:<28} | {query[:35]:<35} | Error: {str(e)}")

    total_time = time.time() - start_total

    print("=" * 90)
    print("📊 100-PARAMETER TEST SUITE SUMMARY REPORT")
    print(f"   Total Tested Parameters: {len(TEST_100_PARAMETERS)}")
    print(f"   Passed:                  {passed}/{len(TEST_100_PARAMETERS)} ({passed/len(TEST_100_PARAMETERS)*100:.1f}%)")
    print(f"   Failed:                  {failed}/{len(TEST_100_PARAMETERS)}")
    print(f"   Total Execution Time:    {total_time:.2f} seconds ({total_time/len(TEST_100_PARAMETERS)*1000:.1f} ms/query avg)")
    print("=" * 90)

    if failures:
        print("\n⚠️ DIAGNOSTIC DETAILS OF FAILURES TO RECONSTRUCT:")
        for f in failures:
            print(f"  [{f['index']}] Query: '{f['query']}'")
            print(f"      Category: {f['category']}")
            print(f"      Reasons:  {f['reasons']}")
            print(f"      Snippet:  {f['answer_snippet']}")
            print("  " + "-" * 60)
        sys.exit(1)
    else:
        print("\n🎉 ALL 100 IN-DOMAIN PARAMETERS PASSED PERFECTLY!")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(run_100_parameter_suite())
