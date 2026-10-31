# Perintah Menjalankan Proyek

Jalankan semua perintah dari dalam folder `submission`.

## 1. Siapkan environment

### Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Shell / Terminal biasa
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Siapkan dataset

Taruh 12 file `PRSA_Data_*.csv` di folder `data/`, lalu cek:

```bash
ls data/                        # Windows: dir data
```

## 3. Jalankan notebook (menghasilkan dashboard/main_data.csv)

### Cara interaktif
```bash
jupyter notebook notebook.ipynb
```
Lalu pilih Run All dan simpan notebook beserta outputnya.

### Cara otomatis (output langsung tersimpan)
```bash
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

Pastikan file ini terbentuk:
```bash
ls dashboard/main_data.csv      # Windows: dir dashboard\main_data.csv
```

## 4. Jalankan dashboard

```bash
streamlit run dashboard/dashboard.py
```
Dashboard terbuka di http://localhost:8501

## 5. Cek struktur akhir sebelum submit

```
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| └───PRSA_Data_*.csv  (12 file)
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt (opsional)
```

## 6. Uji ulang di environment baru (opsional, disarankan)

```bash
python -m venv test-env
source test-env/bin/activate    # Windows: test-env\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```
