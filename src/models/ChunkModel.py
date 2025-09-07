from .BaseDataModel import BaseDataModel
from .db_schemes.minirag import Chunk
from sqlalchemy import delete
from sqlalchemy.future import select
from bson.objectid import ObjectId
class ChunkModel(BaseDataModel):

    def __init__(self, db_client):
        self.db_client = db_client


    
    async def create_chunk(self, chunk : Chunk):

        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        
        return chunk
    
    async def get_chunk(self, chunk_id:str):
        async with self.db_client() as session:
                chunk_sql = select(Chunk).where(Chunk.chunk_id == chunk_id)

                result = await session.execute(chunk_sql)

                chunk = result.scalar_one_or_none()

        return chunk
    
    async def insert_many_chunks(self, chunks:list, batch_size:int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch_chunk = chunks[i:i+batch_size]

                    session.add_all(batch_chunk)
            
            await session.commit()
        
        return len(chunks)

    async def delete_chunks_by_ptoject_id(self, project_id:ObjectId):
        async with self.db_client() as session:
            async with session.begin():
                deletion_by_proj = delete(Chunk).where(Chunk.chunk_project_id == project_id)
                result = await session.execute(deletion_by_proj)
            await session.commit()
            
            return result.rowcount


    async def get_project_chunks(self, project_id: ObjectId, page_no:int=1, page_size: int=50 ):
        async with self.db_client() as session:
            stmt = select(Chunk).where(Chunk.chunk_project_id == project_id).offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()

        return records




        




