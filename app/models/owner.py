from app import db

class Owner(db.Model):
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=True)
    
    # Relasi ke Land (1 ke N)
    lands = db.relationship('Land', backref='owner', cascade='all, delete-orphan', lazy=True)