"""
python ingest_data.py \
    -u=root \
    -p=root \
    -H=localhost \
    -P=5432 \
    -d=ny_taxi \
    -t=yellow_taxi_data \
    -U=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
"""
import argparse

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    if params.extension == "csv":
        df = pd.read_csv(params.url)
    else:
        df = pd.read_parquet(params.url)
    conn_str = f"postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}"
    engine = create_engine(conn_str)
    sql_table = pd.io.sql.get_schema(df, name=params.table, con=engine)
    print(f"CREATING TABLE {params.table} with the following schema:")
    print(sql_table)
    df.head(0).to_sql(con=engine, name=params.table, if_exists="replace")
    print(f"Inserting {df.shape[0]} rows")
    df.to_sql(con=engine, name=params.table, if_exists="append", chunksize=100000)
    engine.dispose()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    parser.add_argument("-u", "--user", help="postgres username")
    parser.add_argument("-p", "--password", help="postgres password")
    parser.add_argument("-H", "--host", help="postgres host")
    parser.add_argument("-P", "--port", help="postgres port")
    parser.add_argument("-d", "--db", help="postgres table")
    parser.add_argument("-t", "--table", help="postgres table")
    parser.add_argument("-U", "--url", help="parquet url")
    parser.add_argument("-e", "--extension", default="parquet", help="file extension")
    args = parser.parse_args()
    main(args)