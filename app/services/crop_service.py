from app.repositories.crop_repository import CropRepository
from app.models.crop import Crop

class CropService:
    @staticmethod
    def get_paginated_crops(page, per_page, search):
        pagination = CropRepository.get_paginated(page, per_page, search)
        
        items = [{"id": c.id, "name": c.name, "season": c.season, "land_id": c.land_id} for c in pagination.items]
        
        return {
            "items": items,
            "pagination": {
                "current_page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total
            }
        }

    @staticmethod
    def create_crop(data):
        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Field nama tanaman wajib diisi"
        if not data or not data.get("season"):
            errors["season"] = "Field musim (season) wajib diisi"
        if not data or not data.get("land_id"):
            errors["land_id"] = "Field land_id wajib diisi"
            
        if errors:
            return {"errors": errors}, 400

        new_crop = Crop(name=data.get("name"), season=data.get("season"), land_id=data.get("land_id"))
        CropRepository.save(new_crop)
        return new_crop, 201

    @staticmethod
    def delete_crop(crop_id):
        crop = CropRepository.get_by_id(crop_id)
        if not crop:
            return None
        CropRepository.delete(crop)
        return crop

    @staticmethod
    def update_crop(crop_id, data):
        crop = CropRepository.get_by_id(crop_id)
        if not crop:
            return None, 404

        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Nama tanaman wajib diisi"
        if not data or not data.get("season"):
            errors["season"] = "Musim tanam wajib diisi"
            
        if errors:
            return {"errors": errors}, 400

        crop.name = data.get("name")
        crop.season = data.get("season")
        if data.get("land_id"):
            crop.land_id = data.get("land_id")

        CropRepository.update(crop)
        return crop, 200