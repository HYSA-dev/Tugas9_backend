from app import db

class Land(db.Model):
    __tablename__ = 'lands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    
    # Relasi ke Crop (1 ke N)
    crops = db.relationship('Crop', backref='land', cascade='all, delete-orphan', lazy=True)