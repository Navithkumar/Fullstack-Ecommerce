import redis
import json
from .models import Category
from .serializers import CategorySerializer

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

CACHE_KEY = 'categories'

def get_categories():
    cached = r.get(CACHE_KEY)
    if cached:
        return json.loads(cached)
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    data = serializer.data
    r.set(CACHE_KEY, json.dumps(data), ex=3600)  # cache for 1 hour
    return data

def clear_cache():
    r.delete(CACHE_KEY)
