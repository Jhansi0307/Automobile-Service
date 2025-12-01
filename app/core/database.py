from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base   # << IMPORTANT

from app.core.config import DATABASE_URL

# SQLAlchemy Base Model
Base = declarative_base()   # << THIS MUST EXIST

# Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# Scoped session for thread safety
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# Initialize DB Tables
def init_db():
    import app.models.customer
    import app.models.vehicle
    import app.models.mechanic
    import app.models.part
    import app.models.service_request
    import app.models.repair_entry
    import app.models.invoice

    Base.metadata.create_all(bind=engine)
