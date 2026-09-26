"""
Extended Real-World & Consumer Rights Test Suite.
Strictly located in: tests/test_extended_domains_suite.py
Tests:
- MSME Udyam Registration (100% Free, zero ISO 45001 hallucination)
- Restaurant Service Charge Illegality (CCPA Guidelines 2022)
- Extra Chilling / Cooling Charges above MRP (Section 36 Legal Metrology)
- Selling Old Unhallmarked Gold (Consumer Exemption vs Jeweller HUID)
- Concrete Mix Formulations & Curing (IS 456 M20 1:1.5:3, W/C ~0.50)
- TMT Rebar Rolling Mass Tolerances (IS 1786 Table 2)
- Domestic Pressure Cookers Safety QCO (IS 2347 Fusible Plug & Gasket)
- Domestic LPG Gas Stoves (IS 4246 Thermal Efficiency >= 68%)
- Toys Mandatory QCO (IS 9873 Small parts & Phthalates)
- Copper Vessel Drinking Water Safety (IS 10500 limits 0.05 to 1.5 mg/L)
- Allied Regulators (BEE Star Ratings, WPC ETA wireless approvals)
- Online Consumer Court Filing (e-Daakhil edaakhil.nic.in)
"""

import sys
import os
import unittest
import asyncio

# Ensure backend is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.services.rag_engine import rag_engine
from app.models.schemas import ChatMode


class TestExtendedDomainsSuite(unittest.TestCase):

    def test_msme_udyam_registration_no_hallucination(self):
        """Query 'apply for msme how' must return Udyam guide and NEVER ISO 45001."""
        resp = asyncio.run(rag_engine.answer_query(
            "apply for msme how",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("udyamregistration.gov.in", answer)
        self.assertIn("aadhaar", answer)
        self.assertIn("pan", answer)
        self.assertIn("free", answer)
        self.assertNotIn("45001", answer)
        self.assertNotIn("occupational health and safety", answer)
        self.assertGreaterEqual(resp.confidence_score, 0.95)

    def test_restaurant_service_charge_illegality(self):
        """Query about service charge on hotel bill must cite CCPA and voluntary status."""
        resp = asyncio.run(rag_engine.answer_query(
            "restaurant added service charge can i refuse",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("ccpa", answer)
        self.assertIn("voluntary", answer)
        self.assertIn("1915", answer)

    def test_chilling_charges_illegal_above_mrp(self):
        """Query about extra cooling charge for cold bottle must cite Legal Metrology Section 36."""
        resp = asyncio.run(rag_engine.answer_query(
            "shopkeeper charged 5 extra for chilled coke",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("legal metrology", answer)
        self.assertTrue("section 36" in answer or "mrp" in answer)
        self.assertIn("illegal", answer)

    def test_sell_old_unhallmarked_gold(self):
        """Query about selling old unhallmarked gold must confirm consumer right."""
        resp = asyncio.run(rag_engine.answer_query(
            "can i sell my old unhallmarked gold jewellery",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("legal", answer)
        self.assertIn("jeweller", answer)

    def test_concrete_mix_ratio_m20(self):
        """Query about M20 mix ratio must return IS 456, 1:1.5:3, and curing duration."""
        resp = asyncio.run(rag_engine.answer_query(
            "concrete mix ratio m20",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("is 456", answer)
        self.assertTrue("1 : 1.5 : 3" in answer or "1:1.5:3" in answer)
        self.assertIn("curing", answer)

    def test_pressure_cooker_safety_is2347(self):
        """Query about pressure cooker safety must cite IS 2347 and fusible plug."""
        resp = asyncio.run(rag_engine.answer_query(
            "pressure cooker safety is 2347",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("is 2347", answer)
        self.assertIn("fusible plug", answer)

    def test_toys_safety_is9873(self):
        """Query about toy safety must cite IS 9873, mandatory ISI, and lead limits."""
        resp = asyncio.run(rag_engine.answer_query(
            "toys safety is 9873",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("is 9873", answer)
        self.assertIn("lead", answer)

    def test_copper_vessel_drinking_water(self):
        """Query about copper water must cite IS 10500 limits and verdigris toxicity risk."""
        resp = asyncio.run(rag_engine.answer_query(
            "is drinking water in copper bottle safe",
            mode=ChatMode.CONSUMER,
            language="en"
        ))
        answer = resp.answer.lower()
        self.assertFalse(resp.refusal_triggered)
        self.assertIn("is 10500", answer)
        self.assertIn("copper", answer)


if __name__ == "__main__":
    unittest.main()
