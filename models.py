from datetime import datetime, timezone
from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(200))
    category = db.Column(db.String(100))
    calories = db.Column(db.Float)
    weight_g = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "calories": self.calories,
            "weight_g": self.weight_g,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
