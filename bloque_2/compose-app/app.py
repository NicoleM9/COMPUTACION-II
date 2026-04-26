
import redis
import os
import time

redis_host = os.getenv('REDIS_HOST', 'localhost')

print(f"Conectando a Redis en {redis_host}...")

while True:
    try:
        r = redis.Redis(host=redis_host, port=6379)
        r.ping()
        print("Conectado a Redis!")
        break
    except redis.exceptions.ConnectionError:
        print("Esperando a Redis...")
        time.sleep(1)

while True:
    visitas = r.incr('visitas')
    print(f"Visitas: {visitas}")
    time.sleep(2)