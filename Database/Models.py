# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, ENUM
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dept(Base):
    __tablename__ = 'dept'

    dept_id = Column(CHAR(60, 'utf8mb4_unicode_ci'), primary_key=True)
    dept_name = Column(CHAR(60, 'utf8mb4_unicode_ci'), nullable=False)


class Clas(Base):
    __tablename__ = 'class'

    class_id = Column(CHAR(60, 'utf8mb4_unicode_ci'), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    class_name = Column(CHAR(60, 'utf8mb4_unicode_ci'), nullable=False)

    dept = relationship('Dept')


class Service(Base):
    __tablename__ = 'service'

    service_id = Column(CHAR(60, 'utf8mb4_unicode_ci'), primary_key=True)
    dept_id = Column(ForeignKey('dept.dept_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    service_name = Column(CHAR(60, 'utf8mb4_unicode_ci'), nullable=False)

    dept = relationship('Dept')


class Worker(Base):
    __tablename__ = 'worker'

    worker_id = Column(CHAR(60, 'utf8mb4_unicode_ci'), primary_key=True)
    class_id = Column(ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    dept_id = Column(ForeignKey('dept.dept_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    worker_name = Column(CHAR(60, 'utf8mb4_unicode_ci'), nullable=False)
    role = Column(ENUM('normal', 'group', 'super'), nullable=False)
    pwd = Column(CHAR(120, 'utf8mb4_unicode_ci'), nullable=False)

    _class = relationship('Clas')
    dept = relationship('Dept')


class ServiceRecord(Base):
    __tablename__ = 'service_record'

    service_record_id = Column(BIGINT(20), primary_key=True)
    service_id = Column(ForeignKey('service.service_id'), nullable=False, index=True)
    service_name = Column(CHAR(60, 'utf8mb4_unicode_ci'), nullable=False)
    service_time = Column(DateTime)
    dept_id = Column(ForeignKey('dept.dept_id'), nullable=False, index=True)
    buyer_company = Column(CHAR(60, 'utf8mb4_unicode_ci'))
    seller_company = Column(CHAR(60, 'utf8mb4_unicode_ci'))
    worker_id = Column(ForeignKey('worker.worker_id'), nullable=False, index=True)
    cost = Column(Float, nullable=False)

    dept = relationship('Dept')
    service = relationship('Service')
    worker = relationship('Worker')
