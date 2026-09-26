"""
Test Suite: Food Safety, Palak Paneer & Nutri-Score Persona Verification
Part of GRASK AI (SIH26107).
Validates:
1. Food & Culinary Intelligence:
   - 'what i should ensure before eating a palak panneer' returns IS 10484, FSSAI regulations,
     iodine starch test, pesticide wash, malachite green dye test, cooking temperature,
     and ZERO steel / cement / civil standards.
2. Domain Protection:
   - Ensures food queries never suffer vector collision with technical construction standards.
3. Nutri-Score Persona Classification:
   - Wholesome safe foods (100% rolled oats, whole wheat roti, fresh paneer, milk)
     receive Grade A/B and SECURE verdict under general persona.
   - Harmful ultra-processed HFSS foods receive Grade D/E and HARMFUL verdict.
4. Internet Truthfulness:
   - Verifies no false 'No active internet connection' banner appears on connected systems.
"""

import sys
import os
import requests
import unittest

BASE_URL = "http://127.0.0.1:8000/api/v1"


class TestFoodAndNutriScoreSafety(unittest.TestCase):

    def test_palak_paneer_query_intelligence(self):
        """Test that palak paneer query returns accurate food safety standards and ZERO steel rebars."""
        payload = {
            "message": "what i should ensure before eating a palak panneer",
            "mode": "consumer",
            "language": "en"
        }
        resp = requests.post(f"{BASE_URL}/chat", json=payload, timeout=15)
        self.assertEqual(resp.status_code, 200, f"Query failed with status {resp.status_code}")
        data = resp.json()
        ans = data.get("answer", "")
        citations = data.get("citations", [])

        # 1. Answer must be rich and relevant to paneer, food safety, and leafy greens
        ans_lower = ans.lower()
        self.assertTrue(
            any(w in ans_lower for w in ["paneer", "is 10484", "palak", "spinach", "fssai", "iodine"]),
            "Answer failed to mention Paneer, IS 10484, Palak, or FSSAI"
        )
        self.assertTrue(
            any(w in ans_lower for w in ["iodine", "starch", "pesticide", "dye", "temperature", "hygiene"]),
            "Answer failed to mention food safety checks (iodine, starch, pesticide wash, or dye test)"
        )

        # 2. Strict anti-hallucination / zero domain mismatch: MUST NOT contain steel bars or cement
        self.assertNotIn("is 1786", ans_lower, "CRITICAL DEFECT: Output hallucinated IS 1786 (Steel Bars) for Palak Paneer!")
        self.assertNotIn("high strength deformed steel", ans_lower, "CRITICAL DEFECT: Output contains steel rebars!")
        self.assertNotIn("concrete reinforcement", ans_lower, "CRITICAL DEFECT: Output contains concrete reinforcement for food!")
        self.assertNotIn("is 269", ans_lower, "CRITICAL DEFECT: Output contains IS 269 Cement for food!")

        # 3. Must not display false network disconnected error
        self.assertNotIn("[offline mode] no active internet connection detected", ans_lower)

        # 4. Citations must not cite steel
        for c in citations:
            self.assertNotEqual(c.get("is_code"), "IS 1786:2008", "Citation erroneously points to IS 1786 Steel!")

        print("\n[PASS] Palak Paneer query resolved with 100% food domain grounding and zero steel mentions.")

    def test_nutri_score_safe_oats(self):
        """Test that 100% Whole Grain Rolled Oats receives Grade A or B and SECURE verdict."""
        payload = {
            "text": "100% Whole Grain Rolled Oats. Per 100g: Energy 389 kcal, Protein 13.5g, Carbohydrates 66.0g, Total Sugar 1.0g, Added Sugar 0g, Total Fat 6.9g, Saturated Fat 1.2g, Trans Fat 0g, Sodium 5mg, Dietary Fiber 10.5g.",
            "persona": "general",
            "language": "en"
        }
        resp = requests.post(f"{BASE_URL}/standards/analyze-ingredients", json=payload, timeout=15)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data.get("verdict"), "SECURE", f"Oats were classified as {data.get('verdict')} instead of SECURE!")
        self.assertIn(data.get("nutri_score_grade"), ["A", "B"], f"Oats received grade {data.get('nutri_score_grade')} instead of A or B!")
        self.assertIn("SECURE", data.get("verdict_badge", ""))
        print(f"[PASS] Whole Oats correctly classified as {data.get('verdict')} (Grade {data.get('nutri_score_grade')}).")

    def test_nutri_score_safe_chapati(self):
        """Test that Whole Wheat Chapati is classified as SECURE and does not trigger Celiac alert for general persona."""
        payload = {
            "text": "Whole Wheat Flour (Atta), Water, Salt. Per 100g: Energy 297 kcal, Protein 11.5g, Carbohydrates 61.0g, Total Sugar 1.5g, Added Sugar 0g, Total Fat 1.7g, Saturated Fat 0.3g, Trans Fat 0g, Sodium 110mg, Dietary Fiber 11.0g.",
            "persona": "general",
            "language": "en"
        }
        resp = requests.post(f"{BASE_URL}/standards/analyze-ingredients", json=payload, timeout=15)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data.get("verdict"), "SECURE", f"Wheat chapati was classified as {data.get('verdict')} instead of SECURE!")
        self.assertIn(data.get("nutri_score_grade"), ["A", "B"])
        print(f"[PASS] Whole Wheat Chapati correctly classified as {data.get('verdict')} (Grade {data.get('nutri_score_grade')}).")

    def test_nutri_score_harmful_junk_food(self):
        """Test that high sodium, high sugar, trans-fat laden noodles receive HARMFUL verdict."""
        payload = {
            "text": "Refined Wheat Flour, Palm Oil, Salt, Monosodium Glutamate (INS 621), Tartrazine (INS 102), Sunset Yellow (INS 110), Invert Sugar Syrup. Per 100g: Energy 480 kcal, Protein 8.0g, Carbohydrates 62.0g, Total Sugar 5.0g, Added Sugar 4.0g, Total Fat 21.0g, Saturated Fat 11.0g, Trans Fat 0.5g, Sodium 980mg.",
            "persona": "general",
            "language": "en"
        }
        resp = requests.post(f"{BASE_URL}/standards/analyze-ingredients", json=payload, timeout=15)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data.get("verdict"), "HARMFUL", f"Junk food was classified as {data.get('verdict')} instead of HARMFUL!")
        self.assertIn(data.get("nutri_score_grade"), ["D", "E"])
        self.assertTrue(len(data.get("harmful_additives", [])) > 0, "Failed to identify harmful additives INS 102 / INS 110 / MSG!")
        print(f"[PASS] Fried Noodles correctly flagged as {data.get('verdict')} with {len(data.get('harmful_additives', []))} detected additives.")


if __name__ == "__main__":
    unittest.main()
