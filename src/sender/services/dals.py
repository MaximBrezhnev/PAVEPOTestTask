from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.sender.models import Account, Contact


class AccountDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_account(
            self,
            client_id: int,
            client_secret: str,
            code: str
    ) -> None:
        async with self.db_session.begin():
            account = Account(
                client_id=int(client_id),
                client_secret=client_secret,
                code=code
            )
            self.db_session.add(account)
            await self.db_session.flush()

    async def delete_accounts(self):
        async with self.db_session.begin():
            await self.db_session.execute(delete(Account))


class ContactDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_contact(self, vk_id: int) -> None:
        async with self.db_session.begin():
            contact = Contact(vk_id=int(vk_id))
            self.db_session.add(contact)
            await self.db_session.flush()

    async def delete_contacts(self):
        async with self.db_session.begin():
            await self.db_session.execute(delete(Contact))
