from flask import Blueprint, request
from app.services.owner_service import OwnerService
from app.utils.response_helper import success_response, fail_response, error_response

owner_bp = Blueprint("owners", __name__, url_prefix="/api/v1/farm")

@owner_bp.route("/owners", methods=["GET"])
def get_owners():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        search = request.args.get('search', '', type=str)
        
        result = OwnerService.get_paginated_owners(page, per_page, search)
        
        return success_response(
            data={
                "items": result["items"],
                "pagination": result["pagination"]
            }, 
            message="Berhasil mengambil data pemilik", 
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)

@owner_bp.route("/owners", methods=["POST"])
def create_owner():
    try:
        data = request.get_json() if request.is_json else None
        
        # Panggil service yang mengembalikan tuple (result, status_code)
        result, status_code = OwnerService.create_owner(data)
        
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(data={"id": result.id, "name": result.name}, message="Data pemilik berhasil ditambahkan", code=201)
    except Exception as e:
        return error_response(message=str(e), code=500)

@owner_bp.route("/owners/<int:id>", methods=["DELETE"])
def delete_owner(id):
    try:
        owner = OwnerService.delete_owner(id)
        if not owner:
            return fail_response(errors={"message": "Data pemilik tidak ditemukan"}, code=404)
        return success_response(message="Data pemilik berhasil dihapus", code=200)
    except Exception as e:
        return error_response(message=str(e), code=500)

@owner_bp.route("/owners/<int:owner_id>", methods=["PUT"])
def update_owner(owner_id):
    try:
        data = request.get_json() if request.is_json else None
        result, status_code = OwnerService.update_owner(owner_id, data)
        
        if status_code == 404:
            return fail_response(message="Data pemilik tidak ditemukan", code=404)
            
        if status_code == 400:
            return fail_response(errors=result["errors"], code=400)
            
        return success_response(
            data={"id": result.id, "name": result.name, "contact": result.contact},
            message="Data pemilik berhasil diperbarui",
            code=200
        )
    except Exception as e:
        return error_response(message=str(e), code=500)