import os
from flask import Flask
import redis

app = Flask(__name__)

   
redis_host = os.getenv('REDIS_HOST', 'redis_db')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def hello():
    try:
        count = r.incr('visits')
    except redis.ConnectionError:
        count = "Sorry, Database is offline!"
    return f"Hello from Python 3-Tier Application! 🚀 Total Visits: {count}\n"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)