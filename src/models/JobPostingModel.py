from .BaseDataModel import BaseDataModel
from .db_schemes.minirag import jobposting
from sqlalchemy import delete
from sqlalchemy.future import select
from bson.objectid import ObjectId
class jobpostingModel(BaseDataModel):

    def __init__(self, db_client):
        self.db_client = db_client


    
    async def create_jobposting(self, jobposting : jobposting):

        async with self.db_client() as session:
            async with session.begin():
                session.add(jobposting)
            await session.commit()
            await session.refresh(jobposting)
        
        return jobposting
    
    async def get_jobposting(self, jobposting_id:str):
        async with self.db_client() as session:
                jobposting_sql = select(jobposting).where(jobposting.jobposting_id == jobposting_id)

                result = await session.execute(jobposting_sql)

                jobposting = result.scalar_one_or_none()

        return jobposting
    
    async def insert_many_jobpostings(self, jobpostings:list, batch_size:int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(jobpostings), batch_size):
                    batch_jobposting = jobpostings[i:i+batch_size]

                    session.add_all(batch_jobposting)
            
            await session.commit()
        
        return len(jobpostings)

    async def delete_jobpostings_by_user_id(self, user_id:ObjectId):
        async with self.db_client() as session:
            async with session.begin():
                deletion_by_proj = delete(jobposting).where(jobposting.jobposting_user_id == user_id)
                result = await session.execute(deletion_by_proj)
            await session.commit()
            
            return result.rowcount


    async def get_user_jobpostings(self, user_id: ObjectId, page_no:int=1, page_size: int=50 ):
        async with self.db_client() as session:
            stmt = select(jobposting).where(jobposting.jobposting_user_id == user_id).offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()

        return records




        




