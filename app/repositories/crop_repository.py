from app import db
from app.models.crop import Crop

class CropRepository:
    @staticmethod
    def get_all():
        return Crop.query.all()

    # Tambahan fungsi pagination & search
    @staticmethod
    def get_paginated(page, per_page, search):
        query = Crop.query
        if search:
            query = query.filter(Crop.name.ilike(f"%{search}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(crop_id):
        return Crop.query.get(crop_id)

    @staticmethod
    def save(crop):
        db.session.add(crop)
        db.session.commit()
        return crop

    @staticmethod
    def delete(crop):
        db.session.delete(crop)
        db.session.commit()

    @staticmethod
    def update(crop):
        db.session.commit()
        return crop