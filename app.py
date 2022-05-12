from urllib.error import HTTPError
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    func,
)

app = Flask('app')
PG_DSN = 'postgresql://postgres:756894@localhost:5432/flask_netology'
engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Advertisment(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key = True)
    title = Column(String(50), nullable = False)
    description = Column(String(150), nullable = False)
    created_at = Column(DateTime, server_default = func.now())
    author = Column(String(50), nullable = False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/create_ad/', methods=['POST'])
def create_ad():
    data_to_create = request.json

    with Session() as session:
        title = data_to_create['title']
        description = data_to_create['description']
        author = data_to_create['author']

        new_add = Advertisment(
            title = title,
            description = description,
            author = author
        )

        if new_add is None:
            raise HTTPError(401, "The ad wasn't created")

        session.add(new_add)
        session.commit()
    session.close()
    
    return jsonify({'status_code': 200, 'text': 'The record was successfully created'})

        


@app.route('/ads/', methods=['GET'])
def get_ads():
    ads_list = []
    with Session() as session:
        ads = session.query(Advertisment).all()
        for ad in ads:
            ads_dict = {}
            ads_dict['id'] = ad.id
            ads_dict['title'] = ad.title
            ads_dict['description'] = ad.description
            ads_dict['created_at'] = ad.created_at
            ads_dict['author'] = ad.author
            ads_list.append(ads_dict)
    session.close()
    return jsonify({'status_code': 200, 'text': 'Request was successfully made', 'ads': ads_list})

@app.route('/delete_ad/', methods=['DELETE'])
def delete_ad():
    id = request.json['id']
    with Session() as session:
        session.query(Advertisment).filter(Advertisment.id == id).delete()
        session.commit()
    session.close()

    return jsonify({'status_code': 201, 'text': 'The record was successfully deleted'})