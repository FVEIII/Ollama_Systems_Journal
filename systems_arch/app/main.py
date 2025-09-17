import os, json
import psycopg2
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
PG_DSN = os.getenv("PG_DSN", "dbname=osj user=osj password=osj host=localhost port=5432")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

RDS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
app = FastAPI(title="OSJ Analytics API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analytics/coffee/30d")
def coffee_30d():
    key = "analytics:v1:coffee:30d"
    cached = RDS.get(key)
    if cached:
        return json.loads(cached)

    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("""
        SELECT origin, avg_price_30d, last_price
        FROM analytics.coffee_prices_30d
        ORDER BY origin;
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()

    payload = [
        {"origin": r[0], "avg_price_30d": float(r[1]), "last_price": float(r[2])}
        for r in rows
    ]
    RDS.setex(key, 120, json.dumps(payload))
    return payload

@app.get("/analytics/coffee/forecast")
def coffee_forecast():
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("SELECT origin, last_price FROM analytics.coffee_prices_30d;")
    rows = cur.fetchall()
    cur.close(); conn.close()

    data = []
    for origin, last_price in rows:
        data.append({
            "origin": origin,
            "forecast": [{"day_offset": d, "price": float(last_price)} for d in range(1, 8)]
        })
    return data
