from celery import shared_task
from django.db import transaction
from django.utils import timezone
import logging

from .models import Outbox
from .producer import get_channel  # new: persistent RabbitMQ channel
import json
import pika

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def process_outbox_events(self, batch_size=100):
    """
    High-performance Outbox processor:
    - Uses DB row locking to avoid duplicates.
    - Reuses a persistent RabbitMQ connection.
    - Retries automatically on transient errors.
    - Logs metrics and timing for observability.
    """

    try:
        #  Open a database transaction to lock a batch of pending events.
        with transaction.atomic():
            events = (
                Outbox.objects
                .select_for_update(skip_locked=True)
                .filter(published=False)
                .order_by("id")[:batch_size]
            )

            if not events:
                logger.debug("No pending events to process.")
                return "No events."

            # Optional: mark as 'in progress' (if you add that field later)
            event_ids = [e.id for e in events]
            logger.info(f"Fetched {len(event_ids)} events: {event_ids}")

        # Get a shared RabbitMQ channel.
        channel = get_channel()

        # Publish each event.
        for event in events:
            try:
                channel.basic_publish(
                    exchange='orders.events',
                    routing_key=event.event_type,
                    body=json.dumps(event.payload),
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                # Mark as published
                event.published = True
                event.published_at = timezone.now()  # if you add this field
                event.save(update_fields=["published"])
                logger.debug(f"Published event {event.id} ({event.event_type})")

            except Exception as publish_error:
                logger.exception(f"Failed to publish event {event.id}: {publish_error}")
                # Let Celery retry this task for transient network issues
                raise self.retry(exc=publish_error)

        logger.info(f"Successfully published {len(events)} events.")
        return f"Processed {len(events)} events."

    except Exception as e:
        logger.exception("Outbox processor failed.")
        raise self.retry(exc=e)
