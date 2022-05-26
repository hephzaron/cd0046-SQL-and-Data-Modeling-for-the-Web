##Run this file to persist second set of data into the database after initial data that was sent

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Artist, Genre, MusicGenre
from decouple import config
import sys

app = Flask(__name__)
DATABASE_USERNAME=config('DATABASE_USERNAME')
DATABASE_PASSWORD=config('DATABASE_PASSWORD')
DATABASE_SERVER=config('DATABASE_SERVER')
DATABASE_NAME=config('DATABASE_NAME')
SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')

app.config[
  'SQLALCHEMY_DATABASE_URI'
  ] = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

genre1 = Genre()

