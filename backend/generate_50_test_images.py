"""
50 Test Images Generator for Camera, Optical Scanner & Upload Features.
Part of GRASK AI (SIH26107).
Generates 50 distinct images covering:
- 12 Audit Compliance Test Reports
- 13 FSSAI Nutri-Score Packaging Labels
- 13 MANAK-Vision Statutory Marks & Barcodes
- 12 Irrelevant & Out-of-Scope Negative Images (Cars, Pets, Scenery, Portraits, Noise)
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_dataset"))
os.makedirs(DATASET_DIR, exist_ok=True)

font_dir = os.environ.get('WINDIR', 'C:\\Windows')
fonts_path = os.path.join(font_dir, 'Fonts')

def get_font(size=18, bold=False):
    try:
        fn = 'arialbd.ttf' if bold else 'arial.ttf'
        p = os.path.join(fonts_path, fn)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
        p2 = os.path.join(fonts_path, 'calibrib.ttf' if bold else 'calibri.ttf')
        if os.path.exists(p2):
            return ImageFont.truetype(p2, size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

font_title = get_font(20, bold=True)
font_subtitle = get_font(15)
font_body = get_font(17)
font_bold = get_font(18, bold=True)

_orig_draw = ImageDraw.Draw

class SmartImageDraw:
    def __init__(self, img):
        self._draw = _orig_draw(img)
        self.font_body = font_body
    def text(self, xy, text, fill=None, font=None, **kwargs):
        if font is None:
            font = self.font_body
        self._draw.text(xy, text, fill=fill, font=font, **kwargs)
    def __getattr__(self, name):
        return getattr(self._draw, name)

ImageDraw.Draw = SmartImageDraw

def draw_header(draw, title, subtitle, width, bg_color=(235, 243, 250), text_color=(15, 23, 42)):
    draw.rectangle([(0, 0), (width, 80)], fill=bg_color)
    draw.line([(0, 80), (width, 80)], fill=(180, 200, 220), width=2)
    draw.text((20, 15), title, fill=text_color, font=font_title)
    draw.text((20, 48), subtitle, fill=(70, 85, 105), font=font_subtitle)

def draw_barcode_bars(draw, x_start, y_start, width, height, number_str):
    # Draw simulated optical vertical bars
    pattern = [2, 1, 3, 1, 2, 2, 1, 3, 1, 2, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 3, 1, 2, 2, 1]
    curr_x = x_start
    draw.rectangle([(x_start - 10, y_start - 10), (x_start + width + 10, y_start + height + 35)], fill=(255, 255, 255), outline=(200, 200, 200))
    for p in pattern:
        if curr_x >= x_start + width - 10:
            break
        bar_w = p * 2
        draw.rectangle([(curr_x, y_start), (curr_x + bar_w, y_start + height)], fill=(0, 0, 0))
        curr_x += bar_w + 3
    draw.text((x_start + 15, y_start + height + 8), number_str, fill=(0, 0, 0), font=font_bold)

def generate_all_images():
    manifest = []
    print("Generating 50 synthetic high-fidelity test images...")

    # =========================================================================
    # CATEGORY 1: AUDIT COMPLIANCE LAB REPORTS (12 images)
    # =========================================================================
    
    # 01. Packaged Drinking Water IS 14543 (Conforming)
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "CENTRAL WATER TESTING LABORATORY (NABL ACCREDITED)", "TEST REPORT & CHEMICAL ANALYSIS CERTIFICATE", 700)
    d.text((30, 100), "Standard: IS 14543 : 2018 (Packaged Drinking Water)", fill=(0, 0, 0))
    d.text((30, 125), "Product: Natural Mountain Dew Packaged Water 1L", fill=(0, 0, 0))
    d.text((30, 150), "Manufacturer: Apex Beverages Private Limited", fill=(0, 0, 0))
    d.text((30, 175), "Batch No: APEX-WTR-2026-B01  |  Date: 15-Mar-2026", fill=(0, 0, 0))
    d.rectangle([(25, 210), (675, 480)], outline=(0, 0, 0), width=2)
    d.line([(25, 245), (675, 245)], fill=(0, 0, 0), width=2)
    d.line([(320, 210), (320, 480)], fill=(0, 0, 0), width=1)
    d.line([(450, 210), (450, 480)], fill=(0, 0, 0), width=1)
    d.line([(560, 210), (560, 480)], fill=(0, 0, 0), width=1)
    d.text((35, 220), "TEST PARAMETER", fill=(0, 0, 0))
    d.text((330, 220), "OBSERVED VALUE", fill=(0, 0, 0))
    d.text((460, 220), "IS LIMIT", fill=(0, 0, 0))
    d.text((570, 220), "VERDICT", fill=(0, 0, 0))
    params = [
        ("pH Value", "7.35", "6.5 - 8.5", "PASS"),
        ("Total Dissolved Solids (TDS)", "125.0 mg/L", "Max 500", "PASS"),
        ("Turbidity", "0.45 NTU", "Max 2.0", "PASS"),
        ("Lead (as Pb)", "0.003 mg/L", "Max 0.01", "PASS"),
        ("Arsenic (as As)", "0.002 mg/L", "Max 0.01", "PASS"),
        ("Nitrate (as NO3)", "14.2 mg/L", "Max 45.0", "PASS"),
        ("Escherichia coli (E. coli)", "0 cfu/250ml", "Absent", "PASS")
    ]
    y = 255
    for p, v, l, stat in params:
        d.text((35, y), p, fill=(0, 0, 0))
        d.text((330, y), v, fill=(0, 0, 0))
        d.text((460, y), l, fill=(70, 70, 70))
        d.text((570, y), stat, fill=(16, 120, 50))
        y += 30
    d.text((30, 510), "CONCLUSION: The tested sample conforms 100% to IS 14543:2018 requirements.", fill=(16, 120, 50))
    path = os.path.join(DATASET_DIR, "audit_01_water_conforming.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_01_water_conforming.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 02. Packaged Drinking Water IS 14543 (Toxic Lead Violation)
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "REGIONAL TOXICOLOGY & WATER QUALITY LAB", "STATUTORY TEST CERTIFICATE - BATCH VERIFICATION", 700)
    d.text((30, 100), "Standard: IS 14543 : 2018 (Packaged Drinking Water)", fill=(0, 0, 0))
    d.text((30, 125), "Product: BlueMountain Aqua Fresh 500ml", fill=(0, 0, 0))
    d.text((30, 150), "Manufacturer: BlueSpring Bottling Corp", fill=(0, 0, 0))
    d.text((30, 175), "Batch No: BSB-2026-TOXIC-04", fill=(0, 0, 0))
    d.rectangle([(25, 210), (675, 450)], outline=(0, 0, 0), width=2)
    d.text((35, 220), "TEST PARAMETER", fill=(0, 0, 0))
    d.text((330, 220), "OBSERVED VALUE", fill=(0, 0, 0))
    d.text((460, 220), "IS LIMIT", fill=(0, 0, 0))
    d.text((570, 220), "STATUS", fill=(0, 0, 0))
    d.line([(25, 245), (675, 245)], fill=(0, 0, 0), width=2)
    fail_params = [
        ("pH Value", "7.10", "6.5 - 8.5", "PASS"),
        ("Total Dissolved Solids (TDS)", "320.0 mg/L", "Max 500", "PASS"),
        ("Lead (as Pb)", "0.028 mg/L", "Max 0.01", "CRITICAL FAIL"),
        ("Arsenic (as As)", "0.003 mg/L", "Max 0.01", "PASS"),
        ("Turbidity", "1.60 NTU", "Max 2.0", "PASS"),
        ("E. Coli", "0 cfu/250ml", "Absent", "PASS")
    ]
    y = 255
    for p, v, l, stat in fail_params:
        d.text((35, y), p, fill=(0, 0, 0))
        d.text((330, y), v, fill=(0, 0, 0))
        d.text((460, y), l, fill=(70, 70, 70))
        col = (200, 20, 20) if "FAIL" in stat else (16, 120, 50)
        d.text((570, y), stat, fill=col)
        y += 30
    d.text((30, 480), "ALERT: Lead content 0.028 mg/L severely violates IS 14543 limit of 0.01 mg/L.", fill=(200, 20, 20))
    path = os.path.join(DATASET_DIR, "audit_02_water_toxic_lead.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_02_water_toxic_lead.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "NON_CONFORMING"})

    # 03. Steel TMT Rebar Fe 500D IS 1786 (Pass)
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "METALLURGICAL TEST LABORATORY OF INDIA", "MILL TEST CERTIFICATE - DEFORMED STEEL REBARS", 700)
    d.text((30, 100), "Standard: IS 1786 : 2008 Grade Fe 500D", fill=(0, 0, 0))
    d.text((30, 125), "Product: High Strength TMT Steel Rebar 12mm", fill=(0, 0, 0))
    d.text((30, 150), "Manufacturer: Jindal Supreme Steel Ltd", fill=(0, 0, 0))
    d.text((30, 175), "Batch Heat No: JSS-FE500D-HEAT88", fill=(0, 0, 0))
    d.rectangle([(25, 210), (675, 450)], outline=(0, 0, 0), width=2)
    d.text((35, 220), "MECHANICAL PROPERTY", fill=(0, 0, 0))
    d.text((330, 220), "OBSERVED", fill=(0, 0, 0))
    d.text((460, 220), "IS 1786 LIMIT", fill=(0, 0, 0))
    d.text((570, 220), "STATUS", fill=(0, 0, 0))
    d.line([(25, 245), (675, 245)], fill=(0, 0, 0), width=2)
    steel_params = [
        ("0.2% Proof Stress / Yield Strength", "540.0 N/mm2", "Min 500.0", "PASS"),
        ("Tensile Strength (UTS)", "615.0 N/mm2", "Min 565.0", "PASS"),
        ("UTS / Yield Ratio", "1.14", "Min 1.10", "PASS"),
        ("Elongation", "18.0 %", "Min 16.0", "PASS"),
        ("Carbon (C)", "0.22 %", "Max 0.25", "PASS"),
        ("Sulphur (S)", "0.035 %", "Max 0.040", "PASS")
    ]
    y = 255
    for p, v, l, stat in steel_params:
        d.text((35, y), p, fill=(0, 0, 0))
        d.text((330, y), v, fill=(0, 0, 0))
        d.text((460, y), l, fill=(70, 70, 70))
        d.text((570, y), stat, fill=(16, 120, 50))
        y += 30
    path = os.path.join(DATASET_DIR, "audit_03_steel_fe500d_pass.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_03_steel_fe500d_pass.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 04. Steel TMT Rebar Fe 500D (Fail - Low Yield Strength)
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "INDEPENDENT METROLOGY & METALLURGY LAB", "REBAR QUALITY AUDIT REPORT - STATUTORY COMPLIANCE", 700)
    d.text((30, 100), "Standard: IS 1786 : 2008 Grade Fe 500D", fill=(0, 0, 0))
    d.text((30, 125), "Manufacturer: Substandard Rolling Mill", fill=(0, 0, 0))
    d.text((30, 150), "Yield Strength: 425.0 N/mm2 (Standard Min: 500.0)", fill=(200, 20, 20))
    d.text((30, 175), "Tensile Strength: 480.0 N/mm2", fill=(0, 0, 0))
    d.text((30, 200), "Elongation: 12.0 % (Standard Min: 16.0)", fill=(200, 20, 20))
    d.text((30, 240), "VERDICT: CRITICAL FAILURE. Material does not conform to Fe 500D structural grade.", fill=(200, 20, 20))
    path = os.path.join(DATASET_DIR, "audit_04_steel_low_strength_fail.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_04_steel_low_strength_fail.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "NON_CONFORMING"})

    # 05. Ordinary Portland Cement 53 Grade IS 269
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "NATIONAL COUNCIL FOR CEMENT AND BUILDING MATERIALS", "CEMENT QUALITY TESTING CERTIFICATE", 700)
    d.text((30, 100), "Standard: IS 269 : 2015 Grade 53", fill=(0, 0, 0))
    d.text((30, 125), "Product: Ordinary Portland Cement 53 Grade", fill=(0, 0, 0))
    d.text((30, 150), "Manufacturer: UltraTech Cement Corporation", fill=(0, 0, 0))
    cement_p = [
        ("Soundness (Le Chatelier)", "1.5 mm", "Max 10.0 mm"),
        ("Initial Setting Time", "125.0 min", "Min 30 min"),
        ("Final Setting Time", "210.0 min", "Max 600 min"),
        ("28-Day Compressive Strength", "56.4 MPa", "Min 53.0 MPa"),
        ("Insoluble Residue", "1.8 %", "Max 5.0 %")
    ]
    y = 190
    for p, v, l in cement_p:
        d.text((30, y), f"{p}: {v} (Limit: {l}) - PASS", fill=(0, 0, 0))
        y += 28
    path = os.path.join(DATASET_DIR, "audit_05_cement_53grade_pass.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_05_cement_53grade_pass.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 06. Municipal Drinking Water IS 10500
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "NEERI ENVIRONMENTAL TESTING LABORATORY", "POTABLE DRINKING WATER REPORT - IS 10500", 700)
    d.text((30, 100), "Standard: IS 10500 : 2012 Drinking Water Specification", fill=(0, 0, 0))
    d.text((30, 130), "pH Value: 7.4 | TDS: 210.0 mg/L | Turbidity: 0.65 NTU", fill=(0, 0, 0))
    d.text((30, 160), "Hardness (CaCO3): 140 mg/L | Chlorides: 85 mg/L | Fluoride: 0.7 mg/L", fill=(0, 0, 0))
    d.text((30, 190), "Lead: 0.002 mg/L | Arsenic: 0.001 mg/L | E. Coli: Absent", fill=(0, 0, 0))
    d.text((30, 230), "VERDICT: Conforming to all IS 10500 potable domestic limits.", fill=(16, 120, 50))
    path = os.path.join(DATASET_DIR, "audit_06_drinking_water_is10500.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_06_drinking_water_is10500.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 07. HDPE Pipe IS 4984
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "CENTRAL CIPET POLYMER TESTING CENTER", "HDPE PRESSURE PIPE CERTIFICATE - IS 4984", 700)
    d.text((30, 100), "Standard: IS 4984 : 2016 (PE 100 Pipes for Water Supply)", fill=(0, 0, 0))
    d.text((30, 130), "Density: 0.952 g/cm3 (IS Limit: 0.940 - 0.960) - PASS", fill=(0, 0, 0))
    d.text((30, 160), "Melt Flow Rate (MFR): 0.38 g/10min (Limit: 0.2 - 1.1) - PASS", fill=(0, 0, 0))
    d.text((30, 190), "Hydrostatic Pressure (100h at 20C): No rupture, Conforming - PASS", fill=(0, 0, 0))
    d.text((30, 220), "Elongation at Break: 450% (Min 350%) - PASS", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "audit_07_hdpe_pipe_is4984.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_07_hdpe_pipe_is4984.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 08. Two Wheeler Helmet IS 4151
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "AUTOMOTIVE RESEARCH ASSOCIATION OF INDIA (ARAI)", "PROTECTIVE HELMET SAFETY TEST REPORT - IS 4151", 700)
    d.text((30, 100), "Standard: IS 4151 : 2015 (Protective Helmets for Motorcycle Riders)", fill=(0, 0, 0))
    d.text((30, 130), "Impact Absorption Test: Peak Headform Deceleration 145g (Max 300g) - PASS", fill=(0, 0, 0))
    d.text((30, 160), "Penetration Resistance: Tip did not pierce inner liner - PASS", fill=(0, 0, 0))
    d.text((30, 190), "Retention System Dynamic Displacement: 18.0 mm (Max 35.0 mm) - PASS", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "audit_08_helmet_is4151.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_08_helmet_is4151.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 09. Structural Steel Plates IS 2062
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "BUREAU OF STEEL INSPECTION", "STRUCTURAL STEEL PLATE TEST REPORT - IS 2062", 700)
    d.text((30, 100), "Standard: IS 2062 : 2011 Grade E250 (Fe 410W)", fill=(0, 0, 0))
    d.text((30, 130), "Yield Strength: 275 MPa (Min 250 MPa) - PASS", fill=(0, 0, 0))
    d.text((30, 160), "Tensile Strength: 440 MPa (410 - 540 MPa) - PASS", fill=(0, 0, 0))
    d.text((30, 190), "Elongation: 25.0 % (Min 23.0%) - PASS", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "audit_09_structural_steel_is2062.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_09_structural_steel_is2062.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 10. Plastic Migration Test IS 9845
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "FOOD CONTACT MATERIALS TESTING CENTER", "GLOBAL MIGRATION CERTIFICATE - IS 9845", 700)
    d.text((30, 100), "Standard: IS 9845 (Food Contact Plastic Articles)", fill=(0, 0, 0))
    d.text((30, 130), "Distilled Water Simulant: 4.2 mg/dm2 (Limit: Max 10.0 mg/dm2) - PASS", fill=(0, 0, 0))
    d.text((30, 160), "3% Acetic Acid Simulant: 5.1 mg/dm2 (Limit: Max 10.0 mg/dm2) - PASS", fill=(0, 0, 0))
    d.text((30, 190), "15% Ethanol Simulant: 3.8 mg/dm2 (Limit: Max 10.0 mg/dm2) - PASS", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "audit_10_plastic_migration_is9845.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_10_plastic_migration_is9845.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 11. LED Luminaire IS 16102
    img = Image.new("RGB", (700, 850), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "ELECTRICAL ELECTRONICS TESTING LAB", "LED BULB SAFETY REPORT - IS 16102", 700)
    d.text((30, 100), "Standard: IS 16102 (Part 1) : 2012 (Self-Ballasted LED Lamps)", fill=(0, 0, 0))
    d.text((30, 130), "Insulation Resistance: 85 MOhm (Min 4 MOhm) - PASS", fill=(0, 0, 0))
    d.text((30, 160), "Electric Strength (Hipot): 4000V Breakdown: None - PASS", fill=(0, 0, 0))
    d.text((30, 190), "Creepage Distance: 6.2 mm (Min 5.0 mm) - PASS", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "audit_11_led_luminaire_is16102.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "audit_11_led_luminaire_is16102.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # 12. Faded / Low Contrast Report
    img = Image.new("RGB", (700, 850), (240, 240, 235))
    d = ImageDraw.Draw(img)
    draw_header(d, "CARBON COPY - FIELD TEST CERTIFICATE", "IS 14543 PACKAGED WATER TESTING", 700, bg_color=(230, 230, 220))
    d.text((30, 100), "Standard: IS 14543 : 2018 Packaged Water", fill=(80, 80, 80))
    d.text((30, 130), "pH Value: 7.2 | Total Dissolved Solids: 135 mg/L", fill=(80, 80, 80))
    d.text((30, 160), "Lead: 0.003 mg/L | Turbidity: 0.5 NTU", fill=(80, 80, 80))
    path = os.path.join(DATASET_DIR, "audit_12_faded_report.jpg")
    img.save(path, quality=80)
    manifest.append({"file": "audit_12_faded_report.jpg", "category": "audit_compliance", "expected_relevant": True, "expected_verdict": "CONFORMING"})

    # =========================================================================
    # CATEGORY 2: FSSAI NUTRI-SCORE FOOD LABELS (13 images)
    # =========================================================================

    # 13. Biscuits High Sugar + Palm Oil
    img = Image.new("RGB", (650, 750), (255, 250, 240))
    d = ImageDraw.Draw(img)
    draw_header(d, "BRITANNIA CHOCO DELIGHT BISCUITS", "NUTRITIONAL FACTS & INGREDIENTS LIST", 650, bg_color=(254, 235, 200), text_color=(120, 50, 10))
    d.rectangle([(25, 100), (625, 420)], outline=(120, 50, 10), width=2)
    d.text((40, 115), "NUTRITION INFORMATION (Per 100g)", fill=(120, 50, 10))
    d.line([(25, 140), (625, 140)], fill=(120, 50, 10), width=1)
    b_nutri = [
        "Energy: 485 kcal",
        "Protein: 6.5 g",
        "Carbohydrate: 68.0 g",
        "  Total Sugars: 34.0 g",
        "  Added Sugars: 32.0 g",
        "Total Fat: 21.0 g",
        "  Saturated Fat: 11.5 g",
        "  Trans Fat: 0.1 g",
        "Sodium: 340 mg"
    ]
    y = 155
    for line in b_nutri:
        d.text((40, y), line, fill=(20, 20, 20))
        y += 24
    d.text((30, 440), "INGREDIENTS: Refined Wheat Flour (Maida), Sugar (32%), Refined Palm Oil,", fill=(20, 20, 20))
    d.text((30, 465), "Hydrogenated Vegetable Fat, Cocoa Solids (4.5%), Invert Sugar Syrup,", fill=(20, 20, 20))
    d.text((30, 490), "Raising Agents [INS 503(ii), INS 500(ii)], Emulsifier [INS 322], Iodized Salt.", fill=(20, 20, 20))
    d.text((30, 530), "FSSAI Lic. No. 10015042001890", fill=(50, 50, 50))
    path = os.path.join(DATASET_DIR, "nutri_01_biscuit_high_sugar.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_01_biscuit_high_sugar.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 14. Instant Noodles (High Sodium + MSG + Palm Oil)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "MAGGI 2-MINUTE NOODLES (MASALA)", "NUTRITIONAL FACTS PER 100g", 650, bg_color=(255, 230, 50), text_color=(180, 0, 0))
    d.text((30, 100), "Energy: 427 kcal  |  Protein: 8.0 g  |  Carbohydrate: 63.5 g", fill=(0, 0, 0))
    d.text((30, 130), "Total Sugars: 2.2 g  |  Added Sugars: 1.1 g", fill=(0, 0, 0))
    d.text((30, 160), "Total Fat: 15.7 g  |  Saturated Fat: 6.8 g  |  Trans Fat: 0.12 g", fill=(0, 0, 0))
    d.text((30, 190), "Sodium: 1020 mg (EXCEEDS WHO DAILY THRESHOLD)", fill=(200, 0, 0))
    d.text((30, 230), "INGREDIENTS: Refined Wheat Flour (Maida), Palm Oil, Salt, Wheat Gluten,", fill=(0, 0, 0))
    d.text((30, 255), "Mineral (Calcium Carbonate), Thickener (INS 508), Flavor Enhancer (INS 621 MSG),", fill=(0, 0, 0))
    d.text((30, 280), "Acidity Regulators (INS 501(i), INS 500(i)), Caramel Color (INS 150d).", fill=(0, 0, 0))
    d.text((30, 320), "FSSAI Central License No: 10012011000168", fill=(0, 50, 120))
    path = os.path.join(DATASET_DIR, "nutri_02_instant_noodles.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_02_instant_noodles.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 15. Pure Peanut Butter (Secure / Conforming)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "MYFITNESS 100% NATURAL PEANUT BUTTER", "PURE HIGH PROTEIN SPREAD - NO ADDED SUGAR", 650, bg_color=(230, 245, 230), text_color=(20, 100, 30))
    d.text((30, 100), "NUTRITION FACTS (Per 100g):", fill=(0, 0, 0))
    d.text((30, 130), "Energy: 620 kcal  |  Protein: 30.2 g (High Protein)", fill=(16, 120, 50))
    d.text((30, 160), "Carbohydrates: 18.0 g  |  Total Sugar: 5.0 g  |  Added Sugar: 0.0 g", fill=(16, 120, 50))
    d.text((30, 190), "Dietary Fiber: 8.5 g  |  Total Fat: 49.0 g  |  Saturated Fat: 8.0 g", fill=(0, 0, 0))
    d.text((30, 220), "Trans Fat: 0.0 g  |  Cholesterol: 0.0 mg  |  Sodium: 15 mg", fill=(16, 120, 50))
    d.text((30, 260), "INGREDIENTS: 100% Roasted Peanuts. No Added Sugar, No Salt, No Hydrogenated Palm Oil.", fill=(20, 100, 30))
    d.text((30, 300), "FSSAI License: 10722999001593", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_03_peanut_butter_pure.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_03_peanut_butter_pure.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "SECURE"})

    # 16. Mango Fruit Drink (Added Sugars + Synthetic Color)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "FROOTEZ MANGO NECTAR DRINK", "FRUIT BEVERAGE LABEL & NUTRITION TABLE", 650, bg_color=(255, 220, 100), text_color=(150, 80, 0))
    d.text((30, 100), "Nutrition Facts (Per 100ml):", fill=(0, 0, 0))
    d.text((30, 130), "Energy: 65 kcal | Carbohydrates: 16.2 g | Added Sugar: 14.5 g", fill=(200, 20, 20))
    d.text((30, 160), "Protein: 0.1 g | Total Fat: 0.0 g | Sodium: 45 mg", fill=(0, 0, 0))
    d.text((30, 200), "INGREDIENTS: Water, Mango Pulp (18%), Sugar, Acidity Regulator (INS 330),", fill=(0, 0, 0))
    d.text((30, 225), "Antioxidant (INS 300), Synthetic Food Color (INS 110 Sunset Yellow FCF).", fill=(200, 20, 20))
    path = os.path.join(DATASET_DIR, "nutri_04_fruit_beverage.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_04_fruit_beverage.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 17. Potato Chips (Trans Fat + High Sodium)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "CRUNCHY MAGIC MASALA POTATO CHIPS", "SAVORY SNACK NUTRITION FACTS", 650)
    d.text((30, 100), "Per 100g: Energy 545 kcal | Fat 35.5g | Saturated Fat 15.0g", fill=(0, 0, 0))
    d.text((30, 130), "Trans Fat 0.35g | Sodium 890mg | Carbohydrates 52.0g | Protein 6.0g", fill=(200, 0, 0))
    d.text((30, 170), "INGREDIENTS: Potatoes, Palmolein Oil, Edible Common Salt, Spices, INS 627, INS 631.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_05_potato_chips.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_05_potato_chips.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 18. Whole Wheat Atta (Secure)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "AASHIRVAAD SHUDH CHAKKI ATTA", "100% WHOLE WHEAT FLOUR - HIGH FIBER", 650, bg_color=(235, 245, 230))
    d.text((30, 100), "Per 100g: Energy 365 kcal | Protein 12.1g | Dietary Fiber 11.5g", fill=(16, 120, 50))
    d.text((30, 130), "Carbohydrates 72.0g | Total Sugar 1.8g | Added Sugar 0g", fill=(16, 120, 50))
    d.text((30, 160), "Total Fat 1.7g | Saturated Fat 0.3g | Sodium 8 mg", fill=(16, 120, 50))
    d.text((30, 200), "INGREDIENTS: 100% Whole Wheat Grain. Zero additives, zero preservatives.", fill=(16, 120, 50))
    path = os.path.join(DATASET_DIR, "nutri_06_whole_wheat_atta.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_06_whole_wheat_atta.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "SECURE"})

    # 19. Energy Drink (Harmful)
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "TURBO CHARGE ENERGY BEVERAGE", "HIGH CAFFEINE CARBONATED DRINK", 650, bg_color=(255, 220, 220), text_color=(180, 0, 0))
    d.text((30, 100), "Energy: 75 kcal | Added Sugars: 18.5g | High Fructose Corn Syrup", fill=(200, 0, 0))
    d.text((30, 130), "Caffeine: 32 mg/100ml | Taurine: 400 mg | Sodium: 120 mg", fill=(200, 0, 0))
    d.text((30, 170), "INGREDIENTS: Carbonated Water, Sugar, Invert Sugar, Caffeine, INS 102 (Tartrazine), INS 211.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_07_energy_drink.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_07_energy_drink.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 20. Dark Chocolate 70%
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "AMUL DARK CHOCOLATE 70% COCOA", "NUTRITIONAL FACTS & COMPOSITION", 650)
    d.text((30, 100), "Per 100g: Energy 540 kcal | Protein 8.5g | Carbohydrates 45.0g", fill=(0, 0, 0))
    d.text((30, 130), "Added Sugar: 24.0g | Total Fat: 36.0g | Saturated Fat: 22.0g", fill=(0, 0, 0))
    d.text((30, 170), "INGREDIENTS: Cocoa Solids, Cocoa Butter, Sugar, Permitted Emulsifier (INS 322).", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_08_dark_chocolate.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_08_dark_chocolate.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "CAUTION"})

    # 21. Pasteurized Cow Milk
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "NANDINI STANDARDIZED COW MILK", "PASTEURIZED FRESH PACKAGED MILK", 650, bg_color=(230, 245, 255))
    d.text((30, 100), "Per 100ml: Energy 72 kcal | Protein 3.3g | Carbohydrates 4.8g", fill=(0, 0, 0))
    d.text((30, 130), "Milk Fat: 4.5g | Calcium: 125 mg | Added Sugar: 0g | Sodium: 48 mg", fill=(16, 120, 50))
    d.text((30, 170), "INGREDIENTS: Pasteurized Standardized Cow Milk. No additives.", fill=(16, 120, 50))
    path = os.path.join(DATASET_DIR, "nutri_09_pasteurized_milk.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_09_pasteurized_milk.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "SECURE"})

    # 22. Infant Cereal Food
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "NESTLE CERELAC BABY CEREAL", "INFANT GRAIN COMPLIMENTARY FOOD", 650)
    d.text((30, 100), "Per 100g: Energy 415 kcal | Protein 15.0g | Carbohydrates 68.0g", fill=(0, 0, 0))
    d.text((30, 130), "Added Sugar: 7.5g | Maltodextrin: 8.0g | Iron: 9.0 mg | Zinc: 2.5 mg", fill=(0, 0, 0))
    d.text((30, 170), "INGREDIENTS: Wheat Flour, Milk Solids, Sugar, Soybean Oil, Mineral & Vitamin Premix.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_10_infant_cereal.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_10_infant_cereal.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "CAUTION"})

    # 23. Corn Flakes
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "KELLOGGS ORIGINAL CORN FLAKES", "BREAKFAST CEREAL NUTRITION FACTS", 650)
    d.text((30, 100), "Per 100g: Energy 380 kcal | Protein 7.5g | Total Carbohydrate 84.0g", fill=(0, 0, 0))
    d.text((30, 130), "Total Sugar: 8.5g | Total Fat: 0.6g | Sodium: 460 mg", fill=(0, 0, 0))
    d.text((30, 170), "INGREDIENTS: Milled Corn (91%), Sugar, Barley Malt Extract, Iodized Salt, Vitamins.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_11_corn_flakes.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_11_corn_flakes.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "CAUTION"})

    # 24. Tomato Ketchup
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "KISSAN FRESH TOMATO KETCHUP", "SAUCE INGREDIENTS & NUTRITION TABLE", 650)
    d.text((30, 100), "Per 100g: Energy 135 kcal | Sugar: 28.5g (High Sugar) | Sodium: 850 mg", fill=(200, 0, 0))
    d.text((30, 130), "Protein: 1.2g | Fat: 0.1g", fill=(0, 0, 0))
    d.text((30, 170), "INGREDIENTS: Water, Tomato Paste (28%), Sugar, Salt, Acidity Regulator (INS 260), Preservative (INS 211).", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_12_tomato_ketchup.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_12_tomato_ketchup.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # 25. Namkeen Savory Mixture
    img = Image.new("RGB", (650, 750), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "HALDIRAM KHATTA MEETHA NAMKEEN", "SNACK MIXTURE NUTRITIONAL FACTS", 650)
    d.text((30, 100), "Per 100g: Energy 520 kcal | Total Fat 31.0g | Saturated Fat 13.0g", fill=(200, 0, 0))
    d.text((30, 130), "Sodium: 580 mg | Carbohydrates 52.0g | Added Sugar: 12.0g", fill=(200, 0, 0))
    d.text((30, 170), "INGREDIENTS: Chickpea Flour, Palmolein Oil, Peanuts, Rice Flakes, Sugar, Citric Acid.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "nutri_13_namkeen_snack.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "nutri_13_namkeen_snack.jpg", "category": "nutri_score", "expected_relevant": True, "expected_verdict": "HARMFUL"})

    # =========================================================================
    # CATEGORY 3: MANAK-VISION MARKS & BARCODES (13 images)
    # =========================================================================

    # 26. Bisleri Water with ISI Mark & CM/L
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "BISLERI PACKAGED DRINKING WATER", "STATUTORY ISI STANDARD MARK LABEL", 650, bg_color=(230, 245, 255))
    d.ellipse([(250, 120), (400, 240)], outline=(0, 0, 0), width=4)
    d.text((305, 160), "IS", fill=(0, 0, 0))
    d.text((260, 95), "IS 14543", fill=(0, 0, 0))
    d.text((245, 255), "CM/L-8400152488", fill=(0, 0, 0))
    d.text((40, 320), "Brand: Bisleri  |  Product: Packaged Drinking Water", fill=(0, 0, 0))
    d.text((40, 350), "Manufacturer: Bisleri International Pvt Ltd, Greater Noida", fill=(0, 0, 0))
    draw_barcode_bars(d, 180, 420, 280, 80, "8901030383728")
    path = os.path.join(DATASET_DIR, "mark_01_bisleri_water_cml.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_01_bisleri_water_cml.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 27. Tata Tiscon Steel Rebar CM/L
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "TATA TISCON 500D REBAR TAG", "BUREAU OF INDIAN STANDARDS CERTIFICATION", 650)
    d.ellipse([(250, 120), (400, 240)], outline=(0, 0, 0), width=4)
    d.text((305, 160), "IS", fill=(0, 0, 0))
    d.text((260, 95), "IS 1786", fill=(0, 0, 0))
    d.text((255, 255), "CM/L-5400234", fill=(0, 0, 0))
    d.text((40, 320), "Company: Tata Steel Limited (Jamshedpur Works)", fill=(0, 0, 0))
    d.text((40, 350), "Grade: High Strength TMT Deformed Rebar Fe 500D", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_02_tatatiscon_cml.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_02_tatatiscon_cml.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 28. UltraTech Cement CM/L
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "ULTRATECH CEMENT BAG FRONT PANEL", "BIS COMPULSORY LICENSING SCHEME-I", 650)
    d.ellipse([(250, 120), (400, 240)], outline=(0, 0, 0), width=4)
    d.text((305, 160), "IS", fill=(0, 0, 0))
    d.text((270, 95), "IS 269", fill=(0, 0, 0))
    d.text((255, 255), "CM/L-6200189", fill=(0, 0, 0))
    d.text((40, 320), "Product: Ordinary Portland Cement 53 Grade", fill=(0, 0, 0))
    d.text((40, 350), "Manufacturer: UltraTech Cement Limited", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_03_ultratech_cement_cml.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_03_ultratech_cement_cml.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 29. boAt Earbuds CRS + Barcode
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "BOAT NIRVANA IVY PRO EARBUDS", "MEITY COMPULSORY REGISTRATION SCHEME", 650)
    d.rectangle([(230, 110), (420, 210)], outline=(0, 0, 0), width=3)
    d.text((305, 120), "CRS", fill=(0, 0, 0))
    d.text((270, 145), "IS 616 : 2017", fill=(0, 0, 0))
    d.text((250, 175), "R-41292958", fill=(0, 0, 0))
    d.text((40, 240), "Product: True Wireless Stereo (TWS) Earbuds", fill=(0, 0, 0))
    d.text((40, 270), "Brand: boAt (Imagine Marketing Limited)", fill=(0, 0, 0))
    draw_barcode_bars(d, 180, 330, 280, 90, "8905650102321")
    path = os.path.join(DATASET_DIR, "mark_04_boat_earbuds_crs.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_04_boat_earbuds_crs.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 30. Dell Laptop Adapter CRS
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "DELL LAPTOP POWER ADAPTER", "MEITY CRS SAFETY REGISTRATION", 650)
    d.rectangle([(230, 110), (420, 210)], outline=(0, 0, 0), width=3)
    d.text((305, 120), "CRS", fill=(0, 0, 0))
    d.text((245, 145), "IS 13252 (Part 1)", fill=(0, 0, 0))
    d.text((250, 175), "R-41001234", fill=(0, 0, 0))
    d.text((40, 240), "Brand: Dell (Dell India Private Limited)", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_05_dell_laptop_crs.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_05_dell_laptop_crs.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 31. Samsung Phone Box CRS
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "SAMSUNG GALAXY SMARTPHONE", "CRS ELECTRONICS REGISTRATION", 650)
    d.rectangle([(230, 110), (420, 210)], outline=(0, 0, 0), width=3)
    d.text((305, 120), "CRS", fill=(0, 0, 0))
    d.text((250, 175), "R-41023456", fill=(0, 0, 0))
    d.text((40, 240), "Manufacturer: Samsung India Electronics Pvt Ltd", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_06_samsung_phone_crs.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_06_samsung_phone_crs.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 32. Gold Necklace Hallmark HUID AB12CD
    img = Image.new("RGB", (650, 650), (255, 250, 230))
    d = ImageDraw.Draw(img)
    draw_header(d, "TANISHQ 22K GOLD JEWELLERY CERTIFICATE", "MANDATORY BIS GOLD HALLMARK & LASER HUID", 650, bg_color=(255, 235, 180), text_color=(120, 80, 0))
    # Draw hallmark triangle
    d.polygon([(325, 110), (250, 220), (400, 220)], outline=(120, 80, 0), width=4)
    d.text((310, 160), "BIS", fill=(120, 80, 0))
    d.text((280, 240), "22K916", fill=(0, 0, 0))
    d.text((250, 275), "HUID: AB12CD", fill=(0, 0, 0))
    d.text((40, 340), "Jeweller: Tanishq (Titan Company Limited)", fill=(0, 0, 0))
    d.text((40, 370), "Assaying Center: National Gold Assaying & Hallmarking Centre", fill=(0, 0, 0))
    d.text((40, 400), "Standard: IS 1417:2016  |  Statutory Lifetime Hallmark", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_07_gold_necklace_huid.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_07_gold_necklace_huid.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 33. Gold Bangles Hallmark HUID HG789K
    img = Image.new("RGB", (650, 650), (255, 250, 230))
    d = ImageDraw.Draw(img)
    draw_header(d, "KALYAN JEWELLERS GOLD HALLMARK CERTIFICATE", "18K GOLD JEWELLERY HUID", 650, bg_color=(255, 235, 180))
    d.polygon([(325, 110), (250, 220), (400, 220)], outline=(120, 80, 0), width=4)
    d.text((310, 160), "BIS", fill=(120, 80, 0))
    d.text((280, 240), "18K750", fill=(0, 0, 0))
    d.text((250, 275), "HUID: HG789K", fill=(0, 0, 0))
    d.text((40, 340), "Jeweller: Kalyan Jewellers India Limited", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_08_gold_bangles_huid.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_08_gold_bangles_huid.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 34. Gold Ring Hallmark HUID PR44X9
    img = Image.new("RGB", (650, 650), (255, 250, 230))
    d = ImageDraw.Draw(img)
    draw_header(d, "MALABAR GOLD & DIAMONDS CERTIFICATE", "20K GOLD HALLMARK HUID", 650, bg_color=(255, 235, 180))
    d.polygon([(325, 110), (250, 220), (400, 220)], outline=(120, 80, 0), width=4)
    d.text((310, 160), "BIS", fill=(120, 80, 0))
    d.text((280, 240), "20K833", fill=(0, 0, 0))
    d.text((250, 275), "HUID: PR44X9", fill=(0, 0, 0))
    d.text((40, 340), "Jeweller: Malabar Gold and Diamonds", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_09_gold_ring_huid.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_09_gold_ring_huid.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 35. Maggi FSSAI Lic. No. 10012011000168
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "NESTLE INDIA STATUTORY FOOD SAFETY LABEL", "FSSAI CENTRAL FOOD BUSINESS OPERATOR LICENSE", 650)
    d.rectangle([(200, 120), (450, 200)], outline=(0, 100, 0), width=3)
    d.text((300, 135), "fssai", fill=(0, 100, 0))
    d.text((220, 165), "Lic. No. 10012011000168", fill=(0, 0, 0))
    d.text((40, 240), "Manufacturer: Nestle India Limited (Central License)", fill=(0, 0, 0))
    d.text((40, 270), "Product: Maggi 2-Minute Noodles Instant Food", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_10_maggi_fssai.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_10_maggi_fssai.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 36. MyFitness FSSAI Lic. No. 10020021000488
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "TANVI FITNESS / MYFITNESS FOOD LABEL", "FSSAI FOSCOS STATUTORY CENTRAL LICENSE", 650)
    d.rectangle([(170, 120), (490, 200)], outline=(0, 100, 0), width=3)
    d.text((300, 135), "fssai", fill=(0, 100, 0))
    d.text((185, 165), "FSSAI Lic. No. 10020021000488", fill=(0, 0, 0))
    d.text((40, 240), "Company: Tanvi Fitness Private Limited, Gujarat", fill=(0, 0, 0))
    d.text((40, 270), "Product: MYFITNESS Peanut Butter Spread", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_11_myfitness_fssai.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_11_myfitness_fssai.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 37. Dettol Soap GS1 EAN-13 Barcode 8901396112203
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "DETTOL ORIGINAL SOAP RETAIL CARTON", "GS1 INDIA STATUTORY GTIN-13 BARCODE", 650)
    d.text((40, 110), "Brand: Dettol (Reckitt Benckiser India)", fill=(0, 0, 0))
    d.text((40, 140), "Product: Dettol Antiseptic Bathing Soap 125g", fill=(0, 0, 0))
    draw_barcode_bars(d, 180, 220, 280, 120, "8901396112203")
    path = os.path.join(DATASET_DIR, "mark_12_dettol_barcode.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_12_dettol_barcode.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": True})

    # 38. Fake ISI Mark (No CM/L number)
    img = Image.new("RGB", (650, 650), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_header(d, "COUNTERFEIT PRODUCT PACKAGING", "UNAUTHORIZED TRADEMARK USE", 650, bg_color=(255, 220, 220), text_color=(180, 0, 0))
    d.ellipse([(250, 120), (400, 240)], outline=(180, 0, 0), width=4)
    d.text((305, 160), "ISI", fill=(180, 0, 0))
    d.text((230, 260), "100% ISI STANDARD", fill=(180, 0, 0))
    d.text((40, 320), "ALERT: MISSING STATUTORY CM/L NUMBER!", fill=(200, 0, 0))
    d.text((40, 350), "Under Section 29 BIS Act 2016, printing ISI without valid CM/L is illegal.", fill=(0, 0, 0))
    path = os.path.join(DATASET_DIR, "mark_13_fake_isi_no_cml.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "mark_13_fake_isi_no_cml.jpg", "category": "mark_check", "expected_relevant": True, "expected_valid": False})

    # =========================================================================
    # CATEGORY 4: IRRELEVANT & OUT-OF-SCOPE IMAGES (12 images)
    # =========================================================================

    # 39. Sports Car (Red Automobile)
    img = Image.new("RGB", (700, 500), (240, 240, 245))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(220, 40, 40))
    d.text((20, 20), "AUTOMOBILE / VEHICLE: FERRARI RED SPORTS CAR", fill=(255, 255, 255))
    # Draw car chassis
    d.polygon([(100, 350), (120, 260), (220, 220), (480, 220), (580, 270), (620, 350)], fill=(220, 30, 30))
    # Car cabin
    d.polygon([(240, 220), (280, 160), (440, 160), (470, 220)], fill=(30, 40, 50))
    # Wheels
    d.ellipse([(180, 330), (260, 410)], fill=(20, 20, 20))
    d.ellipse([(200, 350), (240, 390)], fill=(150, 150, 150))
    d.ellipse([(450, 330), (530, 410)], fill=(20, 20, 20))
    d.ellipse([(470, 350), (510, 390)], fill=(150, 150, 150))
    d.text((150, 440), "V8 Twin Turbo Engine | 320 km/h Top Speed | Carbon Fiber Chassis", fill=(50, 50, 50))
    path = os.path.join(DATASET_DIR, "irrel_01_sports_car.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_01_sports_car.jpg", "category": "irrelevant", "expected_relevant": False})

    # 40. SUV Vehicle
    img = Image.new("RGB", (700, 500), (230, 240, 250))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(40, 70, 110))
    d.text((20, 20), "AUTOMOTIVE TRANSPORT: TOYOTA FORTUNER SUV 4X4", fill=(255, 255, 255))
    d.polygon([(80, 360), (100, 250), (200, 180), (550, 180), (620, 260), (640, 360)], fill=(50, 80, 130))
    d.ellipse([(160, 330), (250, 420)], fill=(30, 30, 30))
    d.ellipse([(470, 330), (560, 420)], fill=(30, 30, 30))
    d.text((120, 440), "Diesel 4-Cylinder Engine | All-Wheel Drive | Highway Off-Road Vehicle", fill=(60, 60, 60))
    path = os.path.join(DATASET_DIR, "irrel_02_suv_vehicle.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_02_suv_vehicle.jpg", "category": "irrelevant", "expected_relevant": False})

    # 41. Car Engine & Transmission
    img = Image.new("RGB", (700, 500), (220, 220, 220))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(60, 60, 60))
    d.text((20, 20), "INTERNAL COMBUSTION AUTOMOTIVE CAR ENGINE (V6)", fill=(255, 255, 255))
    d.rectangle([(150, 120), (550, 380)], fill=(90, 95, 100), outline=(40, 40, 40), width=4)
    d.text((180, 160), "Cylinder Head | Camshaft | Pistons | Fuel Injectors", fill=(255, 255, 255))
    d.text((180, 220), "Transmission Gearbox | Alternator | Radiator Hose", fill=(255, 255, 255))
    d.text((180, 280), "Engine Displacement: 3.5 Liters | Horsepower: 295 HP", fill=(255, 255, 255))
    path = os.path.join(DATASET_DIR, "irrel_03_car_engine.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_03_car_engine.jpg", "category": "irrelevant", "expected_relevant": False})

    # 42. Motorcycle
    img = Image.new("RGB", (700, 500), (245, 245, 245))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(20, 120, 60))
    d.text((20, 20), "TWO-WHEELER VEHICLE: KAWASAKI NINJA MOTORCYCLE", fill=(255, 255, 255))
    d.ellipse([(100, 300), (220, 420)], fill=(20, 20, 20))
    d.ellipse([(480, 300), (600, 420)], fill=(20, 20, 20))
    d.polygon([(180, 340), (320, 250), (450, 250), (520, 340)], fill=(30, 180, 60))
    d.text((180, 440), "Superbike | 650cc Parallel-Twin Engine | Dual Disc Brakes", fill=(40, 40, 40))
    path = os.path.join(DATASET_DIR, "irrel_04_motorcycle.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_04_motorcycle.jpg", "category": "irrelevant", "expected_relevant": False})

    # 43. Domestic Pet Dog
    img = Image.new("RGB", (700, 500), (250, 240, 230))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(180, 120, 60))
    d.text((20, 20), "DOMESTIC ANIMAL / PET: GOLDEN RETRIEVER DOG", fill=(255, 255, 255))
    # Draw dog head
    d.ellipse([(250, 140), (450, 340)], fill=(220, 170, 100))
    d.polygon([(230, 150), (200, 250), (260, 220)], fill=(180, 130, 70))
    d.polygon([(470, 150), (500, 250), (440, 220)], fill=(180, 130, 70))
    d.ellipse([(290, 200), (320, 230)], fill=(0, 0, 0))
    d.ellipse([(380, 200), (410, 230)], fill=(0, 0, 0))
    d.ellipse([(335, 250), (365, 280)], fill=(0, 0, 0))
    d.text((220, 400), "Friendly companion animal, playful outdoor canine.", fill=(80, 60, 40))
    path = os.path.join(DATASET_DIR, "irrel_05_pet_dog.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_05_pet_dog.jpg", "category": "irrelevant", "expected_relevant": False})

    # 44. Domestic Pet Cat
    img = Image.new("RGB", (700, 500), (240, 245, 250))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(120, 100, 160))
    d.text((20, 20), "DOMESTIC FELINE: PERSIAN CAT PORTRAIT", fill=(255, 255, 255))
    d.ellipse([(250, 160), (450, 340)], fill=(240, 240, 240), outline=(150, 150, 150))
    d.polygon([(260, 180), (280, 110), (320, 170)], fill=(220, 180, 180))
    d.polygon([(380, 170), (420, 110), (440, 180)], fill=(220, 180, 180))
    d.ellipse([(290, 220), (320, 245)], fill=(50, 150, 100))
    d.ellipse([(380, 220), (410, 245)], fill=(50, 150, 100))
    d.text((230, 400), "Fluffy white domestic kitten pet resting.", fill=(70, 70, 90))
    path = os.path.join(DATASET_DIR, "irrel_06_pet_cat.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_06_pet_cat.jpg", "category": "irrelevant", "expected_relevant": False})

    # 45. Mountain Landscape / Scenery
    img = Image.new("RGB", (700, 500), (180, 220, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(50, 110, 180))
    d.text((20, 20), "NATURAL SCENERY: HIMALAYAN MOUNTAIN LANDSCAPE", fill=(255, 255, 255))
    d.ellipse([(520, 90), (600, 170)], fill=(255, 230, 80))  # Sun
    d.polygon([(50, 450), (220, 180), (380, 450)], fill=(120, 130, 140))  # Mountain 1
    d.polygon([(260, 450), (420, 140), (600, 450)], fill=(150, 160, 170))  # Mountain 2
    d.rectangle([(0, 420), (700, 500)], fill=(60, 140, 60))  # Grass
    d.text((180, 460), "Peaceful nature, blue skies, snow peaks, pine trees.", fill=(255, 255, 255))
    path = os.path.join(DATASET_DIR, "irrel_07_mountain_landscape.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_07_mountain_landscape.jpg", "category": "irrelevant", "expected_relevant": False})

    # 46. Garden Flower
    img = Image.new("RGB", (700, 500), (255, 245, 245))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(200, 60, 100))
    d.text((20, 20), "BOTANICAL NATURE: RED ROSE GARDEN BLOSSOM", fill=(255, 255, 255))
    d.ellipse([(280, 180), (420, 320)], fill=(220, 30, 70))
    d.ellipse([(320, 220), (380, 280)], fill=(160, 20, 50))
    d.text((220, 400), "Fresh blooming flower petal, botanical gardening.", fill=(80, 40, 50))
    path = os.path.join(DATASET_DIR, "irrel_08_flower_nature.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_08_flower_nature.jpg", "category": "irrelevant", "expected_relevant": False})

    # 47. Human Portrait / Selfie
    img = Image.new("RGB", (700, 500), (240, 230, 220))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(70, 70, 90))
    d.text((20, 20), "HUMAN PORTRAIT: PERSON SMARTPHONE SELFIE", fill=(255, 255, 255))
    d.ellipse([(280, 140), (420, 300)], fill=(235, 195, 165))
    d.text((230, 380), "Individual profile picture, personal photograph.", fill=(60, 60, 60))
    path = os.path.join(DATASET_DIR, "irrel_09_human_portrait.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_09_human_portrait.jpg", "category": "irrelevant", "expected_relevant": False})

    # 48. Programming Code Screenshot
    img = Image.new("RGB", (700, 500), (30, 30, 40))
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (700, 60)], fill=(20, 20, 30))
    d.text((20, 20), "COMPUTER SOFTWARE SOURCE CODE (PYTHON & REACT)", fill=(0, 200, 255))
    code_lines = [
        "import numpy as np",
        "import pandas as pd",
        "def compute_matrix(x, y):",
        "    return np.dot(x.T, y) + np.random.randn(10, 10)",
        "class DataPipeline:",
        "    def __init__(self, endpoint):",
        "        self.url = 'https://api.github.com/repos'"
    ]
    y = 100
    for cl in code_lines:
        d.text((40, y), cl, fill=(180, 220, 150))
        y += 35
    path = os.path.join(DATASET_DIR, "irrel_10_coding_screen.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_10_coding_screen.jpg", "category": "irrelevant", "expected_relevant": False})

    # 49. Blank White Image
    img = Image.new("RGB", (700, 500), (255, 255, 255))
    path = os.path.join(DATASET_DIR, "irrel_11_blank_white.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_11_blank_white.jpg", "category": "irrelevant", "expected_relevant": False})

    # 50. Abstract Noise Texture
    img = Image.new("RGB", (700, 500), (120, 120, 140))
    d = ImageDraw.Draw(img)
    for i in range(0, 700, 30):
        for j in range(0, 500, 30):
            d.rectangle([(i, j), (i + 15, j + 15)], fill=((i * 3) % 255, (j * 4) % 255, ((i + j) * 2) % 255))
    path = os.path.join(DATASET_DIR, "irrel_12_abstract_noise.jpg")
    img.save(path, quality=92)
    manifest.append({"file": "irrel_12_abstract_noise.jpg", "category": "irrelevant", "expected_relevant": False})

    # Save manifest
    manifest_path = os.path.join(DATASET_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSuccessfully generated all {len(manifest)} test images in: {DATASET_DIR}")
    print(f"Manifest written to: {manifest_path}")

if __name__ == "__main__":
    generate_all_images()
