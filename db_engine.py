#!python
# encoding: UTF-8
# file: task_.py
# date
"""
Создать таблицы Brand(name), Car(model, release_year, brand(foreing key на
таблицу Brand)). Реализовать CRUD(создание, чтение, обновление по id, удаление
по id) для бренда и машины. Создать пользовательский интерфейс.
"""
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker, relationship, declarative_base  # , backref
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Date

engine = None

Base = declarative_base()


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "{}".format(self.name)


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    model = Column(String)
    release_year = Column(Date)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates='cars')


Brand.cars = relationship('Car', order_by=Car.id, back_populates='brand')


def main_func():
    """ Test function """
    global engine

    db_user = 'postgres'
    db_password = 'postgres'
    db_name = 'task_16'
    db_echo = True
    engine = create_engine(
        # "postgresql://postgres:postgres@localhost/test",
        f'postgresql://{db_user}:{db_password}@localhost/{db_name}',
        echo=db_echo,
    )
    if not database_exists(engine.url):
        create_database(engine.url)

        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        with session() as session1:
            brand1 = Brand(name='FastestThunder')
            car1 = Car(model='XVF-121', release_year='01/01/1960', brand=brand1)
            car2 = Car(model='ZKX-11', release_year='01/01/1959', brand=brand1)
            car3 = Car(model='GR-101', release_year='01/01/1951', brand=brand1)

            brand2 = Brand(name='TurtleHop')
            car4 = Car(model='TX-4', release_year='01/01/1971', brand=brand2)
            car5 = Car(model='KY-22', release_year='01/01/1955', brand=brand2)

            session1.add_all([brand1, brand2, car1, car2, car3, car4, car5])
            session1.commit()

    ds = engine.execute('select * from car join brand on car.brand_id = brand.id')
    for r in ds:
        print(f'{r.id} {r.model} {r.release_year} {r.name}')


if __name__ == '__main__':
    main_func()
