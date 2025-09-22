from .BaseDataModel import BaseDataModel
from .db_schemes.minirag import Experience
from sqlalchemy import delete
from sqlalchemy.future import select
from bson.objectid import ObjectId
class ExperienceModel(BaseDataModel):

    def __init__(self, db_client):
        self.db_client = db_client


    async def create_experience(self, experience : Experience):
        async with self.db_client() as session:
            async with session.begin():
                session.add(experience)
            await session.commit()
            await session.refresh(experience)
        
        return experience
    
    async def get_experience(self, experience_id:str):
        async with self.db_client() as session:
                experience_sql = select(Experience).where(Experience.experience_id == experience_id)

                result = await session.execute(experience_sql)

                experience = result.scalar_one_or_none()

        return experience
    
    async def insert_many_experiences(self, experiences:list, batch_size:int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(experiences), batch_size):
                    batch_experience = experiences[i:i+batch_size]

                    session.add_all(batch_experience)
            
            await session.commit()
        
        return len(experiences)

    async def delete_experiences_by_user_id(self, user_id:ObjectId):
        async with self.db_client() as session:
            async with session.begin():
                deletion_by_proj = delete(Experience).where(Experience.experience_id == user_id)
                result = await session.execute(deletion_by_proj)
            await session.commit()
            
            return result.rowcount


    async def get_user_experiences(self, user_id: ObjectId, page_no:int=1, page_size: int=50 ):
        async with self.db_client() as session:
            stmt = select(Experience).where(Experience.experience_id == user_id).offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()

        return records