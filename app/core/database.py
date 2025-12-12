from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import make_url
from app.core.config import DATABASE_URL

Base = declarative_base()

# Ensure ssl requirement for Neon
url_obj = make_url(DATABASE_URL)
if "sslmode" not in url_obj.query:
    DATABASE_URL = f"{DATABASE_URL}&sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

def init_db():
    """
    Imports all ORM models and ensures tables exist.
    """
    import app.models.customer
    import app.models.vehicle
    import app.models.mechanic
    import app.models.part
    import app.models.service_request
    import app.models.repair_entry
    import app.models.invoice

    Base.metadata.create_all(bind=engine)
