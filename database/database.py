import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from database.models import Cash, Base

logger = logging.getLogger(__name__)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username="postgres",
    password="admin123",
    host="db",
    database="postgres",
    port=5432
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        logger.exception("Session rollback because of exception")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    try:
        session = next(get_db())

        basic_data = [
            {"val": 200, "bill_type": "B", "amount": 1},
            {"val": 100, "bill_type": "B", "amount": 2},
            {"val": 20, "bill_type": "B", "amount": 5},
            {"val": 10, "bill_type": "C", "amount": 10},
            {"val": 5, "bill_type": "C", "amount": 10},
            {"val": 1, "bill_type": "C", "amount": 10},
            {"val": 0.1, "bill_type": "C", "amount": 1},
            {"val": 0.01, "bill_type": "C", "amount": 10}
        ]
        count = session.query(Cash).count()
        if count == 0:
            for bill in basic_data:
                cash = Cash(val=bill["val"], type=bill["bill_type"],
                            amount=bill["amount"])
                session.add(cash)
            session.commit()
    except Exception as e:
        logger.error(e)
