from app.repositories.land_repository import LandRepository
from app.models.land import Land


class LandService:
    @staticmethod
    def get_all_lands():
        lands = LandRepository.get_all()
        return [
            {"id": l.id, "name": l.name, "area": l.area, "owner_id": l.owner_id}
            for l in lands
        ]

    @staticmethod
    def create_land(data):
        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Field nama lahan wajib diisi"
        if not data or data.get("area") is None:
            errors["area"] = "Field luas lahan (area) wajib diisi"
        if not data or not data.get("owner_id"):
            errors["owner_id"] = "Field owner_id wajib diisi"

        if errors:
            return {"errors": errors}, 400

        new_land = Land(
            name=data.get("name"), area=data.get("area"), owner_id=data.get("owner_id")
        )
        LandRepository.save(new_land)
        return new_land, 201

    @staticmethod
    def delete_land(land_id):
        land = LandRepository.get_by_id(land_id)
        if not land:
            return None
        LandRepository.delete(land)
        return land

    @staticmethod
    def get_paginated_lands(page, per_page, search):
        pagination = LandRepository.get_paginated(page, per_page, search)

        items = [
            {"id": l.id, "name": l.name, "area": l.area, "owner_id": l.owner_id}
            for l in pagination.items
        ]

        return {
            "items": items,
            "pagination": {
                "current_page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
            },
        }

    @staticmethod
    def update_land(land_id, data):
        land = LandRepository.get_by_id(land_id)
        if not land:
            return None, 404

        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Nama lahan wajib diisi"
        if not data or data.get("area") is None:
            errors["area"] = "Luas lahan (area) wajib diisi"
            
        if errors:
            return {"errors": errors}, 400

        land.name = data.get("name")
        land.area = float(data.get("area"))
        if data.get("owner_id"):
            land.owner_id = data.get("owner_id")

        LandRepository.update(land)
        return land, 200