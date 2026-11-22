import shutil


def check_disk_health(path='/', max_usage_percent=85.0):
    """Belirtilen dizinin disk doluluk oranını kontrol eder
    """
    total, used, free = shutil.disk_usage(path)

    usage_percent = (used / total) * 100

    is_healthy = usage_percent < max_usage_percent

    return {
        "path": path,
        "usage_percent": round(usage_percent, 2),
        "is_healthy": is_healthy,
        "free_gb": round(free / (1024 ** 3), 2),
    }
