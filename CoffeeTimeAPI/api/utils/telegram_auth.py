# api/utils/telegram_auth.py
import hashlib
import hmac
from urllib.parse import parse_qsl
from django.conf import settings


def verify_telegram_auth(init_data: str) -> bool:
    """
    Проверяет подпись строки initData, полученной от Telegram WebApp.
    Алгоритм соответствует документации Telegram
    """
    # 1. Разбираем init_data в словарь, сохраняя порядок
    parsed = dict(parse_qsl(init_data, strict_parsing=True))
    # 2. Вытаскиваем пришедший hash
    hash_received = parsed.pop('hash', None)
    if not hash_received:
        return False

    # 3. Формируем data_check_string: сортируем ключи и соединяем через "\n"
    data_check_pairs = sorted(parsed.items(), key=lambda kv: kv[0])
    data_check_string = "\n".join(f"{k}={v}" for k, v in data_check_pairs)

    # 4. Секретный ключ: HMAC‑SHA256 от токена бота
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=settings.TELEGRAM_BOT_TOKEN.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()

    # 5. Вычисляем HMAC‑SHA256 от data_check_string
    calc_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # 6. Сравниваем (регистронезависимо)
    return calc_hash.lower() == hash_received.lower()
