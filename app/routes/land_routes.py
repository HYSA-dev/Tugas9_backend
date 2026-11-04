from flask import Blueprint, request
from app.services.land_service import LandService
from app.utils.response_helper import success_response, fail_response, error_response

land_bp = Blueprint("lands", __name__, url_prefix="/api/v1/farm")

@land_bp.route("/lands", methods=["GET"])
def get_lands():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        search = request.args.get('search', '', type=str)
        
        result = LandService.get_paginated_lands(page, per_page, search)
        
        return success_response(
            data={
                "items": result["items"],
                "pagination": result["pagination"]
            }, 
            message="Berhasil mengambil data lahan", 
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)

@land_bp.route("/lands", methods=["POST"])
def create_land():
    try:
        data = request.get_json() if request.is_json else None
        result, status_code = LandService.create_land(data)
        
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(data={"id": result.id, "name": result.name}, message="Data lahan berhasil ditambahkan", code=201)
    except Exception as e:
        return error_response(message=str(e), code=500)

@land_bp.route("/lands/<int:id>", methods=["DELETE"])
def delete_land(id):
    try:
        land = LandService.delete_land(id)
        if not land:
            return fail_response(errors={"message": "Data lahan tidak ditemukan"}, code=404)
        return success_response(message="Data lahan berhasil dihapus", code=200)
    except Exception as e:
        return error_response(message=str(e), code=500)

@land_bp.route("/lands/<int:land_id>", methods=["PUT"])
def update_land(land_id):
    try:
        data = request.get_json() if request.is_json else None
        result, status_code = LandService.update_land(land_id, data)
        
        if status_code == 404:
            return fail_response(message="Data lahan tidak ditemukan", code=404)
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(
            data={"id": result.id, "name": result.name, "area": result.area, "owner_id": result.owner_id},
            message="Data lahan berhasil diperbarui",
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)