from urllib import request
import redis
import json
from .models import Products
from .serializers import ProductsSerializer
import logging

# Connect to Redis
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
logger = logging.getLogger(__name__)
CACHE_KEY = 'products'


def get_products():
    try:
        cached = r.get(CACHE_KEY)
        if cached:
            return json.loads(cached)
    except Exception as e:
        # Log or print the error (optional)
        print(f"Redis GET failed: {e}")

    # Fallback to DB if Redis fails or cache miss
    try:
        product = Products.objects.all()
        serializer = ProductsSerializer(product, many=True)
        data = serializer.data
        try:
            r.set(CACHE_KEY, json.dumps(data), ex=3600)
        except Exception as e:
            print(f"Redis SET failed: {e}")
        return data
    except Exception as e:
        print(f"DB fetch failed: {e}")
        return []  # return empty list if DB also fails



def get_product_by_user(user_id):
    
    CACHE_KEY = f'products_by_user_{user_id}'
    
    # Try Redis cache first
    try:
        cached = r.get(CACHE_KEY)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.error(f"Redis GET failed: {e}")

    # Fallback to DB
    try:
        products = Products.objects.filter(user_id=user_id)
        serializer = ProductsSerializer(products, many=True)
        data = serializer.data
        
        # Store in Redis
        try:
            r.set(CACHE_KEY, json.dumps(data), ex=3600)
        except Exception as e:
            logger.error(f"Redis SET failed: {e}")
        
        return data
    except Exception as e:
        logger.error(f"DB fetch failed: {e}")
        return []



def clear_cache():
    try:
        r.delete(CACHE_KEY)
    except Exception as e:
        print(f"Redis DELETE failed: {e}")
