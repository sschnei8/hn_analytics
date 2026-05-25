import duckdb
from pathlib import Path

ROOT = Path(__file__).parent.parent
conn = duckdb.connect()

result = conn.execute(f"""
    SELECT
        CASE
            WHEN score = 1                 THEN '1'
            WHEN score BETWEEN 2   AND 3   THEN '2-3'
            WHEN score BETWEEN 4   AND 10  THEN '4-10'
            WHEN score BETWEEN 11  AND 25  THEN '11-25'
            WHEN score BETWEEN 26  AND 50  THEN '26-50'
            WHEN score BETWEEN 51  AND 100 THEN '51-100'
            WHEN score BETWEEN 101 AND 250 THEN '101-250'
            WHEN score BETWEEN 251 AND 500 THEN '251-500'
            WHEN score > 500               THEN '500+'
        END AS score_bucket,
        COUNT(*) AS story_count
    FROM '{ROOT}/data/hnbq.csv'
    WHERE score IS NOT NULL
    GROUP BY score_bucket
    HAVING score_bucket IS NOT NULL
    ORDER BY MIN(score)
""")

print(f"{'score_bucket':>15}  {'story_count':>12}")
for row in result.fetchall():
    print(f"{row[0]:>15}  {row[1]:>12,}")

conn.execute(f"""
    COPY (
        SELECT
            CASE
                WHEN score = 1                 THEN '1'
                WHEN score BETWEEN 2   AND 3   THEN '2-3'
                WHEN score BETWEEN 4   AND 10  THEN '4-10'
                WHEN score BETWEEN 11  AND 25  THEN '11-25'
                WHEN score BETWEEN 26  AND 50  THEN '26-50'
                WHEN score BETWEEN 51  AND 100 THEN '51-100'
                WHEN score BETWEEN 101 AND 250 THEN '101-250'
                WHEN score BETWEEN 251 AND 500 THEN '251-500'
                WHEN score > 500               THEN '500+'
            END AS score_bucket,
            COUNT(*) AS story_count
        FROM '{ROOT}/data/hnbq.csv'
        WHERE score IS NOT NULL
        GROUP BY score_bucket
        HAVING score_bucket IS NOT NULL
        ORDER BY MIN(score)
    ) TO '{ROOT}/data/score_distribution.csv' (HEADER)
""")
