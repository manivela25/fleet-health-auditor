import logging
import threading
from concurrent.futures import ThreadPoolExecutor


class FleetAuditor:
    """4 Modülün tüm tekniklerini birleştiren paralel ve dayanıklı denetim motoru."""

    def __init__(self, blacklisted_plates, max_history=100, max_workers=4):
        # 1. MODÜL 2 (Hız): blacklisted_plates listesini set'e çevir
        self.blacklisted_set = set(blacklisted_plates)  # <-- BURAYI DOLDUR

        self.max_history = max_history
        self.max_workers = max_workers
        self.cache = {}
        self.recent_history = []
        self.lock = threading.Lock()

    def _audit_single_record(self, record):
        """Tek bir GPS/sefer kaydını güvenli, önbellekli ve kilitli şekilde denetler."""
        # 2. MODÜL 1 (Kapı Güvenliği): record boş veya None ise None döndür
        # <-- BURAYI DOLDUR
        if not record:
            return None

        try:
            plate = record["plate"].strip().upper()
            delay_min = int(record["delay_min"])
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            logging.error(f"Bozuk kayıt atlandı: {record} | Hata: {e}")
            return None

        # 3. MODÜL 2 (Önbellek & Set Kontrolü):
        # Eğer (plate, delay_min) anahtarı self.cache içinde varsa doğrudan onu döndür!

        cache_key = (plate, delay_min)
        with self.lock:
            if cache_key in self.cache:
                return self.cache[cache_key]

        is_violation = (plate in self.blacklisted_set) and (delay_min > 5)
        result = {
            "plate": plate,
            "delay_min": delay_min,
            "is_violation": is_violation,
        }

        # 4. MODÜL 3 & 4 (Kilitli Güncelleme & Bellek Sızıntısı Koruması):
        # self.lock altında cache'i güncelle, recent_history'ye ekle ve len > self.max_history ise pop(0) yap
        with self.lock:
            self.cache[cache_key] = result
            self.recent_history.append(result)
            if len(self.recent_history) > self.max_history:
                self.recent_history.pop(0)

        return result

    def audit_batch(self, records):
        """Tüm kayıt listesini ThreadPoolExecutor ile paralel olarak denetler."""
        violations = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 5. MODÜL 4 (Paralel İş Dağıtımı):
            # ThreadPoolExecutor(max_workers=self.max_workers) aç ve self._audit_single_record fonksiyonunu records'a map et
            # Dönen sonuçlardan None olmayan ve res["is_violation"] == True olanları violations listesine ekle
            # <-- BURAYI DOLDUR
            for result in executor.map(self._audit_single_record, records):
                if result and result["is_violation"]:
                    violations.append(result)

        return violations
