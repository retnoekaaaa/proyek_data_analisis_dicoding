# Proyek Analisis Data: Kualitas Udara Beijing (PRSA)

Analisis PM2.5 dari 12 stasiun pemantau di Beijing (Maret 2013 – Februari 2017) beserta dashboard interaktif Streamlit.

## Pertanyaan Bisnis
1. Bagaimana tren dan pola musiman PM2.5, dan stasiun mana yang paling tercemar?
2. Faktor cuaca apa yang paling berkaitan dengan PM2.5?

## Setup Environment

### Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Shell / Terminal
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan Notebook
Letakkan 12 file `PRSA_Data_*.csv` di folder `data/`, lalu jalankan `notebook.ipynb` (Run All). Notebook menghasilkan `dashboard/main_data.csv`.

## Menjalankan Dashboard
```
streamlit run dashboard/dashboard.py
```
Dashboard terbuka di http://localhost:8501
