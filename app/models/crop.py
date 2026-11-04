from app import db

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    land_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)