# orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, Outbox
from .serializers import OrderSerializer
from .tasks import process_outbox_events
from .utils import is_duplicate_request, save_idempotency_response, get_cached_response

class CreateOrderView(APIView):
    def post(self, request):
        idempotency_key = request.headers.get('Idempotency-Key')
        if not idempotency_key:
            return Response({'error': 'Missing Idempotency-Key header'}, status=400)

        # Check duplicate request
        if is_duplicate_request(idempotency_key):
            cached = get_cached_response(idempotency_key)
            return Response(cached, status=200)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                order = serializer.save(status="CREATED")
                Outbox.objects.create(
                    event_type="order.created",
                    payload={"order_id": str(order.id), "user_id": str(order.user_id), "amount": str(order.total_amount)}
                )
            response_data = OrderSerializer(order).data
            save_idempotency_response(idempotency_key, response_data)
            # trigger async event dispatch
            process_outbox_events.delay()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
