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
        status_html = f"""
        <div class="card success">
            <h2>🚀 Application Status: <span class="badge">ONLINE</span></h2>
            <p class="visits-text">Total Visits: <strong>{count}</strong></p>
        </div>
        """
    except redis.ConnectionError:
        status_html = """
        <div class="card error">
            <h2>⚠️ Application Status: <span class="badge error-badge">DATABASE OFFLINE</span></h2>
            <p>Sorry, could not connect to Redis database!</p>
        </div>
        """

    # تصميم HTML شيك وModern جداً
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>3-Tier DevOps Application</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: #f8fafc;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
                background: #1e293b;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
                max-width: 500px;
                width: 100%;
                border: 1px solid #334155;
            }}
            h1 {{
                color: #38bdf8;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            .card {{
                background: #0f172a;
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                border-left: 5px solid #38bdf8;
            }}
            .card.error {{
                border-left-color: #ef4444;
            }}
            .badge {{
                background: #0284c7;
                color: white;
                padding: 4px 10px;
                border-radius: 20px;
                font-size: 14px;
            }}
            .error-badge {{
                background: #dc2626;
            }}
            .visits-text {{
                font-size: 20px;
                margin-top: 15px;
            }}
            .footer {{
                margin-top: 25px;
                font-size: 12px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Python 3-Tier Architecture</h1>
            <p>Managed via Docker, GitLab CI/CD & AWS EC2</p>
            {status_html}
            <div class="footer">
                Powered by Nginx ➔ Flask ➔ Redis
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)