import uuid

from django.core.cache import cache


def generate_and_store_otp(user):
    otp = uuid.uuid4()
    cache_key = f"otp_{user.id}"
    cache.set(cache_key, str(otp), timeout=300)  # OTP expires in 5 minutes (300 seconds)
    return otp
