from app.repositories.owner_repository import OwnerRepository
from app.models.owner import Owner

class OwnerService:
    @staticmethod
    def get_paginated_owners(page, per_page, search):
        pagination = OwnerRepository.get_paginated(page, per_page, search)
        
        items = [{"id": o.id, "name": o.name, "contact": o.contact} for o in pagination.items]
        
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
    def get_all_owners():
        owners = OwnerRepository.get_all()
        return [{"id": o.id, "name": o.name, "contact": o.contact} for o in owners]

    @staticmethod
    def create_owner(data):
        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Field nama pemilik wajib diisi"
        if not data or not data.get("contact"):
            errors["contact"] = "Field kontak wajib diisi"
            
        if errors:
            return {"errors": errors}, 400 # Kembalikan error validasi

        new_owner = Owner(name=data.get("name"), contact=data.get("contact"))
        OwnerRepository.save(new_owner)
        return new_owner, 201

    @staticmethod
    def delete_owner(owner_id):
        owner = OwnerRepository.get_by_id(owner_id)
        if not owner:
            return None
        OwnerRepository.delete(owner)
        return owner

    @staticmethod
    def update_owner(owner_id, data):
        owner = OwnerRepository.get_by_id(owner_id)
        if not owner:
            return None, 404

        errors = {}
        if not data or not data.get("name"):
            errors["name"] = "Field nama pemilik wajib diisi"
        
        if errors:
            return {"errors": errors}, 400

        # Update data pemilik
        owner.name = data.get("name")
        owner.contact = data.get("contact", owner.contact)
        
        OwnerRepository.update(owner)
        return owner, 200