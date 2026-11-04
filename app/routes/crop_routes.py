from flask import Blueprint, request
from app.services.crop_service import CropService
from app.utils.response_helper import success_response, fail_response, error_response

crop_bp = Blueprint("crops", __name__, url_prefix="/api/v1/farm")

@crop_bp.route("/crops", methods=["GET"])
def get_crops():
    try:
        # Menangkap query parameter paginasi & search dari URL
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        search = request.args.get('search', '', type=str)
        
        # Memanggil service yang sudah kita update
        result = CropService.get_paginated_crops(page, per_page, search)
        
        # Mengembalikan respons sukses dengan menyertakan data dan metadata pagination
        return success_response(
            data={
                "items": result["items"],
                "pagination": result["pagination"]
            }, 
            message="Berhasil mengambil data tanaman", 
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)

@crop_bp.route("/crops", methods=["POST"])
def create_crop():
    try:
        data = request.get_json() if request.is_json else None
        result, status_code = CropService.create_crop(data)
        
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(data={"id": result.id, "name": result.name}, message="Data tanaman berhasil ditambahkan", code=201)
    except Exception as e:
        return error_response(message=str(e), code=500)

@crop_bp.route("/crops/<int:id>", methods=["DELETE"])
def delete_crop(id):
    try:
        crop = CropService.delete_crop(id)
        if not crop:
            return fail_response(errors={"message": "Data tanaman tidak ditemukan"}, code=404)
        return success_response(message="Data tanaman berhasil dihapus", code=200)
    except Exception as e:
        return error_response(message=str(e), code=500)

@crop_bp.route("/crops/<int:crop_id>", methods=["PUT"])
def update_crop(crop_id):
    try:
        data = request.get_json() if request.is_json else None
        result, status_code = CropService.update_crop(crop_id, data)
        
        if status_code == 404:
            return fail_response(message="Data tanaman tidak ditemukan", code=404)
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(
            data={"id": result.id, "name": result.name, "season": result.season, "land_id": result.land_id},
            message="Data tanaman berhasil diperbarui",
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)