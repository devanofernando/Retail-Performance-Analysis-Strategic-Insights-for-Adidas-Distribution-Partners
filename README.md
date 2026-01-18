# Retail Performance Analysis : Strategic Insights for Adidas Distribution Partners

ANALISIS PERFORMA PENJUALAN PRODUK RETAIL ADIDAS SEBAGAI INDIKATOR KELAYAKAN STRATEGI BISNIS

## Repository Outline
Bagian ini menjelaskan secara singkat konten/isi dari file yang dipush ke repository

1. P2M3_devano_fernando_conceptual.txt
    - Basic knowledge NoSQL
2. P2M3_devano_fernando_DAG_graph.jpg 
    - Berisi alur dari ETL yang nanti akan dijalankan oleh airflow secara otomatis 
3. P2M3_devano_fernando_ddl.txt
    - Berisi querry untuk create table dan insert value ke dalam postgreSQL
4. P2M3_devano_fernando_GX.ipynb
    - Berisi hasil dari great expectation yang didalamnya ada validasi data setelah proses ETL
5. P2M3_devano_fernando_DAG.py
    - Berisi syntax DAG untuk melakukan extraksi data dari data source (postgresSQL) dilanjut dengan transformasi data dan load data ke warehouse data base (elasticsearch)
6. P2M3_devano_fernando_data_raw.csv
    - Berisi data mentah yang sudah di extract dari postgreSQL
7. P2M3_devano_fernando_data_clean.csv
    - Merupakan data yang kondisinya sudah clean (hasil dari proses transformasi) yang sudah siap dimasukkan ke server warehouse database
8. Images
    - Berisi kumpulan dari visualisasi yang ingin dicapai (seperti channel penjualan apa yang paling mendominasi, toko retail mana yang paling mendominasi, produk mana yang paling laku, dll)


## Problem Background

Sebagai Data Analyst di perusahaan ritel fashion global yang menjual produk Adidas, saya diminta untuk menganalisis performa penjualan yang terjadi dari tahun 2020 - 2021. Tujuannya yaitu untuk memberikan rekomendasi data-driven kepada manajemen mengenai strategi distribusi, alokasi stok, dan fokus pemasaran sehingga perusahaan dapat meningkatkan profitabilitas dan mengoptimalkan sumber daya di tengah persaingan yang ketat.

## Project Output
 
    - Mengidentifikasi produk dan retailer paling profitabel
    - Memahami efektivitas setiap channel penjualan (Online vs In-store vs Outlet)
    - Mengetahui pola musiman dalam penjualan
    - Memberikan rekomendasi konkret kepada tim Marketing & Sales agar alokasi anggaran dan stok lebih tepat sasaran


## Data

Dataset berisi **data penjualan ritel produk Adidas** yang disimulasikan secara internal, dengan karakteristik sebagai berikut:

- Jumlah baris: 9.648 transaksi  
- Jumlah kolom: 14 kolom utama (kombinasi kategorikal & numerikal)  
  - Kategorikal: `retailer`, `region`, `state`, `city`, `product`, `sales_method,`  
  - Numerikal: `retailer_id`, `price_per_unit`, `units_sold`, `total_sales`, `operating_profit`, `operating_margin`  
- **Rentang waktu**: Januari 2020 – Desember 2021  
- **Wilayah**: Northeast, South, Midwest, West (Amerika Serikat)  
- **Retailer**: West Gear, Foot Locker, Sports Direct, Amazon, Kohl’s  

## Method

Alur pengerjaan dari proyek ini mengikuti pipeline ETL dan validasi berikut:

1. Extract: Ambil data mentah dari PostgreSQL (table_m3) tanpa modifikasi
2. Transform:
- Normalisasi nama kolom → lowercase + underscore
- Bersihkan simbol ($, ,, %) dari nilai numerik
- Konversi invoice_date ke tipe datetime
- Handle missing values & duplikat (walaupun tidak ada)
3. Load: Kirim data clean ke Elasticsearch untuk visualisasi
4. Validasi: Gunakan Great Expectations untuk memastikan kualitas data (7 expectation, semua success: true)
5. Visualisasi: Buat 6 visualisasi berbeda + 2 Markdown di Kibana sesuai objective


## Stacks

- Bahasa Pemrogaman:
    - python
    - SQL

- Library:
    - pandas
    - psycopg2
    - datetime
    - airflow (DAG)
    - airflow.operators.python (PythonOperator)
    - elastchsearch (Elasticsearch, helpers)
    - csv
    - re

- Container:
    - docker

- Database: 
    - postgresSQL
    - elasticsearch

- Orchestractor: 
    - airflow

- Visualization:
    - kibana


## Reference

URL dataset = https://www.kaggle.com/datasets/heemalichaudhari/adidas-sales-dataset 

