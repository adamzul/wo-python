from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:@localhost/wo')
Session_db = sessionmaker(bind=engine)

Base = declarative_base()