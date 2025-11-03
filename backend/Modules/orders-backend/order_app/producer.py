import pika, json
from contextlib import contextmanager

_connection = None
_channel = None

def get_channel():
    global _connection, _channel
    if _connection is None or _connection.is_closed:
        params = pika.ConnectionParameters(
            host='rabbitmq',  # or from settings
            heartbeat=600,    # keepalive
            blocked_connection_timeout=300,
        )
        _connection = pika.BlockingConnection(params)
        _channel = _connection.channel()
    return _channel

def publish_event(event_type, payload):
    channel = get_channel()
    channel.basic_publish(
        exchange='',
        routing_key=event_type,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )
