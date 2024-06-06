import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5433/computer-information"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the ComputerInfo model
class ComputerInfoDB(Base):
    __tablename__ = "computer_info"
    
    ip = Column(String, primary_key=True)
    computer_name = Column(String, nullable=False)
    cpu_temp = Column(Float)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    os = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class ComputerInfo(BaseModel):
    ip: str 
    computer_name: str 
    cpu_temp: float | None = None
    cpu_usage: float | None = None
    memory_usage: float 
    os: str
    time: datetime.datetime

@app.post("/register")
async def register_computer_info(raw_info: ComputerInfo):
    db = SessionLocal()
    computer_info = ComputerInfoDB(
        ip=raw_info.ip,
        computer_name=raw_info.computer_name,
        cpu_temp=raw_info.cpu_temp,
        cpu_usage=raw_info.cpu_usage,
        memory_usage=raw_info.memory_usage,
        os=raw_info.os,
        created_at=raw_info.time
    )
    try:
        db.add(computer_info)
        db.commit()
        db.refresh(computer_info)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return raw_info