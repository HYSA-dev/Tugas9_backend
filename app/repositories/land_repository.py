from app import db
from app.models.land import Land

class LandRepository:
    @staticmethod
    def get_all():
        return Land.query.all()

    @staticmethod
    def get_paginated(page, per_page, search):
        query = Land.query
        if search:
            query = query.filter(Land.name.ilike(f"%{search}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(land_id):
        return Land.query.get(land_id)

    @staticmethod
    def save(land):
        db.session.add(land)
        db.session.commit()
        return land

    @staticmethod
    def delete(land):
        db.session.delete(land)
        db.session.commit()

    @staticmethod
    def update(land):
        db.session.commit()
        return land