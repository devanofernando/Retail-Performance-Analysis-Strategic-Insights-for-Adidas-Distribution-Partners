import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import psycopg2 as db
import re
import csv

def extract():
    '''
    Mengambil data dari PostgreSQL tanpa modifikasi.
    '''
    conn = db.connect(
        host="postgres",
        port=5432,
        database="milestone_3",
        user="airflow",
        password="airflow"
    )
    df = pd.read_sql('SELECT * FROM "table_m3"', con=conn)
    df.to_csv("P2M3_devano_fernando_data_raw_from_db.csv", index=False)
    conn.close()

def transform():
    # Membaca file CSV tanpa header
    df = pd.read_csv("P2M3_devano_fernando_data_raw_from_db.csv", header=None)

    # Define nama kolom sesuai yang diambil dari dataset original
    columns = [
        "Retailer", "Retailer ID", "Invoice Date", "Region", "State", "City",
        "Product", "Price per Unit", "Units Sold", "Total Sales",
        "Operating Profit", "Operating Margin", "Sales Method"
    ]
    df.columns = columns

    # Normalisasi nama kolom: lowercase dan underscore
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)  

    # Handle missing values
    numeric_cols = ['price_per_unit', 'units_sold', 'total_sales', 'operating_profit', 'operating_margin']
    text_cols = ['retailer', 'retailer_id', 'region', 'state', 'city', 'product', 'sales_method']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('[$%, ]', '', regex=True), errors='coerce').fillna(0)
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')

    # Konversi invoice_date (hanya untuk nilai yang valid)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%m/%d/%Y', errors='coerce')
    df = df.dropna(subset=['invoice_date'])

    # Simpan ke file clean (ada header)
    output_path = "/opt/airflow/dags/P2M3_devano_fernando_data_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Data cleaning: {len(df)} baris valid tersimpan.")

def load():
    """
    Mengoper data clean ke Elasticsearch.
    """
    # Baca file data clean (otomatis baca header)
    df = pd.read_csv("/opt/airflow/dags/P2M3_devano_fernando_data_clean.csv")

    # Koneksi ke Elasticsearch
    es = Elasticsearch(hosts=["http://elasticsearch:9200"])
    index_name = "milestone_3_clean"

    # Siapkan data untuk bulk insert
    actions = [
        {"_index": index_name, "_source": row.to_dict()}
        for _, row in df.iterrows()
    ]

    # Kirim ke Elasticsearch
    try:
        helpers.bulk(es, actions)
        print(f"Berhasil mengirim {len(actions)} dokumen ke Elasticsearch index '{index_name}'")
    except Exception as e:
        print(f"Gagal mengirim data ke Elasticsearch: {e}")
        raise

# DAG Configuration
default_args = {
    'owner': 'Devano',
    'start_date': dt.datetime(2024, 11, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'P2M3_devano_fernando_DAG',
    default_args=default_args,
    schedule_interval='10,20,30 9 * * 6',
    catchup=False
) as dag:

    fetch_task = PythonOperator(task_id='extract', python_callable=extract)
    clean_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    fetch_task >> clean_task >> load_task