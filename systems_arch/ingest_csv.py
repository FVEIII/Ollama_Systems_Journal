import csv, os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()
PG_DSN = os.getenv("PG_DSN", "dbname=osj user=osj password=osj host=localhost port=5432")
CSV_PATH = os.getenv("CSV_PATH", "data/coffee_prices_template.csv")

def main():
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute("""
                INSERT INTO analytics.coffee_prices (date, origin, price_usd_per_kg, source)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (date, origin) DO UPDATE
                SET price_usd_per_kg = EXCLUDED.price_usd_per_kg,
                    source = EXCLUDED.source;
            """, (row["date"], row["origin"], row["price_usd_per_kg"], row.get("source")))
    cur.execute("DELETE FROM analytics.coffee_prices_30d;")
    cur.execute("""
        INSERT INTO analytics.coffee_prices_30d (as_of_date, origin, avg_price_30d, last_price)
        SELECT
          MAX(date) as as_of_date,
          origin,
          AVG(price_usd_per_kg) FILTER (WHERE date >= (MAX(date) - INTERVAL '30 days'))::numeric(10,4) as avg_30d,
          (ARRAY_AGG(price_usd_per_kg ORDER BY date DESC))[1] as last_price
        FROM analytics.coffee_prices
        GROUP BY origin;
    """)
    conn.commit()
    cur.close(); conn.close()
    print(f"[{datetime.now().isoformat(timespec='seconds')}] Ingest + 30d rollup complete.")

if __name__ == "__main__":
    main()
