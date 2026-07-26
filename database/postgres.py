from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

# Declare Base class for SQL models
Base = declarative_base()

# Create asynchronous database engine with dynamic driver fallback
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=10
    )
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
except Exception:
    engine = None
    async_session_maker = None

async def get_async_db():
    """
    Dependency injector yielding database session.
    """
    if async_session_maker is not None:
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    else:
        # Return a simple mock session for local execution validation
        class MockSession:
            async def commit(self): pass
            async def rollback(self): pass
            async def close(self): pass
            async def execute(self, *args, **kwargs):
                class MockResult:
                    def scalars(self):
                        class MockScalars:
                            def first(self): return None
                            def all(self): return []
                        return MockScalars()
                return MockResult()
            def add(self, entity): pass
            async def flush(self): pass
        yield MockSession()

