from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from database.repositories.base import IRepository
from models.domain.task import TaskModel

class TaskRepository(IRepository[TaskModel]):
    """
    Asynchronous repository implementation for Task storage.
    """
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_by_id(self, id: str) -> Optional[TaskModel]:
        result = await self.db.execute(select(TaskModel).where(TaskModel.id == id))
        return result.scalars().first()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[TaskModel]:
        result = await self.db.execute(select(TaskModel).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def add(self, entity: TaskModel) -> TaskModel:
        self.db.add(entity)
        await self.db.flush() # Flush to populate generated columns/IDs
        return entity

    async def update(self, entity: TaskModel) -> TaskModel:
        self.db.add(entity)
        await self.db.flush()
        return entity

    async def delete(self, id: str) -> bool:
        task = await self.get_by_id(id)
        if task:
            await self.db.delete(task)
            return True
        return False
