import os
from adapters.db.postgres_repo import PostgresOrderRepository
from adapters.file.csv_repo import CsvOrderRepository
from adapters.http.controllers import create_app

def build_app():
    adapter = os.getenv("REPO_ADAPTER", "db")
    if adapter == "db":
        conn_str = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')} host={os.getenv('DB_HOST')}"
        repo = PostgresOrderRepository(conn_str)
    else:
        repo = CsvOrderRepository(os.getenv("CSV_PATH", "/data/orders.csv"))
    return create_app(repo)
