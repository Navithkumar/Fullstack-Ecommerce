import redis
import json
from .models import Cart
from .serializers import CartSerializer
from django.conf import settings
from pagination import MyCustomPagination

# Connect Redis (preferably from env vars)
r = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "redis"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=0,
    decode_responses=True
)

def get_cart_cache_key(user_id):
    return f"cart:{user_id}"

def get_cart_items(user_id):
    cache_key = get_cart_cache_key(user_id)
    try:
        cached = r.get(cache_key)
        if cached:
            print(f"Redis HIT for {cache_key}")
            return json.loads(cached)
    except redis.RedisError as e:
        print(f"Redis GET failed: {e}")

    # Fallback: Fetch from DB
    try:
        cart_items = Cart.objects.filter(user_id=user_id)
        serializer = CartSerializer(cart_items, many=True)
        data = serializer.data

        # Cache it for next time
        try:
            r.setex(cache_key, 3600, json.dumps(data))  # expires in 1 hour
            print(f"Redis SET for {cache_key}")
        except redis.RedisError as e:
            print(f"Redis SET failed: {e}")

        return data
    except Exception as e:
        print(f"DB fetch failed: {e}")
        return []

def clear_cache(user_id):
    cache_key = get_cart_cache_key(user_id)
    try:
        r.delete(cache_key)
        print(f"Redis cache cleared for {cache_key}")
    except redis.RedisError as e:
        print(f"Redis DELETE failed: {e}")
