from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # list of ItemModels

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
