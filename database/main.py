# ----------------------------------------------------
#  FULL SQLALCHEMY MODELS + CRUD IN ONE FILE
# ----------------------------------------------------

from sqlalchemy import (
    Column, String, Integer, Text, TIMESTAMP, Float,
    ForeignKey, create_engine, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import uuid

# ----------------------------------------------------
# DATABASE SETUP
# ----------------------------------------------------
DATABASE_URL = "postgresql://username:password@localhost:5432/yourdb"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# ----------------------------------------------------
# MODELS
# ----------------------------------------------------

# ---------------- BUSINESS ----------------
class Business(Base):
    __tablename__ = "business"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    category = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    google_maps_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    reviews = relationship("Review", back_populates="business", cascade="all, delete")
    trend_logs = relationship("TrendLog", back_populates="business", cascade="all, delete")
    ai_results = relationship("AIResult", back_populates="business", cascade="all, delete")


# ---------------- REVIEWS ----------------
class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id"), nullable=False)

    reviewer_name = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
    platform = Column(Text, nullable=True)
    review_date = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    business = relationship("Business", back_populates="reviews")


# ---------------- TREND LOGS ----------------
class TrendLog(Base):
    __tablename__ = "trend_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id"), nullable=False)

    week = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    topic_trends = Column(JSONB, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())

    business = relationship("Business", back_populates="trend_logs")


# ---------------- AI RESULTS ----------------
class AIResult(Base):
    __tablename__ = "ai_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("business.id"), nullable=False)

    sentiment_pos = Column(Integer, nullable=True)
    sentiment_neg = Column(Integer, nullable=True)
    sentiment_neu = Column(Integer, nullable=True)

    top_topics = Column(JSONB, nullable=True)
    keywords = Column(JSONB, nullable=True)
    top_complaints = Column(JSONB, nullable=True)
    top_praises = Column(JSONB, nullable=True)

    ai_insights = Column(Text, nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    business = relationship("Business", back_populates="ai_results")


# ----------------------------------------------------
# CRUD FUNCTIONS
# ----------------------------------------------------

# ---------------- BUSINESS CRUD ----------------
def create_business(db, name, category, location, google_maps_url):
    business = Business(
        name=name,
        category=category,
        location=location,
        google_maps_url=google_maps_url
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


def get_business(db, business_id):
    return db.query(Business).filter(Business.id == business_id).first()


def list_businesses(db):
    return db.query(Business).all()


def update_business(db, business_id, data: dict):
    business = get_business(db, business_id)
    if not business:
        return None

    for key, value in data.items():
        setattr(business, key, value)

    db.commit()
    db.refresh(business)
    return business


def delete_business(db, business_id):
    business = get_business(db, business_id)
    if business:
        db.delete(business)
        db.commit()
        return True
    return False


# ---------------- REVIEWS CRUD ----------------
def create_review(db, business_id, reviewer_name, rating, text, platform, review_date):
    review = Review(
        business_id=business_id,
        reviewer_name=reviewer_name,
        rating=rating,
        text=text,
        platform=platform,
        review_date=review_date
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_reviews_by_business(db, business_id):
    return db.query(Review).filter(Review.business_id == business_id).all()


def delete_review(db, review_id):
    review = db.query(Review).filter(Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
        return True
    return False


# ---------------- TREND LOG CRUD ----------------
def create_trend_log(db, business_id, week, month, sentiment_score, topic_trends):
    log = TrendLog(
        business_id=business_id,
        week=week,
        month=month,
        sentiment_score=sentiment_score,
        topic_trends=topic_trends
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_trend_logs(db, business_id):
    return db.query(TrendLog).filter(TrendLog.business_id == business_id).all()


def delete_trend_log(db, log_id):
    log = db.query(TrendLog).filter(TrendLog.id == log_id).first()
    if log:
        db.delete(log)
        db.commit()
        return True
    return False


# ---------------- AI RESULT CRUD ----------------
def save_ai_result(db, business_id, data: dict):
    result = db.query(AIResult).filter(AIResult.business_id == business_id).first()

    if result:
        for key, value in data.items():
            setattr(result, key, value)
    else:
        result = AIResult(
            business_id=business_id,
            **data
        )
        db.add(result)

    db.commit()
    db.refresh(result)
    return result


def get_ai_results(db, business_id):
    return db.query(AIResult).filter(AIResult.business_id == business_id).first()


# ----------------------------------------------------
# CREATE TABLES
# ----------------------------------------------------
def init_db():
    Base.metadata.create_all(engine)
