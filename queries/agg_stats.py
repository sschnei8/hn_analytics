import duckdb
from pathlib import Path

ROOT = Path(__file__).parent.parent
conn = duckdb.connect()

result = conn.execute(f"""
    SELECT
        AVG(score)                                          AS mean_score,
        mode(score)                                         AS mode_score,
        MIN(score)                                          AS min_score,
        MAX(score)                                          AS max_score,
        COUNT(*)                                            AS total_stories,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) AS median_score
    FROM '{ROOT}/data/hnbq.csv'
    WHERE score IS NOT NULL
""")

cols = [d[0] for d in result.description]
row = result.fetchone()
for col, val in zip(cols, row):
    print(f"{col}: {val}")

conn.execute(f"""
    COPY (
        SELECT
            AVG(score)                                          AS mean_score,
            mode(score)                                         AS mode_score,
            MIN(score)                                          AS min_score,
            MAX(score)                                          AS max_score,
            COUNT(*)                                            AS total_stories,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) AS median_score
        FROM '{ROOT}/data/hnbq.csv'
        WHERE score IS NOT NULL
    ) TO '{ROOT}/data/agg_stats.csv' (HEADER)
""")
