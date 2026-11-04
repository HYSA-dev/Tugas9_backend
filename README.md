# UTS Backend - Sistem Manajemen Data Lahan dan Tanaman
**Mata Kuliah:** Dasar Pemrograman Backend  
**Dosen Pengampu:** Sony Panca Budiarto, M.Kom  
**Nama Mahasiswa:** Galing Surya  
**NIM:** 1125102206 (Kelas S1-TI / SP3.1)  

---

## 📌 Deskripsi Proyek
Proyek Backend ini dikembangkan untuk memenuhi Ujian Tengah Semester (UTS) Ganjil Tahun Akademik 2026/2027[cite: 4]. Sistem ini dirancang menggunakan arsitektur berlapis (*Layered Architecture*) dengan pola modular[cite: 4], menerapkan basis data relasional MySQL melalui SQLAlchemy ORM[cite: 4], serta menyediakan *endpoint* RESTful API untuk pengelolaan data lahan pertanian[cite: 4].

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Framework:** Flask
* **ORM:** Flask-SQLAlchemy (PyMySQL)
* **Database:** MySQL / MySQL Workbench
* **API Testing:** Postman / Thunder Client

## 📁 Struktur Folder Proyek
Proyek ini menerapkan hierarki folder modular sesuai standar praktikum:
```text
uts_backend_1125102206/
├── app/
│   ├── models/
│   │   └── farm_model.py   # Skema 3 Tabel Berelasi (Owner -> Land -> Crop)
│   ├── routes/
│   │   └── farm_routes.py  # Endpoint CRUD & Transaksi Atomik (Try-Except-Rollback)
│   ├── __init__.py         # Application Factory Pattern
│   └── config.py           # Konfigurasi Database MySQL
├── venv/                   # Virtual Environment
├── run.py                  # Entry Point Aplikasi
└── README.md

Skema Database Relasional (One-to-Many / 1:N)
Sistem ini terdiri dari 3 tabel utama yang saling berelasi:

owners (Tabel Pemilik Lahan) — Berelasi One-to-Many ke tabel lands.

lands (Tabel Lahan) — Berelasi One-to-Many ke tabel crops.

crops (Tabel Komoditas Tanaman).

🚀 Cara Menjalankan Proyek
Clone atau buka direktori proyek di dalam terminal/VS Code.

Aktifkan virtual environment: