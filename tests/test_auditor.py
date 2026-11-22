import unittest

from src.fleet_auditor import FleetAuditor
from src.system_monitor import check_disk_health


class TestFleetAuditor(unittest.TestCase):

    def setUp(self):
        self.auditor = FleetAuditor(
            blacklisted_plates=["25 AB 101", "25 CD 202"],
            max_history=3,
            max_workers=4,
        )

    def test_valid_and_corrupted_records(self):
        """Modül 1 & 3: Boş veya bozuk kayıtlar programı çökertmeden atlanmalı."""
        records = [
            None,
            {},
            {"plate": "25 AB 101", "delay_min": "12"},  # İhlal (kara listede ve > 5 dk)
            {"plate": "25 AB 101", "delay_min": "3"},  # İhlal değil (<= 5 dk)
            {"plate": "25 XY 999", "delay_min": "20"},  # İhlal değil (kara listede yok)
            {"plate": "25 CD 202", "delay_min": "bozuk_sayi"},  # Hatalı sayı -> loglanıp atlanmalı
        ]
        violations = self.auditor.audit_batch(records)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["plate"], "25 AB 101")

    def test_memory_limit_history(self):
        """Modül 3: Geçmiş listesi max_history sınırını asla aşmamalı."""
        records = [{"plate": f"25 TT {i}", "delay_min": 10} for i in range(10)]
        self.auditor.audit_batch(records)
        self.assertEqual(len(self.auditor.recent_history), 3)

    def test_disk_health_check(self):
        """Modül 4: Disk sağlığı fonksiyonu beklenen anahtarları döndürmeli."""
        report = check_disk_health("/", max_usage_percent=99.9)
        self.assertIn("usage_percent", report)
        self.assertTrue(report["is_healthy"])


if __name__ == "__main__":
    unittest.main()
