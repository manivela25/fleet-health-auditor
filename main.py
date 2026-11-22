import cProfile
import logging
import pstats

from src.fleet_auditor import FleetAuditor
from src.system_monitor import check_disk_health

logging.basicConfig(
    filename="audit_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_audit():
    disk_status = check_disk_health("/", max_usage_percent=85.0)
    print(f"Disk Durumu: %{disk_status['usage_percent']} dolu ({disk_status['free_gb']} GB boş)")

    if not disk_status["is_healthy"]:
        print("UYARI: Disk kapasitesi kritik seviyede!")

    sample_records = [
        {"plate": f"25 M {i % 50:03d}", "delay_min": (i % 15)}
        for i in range(1000)
    ]
    sample_records.extend([None, {"plate": "25 M 001", "delay_min": "HATALI"}])

    auditor = FleetAuditor(
        blacklisted_plates=["25 M 001", "25 M 005", "25 M 012"],
        max_history=100,
        max_workers=4,
    )

    violations = auditor.audit_batch(sample_records)
    print(f"Toplam {len(sample_records)} kayıt tarandı -> {len(violations)} ihlal tespit edildi.")
    print(f"Önbelleğe alınan benzersiz sorgu sayısı: {len(auditor.cache)}")


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_audit()
    profiler.disable()

    print("\n--- cProfile En Çok Zaman Harcayan İlk 5 Fonksiyon ---")
    stats = pstats.Stats(profiler).sort_stats("tottime")
    stats.print_stats(5)
