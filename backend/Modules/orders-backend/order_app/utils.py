import json
from django.core.cache import cache

def is_duplicate_request(idempotency_key):
    return cache.get(idempotency_key) is not None

def save_idempotency_response(idempotency_key, response_data):
    cache.set(idempotency_key, json.dumps(response_data), timeout=3600)

def get_cached_response(idempotency_key):
    data = cache.get(idempotency_key)
    return json.loads(data) if data else None
