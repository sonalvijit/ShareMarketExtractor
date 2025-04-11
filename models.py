from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from time import time as current_time
from os import path
from datetime import datetime

DATABASE_URI:str = "sqlite:///db/stocks.db"
Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(engine)

class Share(Base):
     __tablename__ = "shares"
     id = Column(Integer, primary_key=True)
     share_name = Column(String, unique=True, nullable=False)
     prices = relationship("SharePrice", back_populates="share", cascade="all, delete-orphan")

     def __repr__(self):
          return f"<Share(id={self.id}, share_name='{self.share_name}')>"
     
class SharePrice(Base):
     __tablename__ = "share_prices"
     id = Column(Integer, primary_key=True)
     share_id = Column(Integer, ForeignKey("shares.id"), nullable=False)
     share_value = Column(Float, nullable=False)
     share_pts = Column(Float, nullable=False)
     G_N_L = Column(String, nullable=False)
     timestamp = Column(Integer, default=int(current_time()), nullable=False)
     share = relationship("Share", back_populates="prices")

def initialize_database():
     if not path.exists("stocks.db"):
          Base.metadata.create_all(engine)
          print("Database created successfully.")
     else:
          print("Database already exists.")

def save_share_db(share_name:str, share_value:float, share_pts:float, G_N_L:str):
     session = Session()
     share = session.query(Share).filter_by(share_name=share_name).first()
     if not share:
          share = Share(share_name=share_name)
          session.add(share)
          session.commit()
     new_price = SharePrice(share_id=share.id, share_value=share_value, share_pts=share_pts, G_N_L=G_N_L)
     session.add(new_price)
     session.commit()
     session.close()
     # print(f"Saved {share_name} with value {share_value} to the database.")

def get_share_data(date: str, epoch:bool=False):
     session = Session()
     target_date = int(datetime.strptime(date + " " + datetime.now().strftime("%H:%M:%S"), "%d-%m-%Y %H:%M:%S").timestamp())
     shares = session.query(Share).all()
     share_data = {}

     for share in shares:
          latest_price = (
               session.query(SharePrice)
               .filter(SharePrice.share_id == share.id, SharePrice.timestamp <= target_date)
               .order_by(SharePrice.timestamp.desc())
               .first()
          )
          if latest_price:
               share_data[share.share_name] = {
                    "id": share.id,
                    "prices": [{
                         "share_value": latest_price.share_value,
                         "share_pts": latest_price.share_pts,
                         "G_N_L": latest_price.G_N_L,
                         "timestamp": latest_price.timestamp
                    }]
               }
     session.close()
     if epoch:
          print(f"Fetched share data for date {share_data}.")
     else:
          pass
     return [share_data, date]