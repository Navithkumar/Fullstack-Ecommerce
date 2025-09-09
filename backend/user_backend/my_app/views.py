from django.http import HttpResponse

from django.http import JsonResponse

def hello(request):
    return JsonResponse({"message": "Hello navith test"})

