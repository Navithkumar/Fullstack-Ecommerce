from rest_framework.response import Response

def success_response(message, data=None, status=200):
    return Response({
        "is_v1":True,
        'status': 'success',
        'message': message,
        'data': data
    }, status=status)

def error_response(message, errors=None, status=400):
    return Response({
        "is_v1":True,
        'status': 'error',
        'message': message,
        'errors': errors
    }, status=status)
