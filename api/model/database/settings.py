from api import db


class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)

    active = db.Column(db.Boolean, default=False, nullable=False)

    web = db.Column(db.JSON(), nullable=True)
    api = db.Column(db.JSON(), nullable=True)

    def update(self, data):
        for key in data:
            setattr(self, key, data[key])

    def serialize(self):
        return {
            "id": self.id,
            "active": self.active,
            "web": self.web,
            "api": self.api
        }
