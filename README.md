# 🌾 Farm Management System - Backend API (UTS)

Sistem Manajemen Data Lahan dan Tanaman Pertanian (Farm Management System) berbasis RESTful API. Proyek backend ini dibangun menggunakan **Flask** dengan arsitektur berlapis (*Layered Architecture*: Model - Repository - Service - Route), mendayagunakan **SQLAlchemy (MySQL)** sebagai ORM, serta menerapkan transaksi atomik multi-tabel (ACID Compliance).

---

## 🛠️ Teknologi & Stack
* **Language**: Python 3.x
* **Framework**: Flask (Application Factory Pattern & Blueprints)
* **Database & ORM**: MySQL via SQLAlchemy (PyMySQL driver)
* **Architecture**: Layered Architecture (Model $\rightarrow$ Repository $\rightarrow$ Service $\rightarrow$ Route)
* **API Standard**: JSON Response Envelope (`success`, `fail`, `error`)

---

## 📁 Struktur Direktori Proyek

```text
uts_backend_1125102206/
├── app/
│   ├── models/
│   │   └── farm_model.py         # ORM Model 3 Tabel (Owner, Land, Crop)
│   ├── repositories/
│   │   ├── owner_repository.py   # Data Access Layer - Owner
│   │   ├── land_repository.py    # Data Access Layer - Land
│   │   └── crop_repository.py    # Data Access Layer - Crop
│   ├── services/
│   │   ├── owner_service.py      # Business Logic & Validation - Owner
│   │   ├── land_service.py       # Business Logic & Validation - Land
│   │   └── crop_service.py       # Business Logic & Validation - Crop
│   ├── routes/
│   │   ├── owner_routes.py       # Controller Endpoint CRUD Owner
│   │   ├── land_routes.py        # Controller Endpoint CRUD Land
│   │   ├── crop_routes.py        # Controller Endpoint CRUD Crop
│   │   └── advanced_routes.py    # Multi-Table Transaction (ACID)
│   ├── utils/
│   │   └── response_helper.py    # JSON Response Envelope Formatter
│   └── __init__.py               # Application Factory (`create_app`)
├── config.py                     # Database Configuration (MySQL Connection String)
├── run.py                        # Application Entry Point
├── db_uts_backend.sql            # File Ekspor Database MySQL
└── README.md                     # Dokumentasi Proyek
```

---

## 🚀 Fitur Utamanya

1. **Full CRUD Operations (3 Entitas Relasional)**:
   * **Owners** (Pemilik Lahan)
   * **Lands** (Lahan Pertanian, Relasi 1:N ke Owner)
   * **Crops** (Tanaman Komoditas, Relasi 1:N ke Land)
2. **Server-Side Pagination & Search**:
   * Paginasi berbasis `page` & `per_page`.
   * Pencarian `search` menggunakan pencocokan substring `.ilike()` (*case-insensitive*).
3. **Advanced Multi-Table Transaction (ACID Compliance)**:
   * Penambahan data Owner dan Land secara simultan.
   * Menggunakan `db.session.flush()` untuk mendapatkan *relational ID* secara instan.
   * Didukung mekanisme pembatalan otomatis (`db.session.rollback()`) jika terjadi kesalahan internal untuk mencegah korupsi data.
4. **Validasi Error Berlapis**:
   * Pengembalian respons standar berformat JSON Envelope dengan HTTP Status Code yang tepat (`200`, `201`, `400`, `404`, `500`).

---

## 📡 Daftar Endpoint API

### 1. Owners (`/api/v1/farm/owners`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/farm/owners` | Ambil daftar pemilik (Pagination & Search `?search=...`) |
| `POST` | `/api/v1/farm/owners` | Tambah data pemilik baru |
| `PUT` | `/api/v1/farm/owners/<id>` | Perbarui data pemilik berdasarkan ID |
| `DELETE` | `/api/v1/farm/owners/<id>` | Hapus data pemilik berdasarkan ID |

### 2. Lands (`/api/v1/farm/lands`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/farm/lands` | Ambil seluruh daftar lahan (Pagination & Search) |
| `POST` | `/api/v1/farm/lands` | Tambah data lahan baru (`owner_id` required) |
| `PUT` | `/api/v1/farm/lands/<id>` | Perbarui data lahan berdasarkan ID |
| `DELETE` | `/api/v1/farm/lands/<id>` | Hapus data lahan berdasarkan ID |

### 3. Crops (`/api/v1/farm/crops`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/farm/crops` | Ambil seluruh data tanaman komoditas |
| `POST` | `/api/v1/farm/crops` | Tambah data tanaman baru (`land_id` required) |
| `PUT` | `/api/v1/farm/crops/<id>` | Perbarui data tanaman berdasarkan ID |
| `DELETE` | `/api/v1/farm/crops/<id>` | Hapus data tanaman berdasarkan ID |

### 4. Advanced Transaction (`/api/v1/farm/advanced`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/farm/advanced/owner-with-land` | Buat Owner & Land sekaligus dalam 1 transaksi atomik |

---
