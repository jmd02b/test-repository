from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # same as: SELECT * from items where name=name LIMIT 1

    def upsert_to_db(self):
        db.session.add(self)
        db.session.commit()
        ''' same as: INSERT INTO items VALUES (name, price)
            session knows to either update or delete so if exists
            same as: UPDATE items SET price=price WHERE name=name
        '''

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
