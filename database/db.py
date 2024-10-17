from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    import database.models
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
from database.models import User, Keyword
from sqlalchemy.orm import Session

def get_user(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, telegram_id: int):
    user = User(telegram_id=telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def add_keyword_user(telegram_id: int, keyword: str):
    db = SessionLocal()
    user = get_user(db, telegram_id)
    if not user:
        user = create_user(db, telegram_id)
    keyword_entry = Keyword(keyword=keyword, user=user)
    db.add(keyword_entry)
    db.commit()
    db.close()

def remove_keyword_user(telegram_id: int, keyword: str):
    db = SessionLocal()
    user = get_user(db, telegram_id)
    if user:
        keyword_entry = db.query(Keyword).filter(Keyword.user_id == user.id, Keyword.keyword == keyword).first()
        if keyword_entry:
            db.delete(keyword_entry)
            db.commit()
    db.close()

def get_keywords_user(telegram_id: int):
    db = SessionLocal()
    user = get_user(db, telegram_id)
    if user:
        keywords = [k.keyword for k in user.keywords]
    else:
        keywords = []
    db.close()
    return keywords

def edit_keyword_user(telegram_id: int, old_keyword: str, new_keyword: str):
    db = SessionLocal()
    user = get_user(db, telegram_id)
    if user:
        keyword_entry = db.query(Keyword).filter(Keyword.user_id == user.id, Keyword.keyword == old_keyword).first()
        if keyword_entry:
            keyword_entry.keyword = new_keyword
            db.commit()
    db.close()