# Fleet Health Auditor

Paralel işleme (`ThreadPoolExecutor`), önbellekleme (`set` & `cache`), bellek sınırı koruması ve disk kapasite izleme tekniklerini birleştiren dayanıklı Python denetim aracı.

## Özellikler
- **Hata Toleransı ve Loglama:** Boş veya bozuk formatlı kayıtları uygulamayı çökertmeden yakalar ve loglar.
- **Performans Optimizasyonu:** `O(1)` set araması, sonuç önbellekleme ve `cProfile` darboğaz analizi.
- **Bellek ve Kaynak Yönetimi:** Sabit boyutlu geçmiş tamponu (`max_history`) ve işlem öncesi disk doluluk kontrolü.
- **Eşzamanlılık:** `ThreadPoolExecutor` ile paralel denetim ve `threading.Lock` ile iş parçacığı güvenliği.

## Çalıştırma ve Test
```bash
python3 -m unittest discover -s tests
python3 main.py
