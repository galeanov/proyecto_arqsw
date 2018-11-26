
from project import db


class Losa(db.Model):


    __tablename__ = 'losas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    canchan = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(128), nullable=False)
    preciod = db.Column(db.String(128), nullable=False)
    precion = db.Column(db.String(128), nullable=False)

    def __init__(self, canchan, tipo, preciod, precion):
        self.canchan = canchan
        self.tipo = tipo
        self.preciod = preciod
        self.precion = precion

    def to_json(self):
        return {
            'id': self.id,
            'canchan': self.canchan,
            'tipo': self.tipo,
            'preciod': self.preciod,
            'precion': self.precion

        }