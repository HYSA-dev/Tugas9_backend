from app import db
from app.models.owner import Owner

class OwnerRepository:
    @staticmethod
    def get_all():
        return Owner.query.all()

    @staticmethod
    def get_paginated(page, per_page, search):
        query = Owner.query
        if search:
            query = query.filter(Owner.name.ilike(f"%{search}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(owner_id):
        return Owner.query.get(owner_id)

    @staticmethod
    def save(owner):
        db.session.add(owner)
        db.session.commit()
        return owner

    @staticmethod
    def delete(owner):
        db.session.delete(owner)
        db.session.commit()

    @staticmethod
    def update(owner):
        db.session.commit()
        return owner