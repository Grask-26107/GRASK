import urllib.request
import json
import base64
import io
import time
import sys
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_simple_barcode_image(ean13_code: str) -> str:
    """Generates an in-memory synthetic barcode image with alternating stripes for test verification."""
    # We can create a real barcode using standard EAN-13 binary patterns
    # Or test zxingcpp with a real drawn EAN-13
    # EAN-13 encoding tables
    L_CODE = ["0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011"]
    G_CODE = ["0100111", "0110011", "0011011", "0100001", "0011101", "0111001", "0000101", "0010001", "0001001", "0010111"]
    R_CODE = ["1110010", "1100110", "1101100", "1000010", "1011100", "1001110", "1010000", "1000100", "1001000", "1110100"]
    FIRST_GROUP = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]

    first_digit = int(ean13_code[0])
    pattern = FIRST_GROUP[first_digit]
    
    # Start guard: 101
    modules = "101"
    
    # First 6 digits
    for i in range(6):
        digit = int(ean13_code[1 + i])
        encoding = pattern[i]
        modules += L_CODE[digit] if encoding == "L" else G_CODE[digit]
        
    # Center guard: 01010
    modules += "01010"
    
    # Last 6 digits (R-codes)
    for i in range(6):
        digit = int(ean13_code[7 + i])
        modules += R_CODE[digit]
        
    # End guard: 101
    modules += "101"
    
    # Render into PIL image
    module_width = 3
    height = 100
    quiet_zone = 30
    total_width = len(modules) * module_width + (quiet_zone * 2)
    
    img = Image.new('RGB', (total_width, height + 40), color='white')
    draw = ImageDraw.Draw(img)
    
    x = quiet_zone
    for bit in modules:
        if bit == "1":
            draw.rectangle([x, 15, x + module_width - 1, 15 + height], fill='black')
        x += module_width
        
    # Convert to base64
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=95)
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return b64

def test_hybrid_scanner():
    print("=" * 90)
    print("🚀 TESTING HYBRID DUAL-CHANNEL BARCODE & TEXT SCANNER LIVE")
    print("=" * 90)
    
    # Test Case 1: Pure Optical Barcode Stripes (Image Only, NO TEXT provided)
    print("\n--- TEST CASE 1: Pure Barcode Stripes (Image Only, Zero Text) ---")
    patanjali_b64 = generate_simple_barcode_image("8906056351467")
    payload1 = {
        "text": "", # Intentionally blank text
        "image_base64": patanjali_b64
    }
    t0 = time.time()
    req = urllib.request.Request(
        "http://localhost:8000/api/v1/standards/ocr-extract",
        data=json.dumps(payload1).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req, timeout=10)
    dt = (time.time() - t0) * 1000
    data = json.loads(res.read().decode('utf-8'))
    
    v = data.get("verification", {})
    h = data.get("hybrid_summary", {})
    print(f"Latency: {dt:.1f}ms")
    print(f"Decoded Barcode from Stripes: {h.get('barcode_from_stripes')}")
    print(f"Consensus Barcode:           {h.get('consensus_barcode')}")
    print(f"Hybrid Match Status:         {h.get('hybrid_match_status')}")
    print(f"Brand Name:                  {v.get('brand_name')}")
    print(f"Parent Company:              {v.get('parent_company')}")
    print(f"Product Title:               {v.get('product_name')}")
    print(f"License Type:                {v.get('license_type')}")
    print(f"Checksum Valid:              {h.get('checksum_valid')}")
    
    assert h.get("barcode_from_stripes") == "8906056351467", "Optical decoding failed!"
    assert "Patanjali" in str(v.get("brand_name")), "Brand resolution failed!"
    print("✅ TEST 1 PASSED: Optical Barcode Stripes decoded & Patanjali details resolved!")

    # Test Case 2: Noisy OCR Text (Floating '8' missing, guard bar noise)
    print("\n--- TEST CASE 2: Noisy OCR Text (Missing floating 8: '906056351467') ---")
    payload2 = {
        "text": "Manufactured by Patanjali. Barcode: 906056351467 Net Qty: 500ml",
        "image_base64": None
    }
    t0 = time.time()
    req = urllib.request.Request(
        "http://localhost:8000/api/v1/standards/ocr-extract",
        data=json.dumps(payload2).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req, timeout=10)
    dt = (time.time() - t0) * 1000
    data = json.loads(res.read().decode('utf-8'))
    
    v = data.get("verification", {})
    h = data.get("hybrid_summary", {})
    print(f"Latency: {dt:.1f}ms")
    print(f"Consensus Barcode:           {h.get('consensus_barcode')}")
    print(f"Hybrid Match Status:         {h.get('hybrid_match_status')}")
    print(f"Brand Name:                  {v.get('brand_name')}")
    print(f"Checksum Valid:              {h.get('checksum_valid')}")
    
    assert h.get("consensus_barcode") == "8906056351467", "OCR detached digit repair failed!"
    print("✅ TEST 2 PASSED: Missing leading 8 auto-recovered and verified!")

    # Test Case 3: Dual Channel Full Consensus (Image + Text)
    print("\n--- TEST CASE 3: Dual Channel Consensus (boAt Nirvana 8905650102321) ---")
    boat_b64 = generate_simple_barcode_image("8905650102321")
    payload3 = {
        "text": "boAt Nirvana Ivy Pro True Wireless Earbuds Barcode: 8905650102321 R-41292958",
        "image_base64": boat_b64
    }
    t0 = time.time()
    req = urllib.request.Request(
        "http://localhost:8000/api/v1/standards/ocr-extract",
        data=json.dumps(payload3).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req, timeout=10)
    dt = (time.time() - t0) * 1000
    data = json.loads(res.read().decode('utf-8'))
    
    v = data.get("verification", {})
    h = data.get("hybrid_summary", {})
    print(f"Latency: {dt:.1f}ms")
    print(f"Decoded from Stripes:        {h.get('barcode_from_stripes')}")
    print(f"Decoded from Text:           {h.get('barcode_from_text')}")
    print(f"Hybrid Consensus Status:     {h.get('hybrid_match_status')}")
    print(f"Brand Name:                  {v.get('brand_name')}")
    print(f"Parent Company:              {v.get('parent_company')}")
    print(f"Governing Standard:          {v.get('standard_code')}")
    print(f"License Type:                {v.get('license_type')}")
    
    assert h.get("barcode_from_stripes") == "8905650102321", "Optical decoding failed for boAt!"
    assert "PERFECT_MATCH" in h.get("hybrid_match_status"), "Cross-verification consensus failed!"
    assert "boAt" in str(v.get("brand_name")), "boAt Brand resolution failed!"
    print("✅ TEST 3 PASSED: Dual-Channel Perfect Match & boAt details verified!")

    print("\n" + "=" * 90)
    print("🎉 ALL HYBRID DUAL-CHANNEL TESTS PASSED 100%!")
    print("=" * 90)

if __name__ == '__main__':
    test_hybrid_scanner()
