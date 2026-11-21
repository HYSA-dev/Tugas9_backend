from flask import Blueprint, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
from app.config import Config
from app.utils.response_helper import success_response, fail_response, error_response
import datetime

mongo_bp = Blueprint('mongo_logs', __name__, url_prefix='/api/v1/farm/logs')

# Inisialisasi koneksi MongoDB dari konfigurasi terpusat
client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[Config.MONGO_DB_NAME]
log_collection = db['farm_activity_logs']


# 1. READ ALL: Menampilkan maksimal 20 dokumen log aktivitas pertanian terbaru
@mongo_bp.route('', methods=['GET'])
def get_all_logs():
    try:
        logs = list(log_collection.find().sort("timestamp", -1).limit(20))
        for log in logs:
            log['_id'] = str(log['_id'])  # Serialisasi BSON ObjectId ke String

        return success_response(
            data={
                "total": len(logs),
                "items": logs
            },
            message="Berhasil mengambil daftar log aktivitas pertanian",
            code=200
        )
    except PyMongoError as e:
        return error_response(message=f"Gagal mengakses MongoDB: {str(e)}", code=500)


# 2. READ ONE: Mengambil detail satu dokumen log berdasarkan ObjectId
@mongo_bp.route('/<string:log_id>', methods=['GET'])
def get_log_by_id(log_id):
    try:
        log = log_collection.find_one({"_id": ObjectId(log_id)})
        if not log:
            return fail_response(errors={"message": "Dokumen log tidak ditemukan"}, code=404)

        log['_id'] = str(log['_id'])
        return success_response(
            data=log,
            message="Detail dokumen log ditemukan",
            code=200
        )
    except InvalidId:
        return fail_response(
            errors={"log_id": "Format ObjectId tidak valid (harus 24 karakter heksadesimal)"},
            code=400
        )
    except PyMongoError as e:
        return error_response(message=f"Gagal mengakses MongoDB: {str(e)}", code=500)


# 3. CREATE: Menyimpan log aktivitas / observasi lahan baru (Embedded Document)
@mongo_bp.route('', methods=['POST'])
def create_log():
    data = request.get_json() if request.is_json else None

    errors = {}
    if not data or not data.get("actor"):
        errors["actor"] = "Field 'actor' (petugas/pemilik) wajib diisi"
    if not data or not data.get("action"):
        errors["action"] = "Field 'action' wajib diisi"

    if errors:
        return fail_response(errors=errors, code=400)

    log_document = {
        "actor": data["actor"],
        "action": data["action"],
        "land_id": data.get("land_id"),       # Referensi opsional ke ID lahan di MySQL
        "crop_name": data.get("crop_name"),   # Referensi opsional ke nama tanaman
        "metadata": data.get("metadata", {}), # Embedded Document dinamis (pH tanah, pupuk, cuaca, dll.)
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    try:
        result = log_collection.insert_one(log_document)
        log_document['_id'] = str(result.inserted_id)

        return success_response(
            data=log_document,
            message="Log aktivitas pertanian berhasil disimpan ke MongoDB",
            code=201
        )
    except PyMongoError as e:
        return error_response(message=f"Gagal menyimpan dokumen: {str(e)}", code=500)


# 4. UPDATE: Memperbarui field tertentu secara atomik menggunakan operator $set
@mongo_bp.route('/<string:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json() if request.is_json else None
    if not data:
        return fail_response(errors={"body": "Request body JSON tidak boleh kosong"}, code=400)

    update_fields = {}
    if "actor" in data:
        update_fields["actor"] = data["actor"]
    if "action" in data:
        update_fields["action"] = data["action"]
    if "land_id" in data:
        update_fields["land_id"] = data["land_id"]
    if "crop_name" in data:
        update_fields["crop_name"] = data["crop_name"]
    if "metadata" in data:
        update_fields["metadata"] = data["metadata"]

    if not update_fields:
        return fail_response(errors={"fields": "Tidak ada field valid untuk diperbarui"}, code=400)

    update_fields["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        res = log_collection.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": update_fields}
        )
        if res.matched_count == 0:
            return fail_response(errors={"message": "Dokumen log tidak ditemukan"}, code=404)

        return success_response(
            message="Dokumen log pertanian berhasil diperbarui",
            code=200
        )
    except InvalidId:
        return fail_response(
            errors={"log_id": "Format ObjectId tidak valid (harus 24 karakter heksadesimal)"},
            code=400
        )
    except PyMongoError as e:
        return error_response(message=f"Gagal memperbarui dokumen: {str(e)}", code=500)


# 5. DELETE: Menghapus dokumen log berdasarkan ObjectId
@mongo_bp.route('/<string:log_id>', methods=['DELETE'])
def delete_log(log_id):
    try:
        res = log_collection.delete_one({"_id": ObjectId(log_id)})
        if res.deleted_count == 0:
            return fail_response(errors={"message": "Dokumen log tidak ditemukan"}, code=404)

        return success_response(
            message="Dokumen log pertanian berhasil dihapus",
            code=200
        )
    except InvalidId:
        return fail_response(
            errors={"log_id": "Format ObjectId tidak valid (harus 24 karakter heksadesimal)"},
            code=400
        )
    except PyMongoError as e:
        return error_response(message=f"Gagal menghapus dokumen: {str(e)}", code=500)