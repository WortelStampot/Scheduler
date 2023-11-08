from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

## models ##
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Roles(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    day: Mapped[str] = mapped_column(String)
    callTime: Mapped[str] = mapped_column(String)
    qualifiedStaff: Mapped[str] = mapped_column(String)

class Staff(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    maxShifts: Mapped[str] = mapped_column(String)
    availability: Mapped[str] = mapped_column(String)
    rolePreference: Mapped[str] = mapped_column(String)

class Input(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    weekOf: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)

class Schedule(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roles: Mapped[str] = mapped_column(String)
    staff: Mapped[str] = mapped_column(String)
    algorithm: Mapped[str] = mapped_column(String)
    matching: Mapped[str] = mapped_column(String)
    weekOf: Mapped[str] = mapped_column(String)
    timestamp: Mapped[str] = mapped_column(String)