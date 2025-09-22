from .BaseDataModel import BaseDataModel
from .db_schemes.minirag import User
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func


class UserModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    async def create_user(self, user: User):
        async with self.db_client() as session:
            async with session.begin():
                session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user
            


    async def get_user_or_create_one(self, user_id: str):
        async with self.db_client() as session:
            async with session.begin():
                query = select(User).where(User.user_id==user_id)
                result = await session.execute(query)
                user = result.scalar_one_or_none()
                if user is None:
                    user_rec = User(
                        user_id = user_id
                    )
                    user = await self.create_user(user=user_rec)
                    return user
                else:
                    return user


    async def get_all_users(self, page: int=1, page_size: int=10):
        async with self.db_client() as session:
            async with session.begin():

                total_documents = await session.execute(select(
                    func.count( User.user_id )
                ))
                
                total_documents = total_documents.scalar_one()
                
                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1
                
                query = select(User).offset((page-1) * page_size ).limit(page_size)
                results = await session.execute(query).scalars().all()

                return results
