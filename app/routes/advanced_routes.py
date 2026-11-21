from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import PyMongoError
from app import db
from app.models.owner import Owner
from app.models.land import Land
from app.routes.mongo_log_routes import log_collection
from app.utils.response_helper import success_response, fail_response, error_response
import datetime

advanced_bp = Blueprint('advanced_api', __name__, url_prefix='/api/v1/farm/advanced')


def record_audit_log(action, status, metadata):
    """Helper untuk mencatat audit trail transaksi MySQL ke MongoDB (Polyglot Persistence)"""
    try:
        log_collection.insert_one({
            "actor": "SYSTEM_TRANSACTION",
            "action": action,
            "metadata": {
                "transaction_status": status,
                **metadata
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })
    except PyMongoError:
        # Jangan sampai kegagalan pencatatan log menggagalkan respons utama
        pass


@advanced_bp.route('/owner-with-land', methods=['POST'])
def create_owner_with_land_transaction():
    data = request.get_json() if request.is_json else None

    # Validasi input dasar
    errors = {}
    if not data or not data.get("owner_name"):
        errors["owner_name"] = "Nama pemilik wajib diisi"
    if not data or not data.get("land_name"):
        errors["land_name"] = "Nama lahan wajib diisi"
    if not data or data.get("area") is None:
        errors["area"] = "Luas lahan (area) wajib diisi"

    if errors:
        return fail_response(errors=errors, code=400)

    try:
        # 1. Buat objek Owner baru
        new_owner = Owner(
            name=data.get("owner_name"),
            contact=data.get("contact", "-")
        )
        db.session.add(new_owner)

        # 2. Flush untuk mendapatkan new_owner.id secara otomatis sebelum commit akhir
        db.session.flush()

        # 3. Buat objek Land dengan menyertakan owner_id yang baru saja di-flush
        new_land = Land(
            name=data.get("land_name"),
            area=float(data["area"]),
            owner_id=new_owner.id
        )
        db.session.add(new_land)

        # 4. Commit permanen jika kedua proses sukses
        db.session.commit()

        # 5. Catat Audit Trail COMMIT ke MongoDB
        record_audit_log(
            action="TRANSACTION_OWNER_WITH_LAND",
            status="COMMITTED",
            metadata={
                "owner_id": new_owner.id,
                "owner_name": new_owner.name,
                "land_id": new_land.id,
                "land_name": new_land.name,
                "area_hectare": new_land.area
            }
        )

        return success_response(
            data={
                "owner": {"id": new_owner.id, "name": new_owner.name},
                "land": {"id": new_land.id, "name": new_land.name, "area": new_land.area}
            },
            message="Transaksi berhasil: Pemilik dan Lahan baru berhasil disimpan",
            code=201
        )

    except (SQLAlchemyError, ValueError, TypeError) as e:
        # Batalkan seluruh perubahan jika terjadi galat / error tipe data
        db.session.rollback()

        # Catat Audit Trail ROLLBACK ke MongoDB
        record_audit_log(
            action="TRANSACTION_OWNER_WITH_LAND",
            status="ROLLBACK",
            metadata={
                "reason": str(e),
                "attempted_payload": data
            }
        )

        return error_response(message=f"Transaksi dibatalkan (Rollback): {str(e)}", code=500)