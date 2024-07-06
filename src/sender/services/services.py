from datetime import datetime
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.sender.services.dals import AccountDAL, ContactDAL
from src.sender.services.hashing import Hasher
from src.worker.celery import send_messages_task


class SenderService:
    def __init__(self, db_session: AsyncSession):
        self.account_dal = AccountDAL(db_session=db_session)
        self.contact_dal = ContactDAL(db_session=db_session)
        self.hasher = Hasher()

    async def upload_accounts(
            self,
            accounts_data: List[Dict[str, str]]
    ) -> None:
        for account in accounts_data:
            await self.account_dal.add_account(
                client_id=account.get("client_id"),
                client_secret=account.get("client_secret"),
                code=account.get("code")
            )

    async def delete_accounts(self) -> None:
        await self.account_dal.delete_accounts()

    async def upload_contacts(
            self,
            contacts_data: str
    ) -> None:
        for contact in contacts_data:
            await self.contact_dal.add_contact(vk_id=contact[0])

    async def delete_contacts(self) -> None:
        await self.contact_dal.delete_contacts()

    @staticmethod
    async def send_message(
            message: str,
            minute: int,
            hour: int,
            day: int,
            month: int,
            year: int
    ) -> None:

        # send_messages_task.apply_async(
        #     (message, ),
        #     eta=datetime(
        #         minute=minute,
        #         hour=hour,
        #         day=day,
        #         month=month,
        #         year=year
        #     )
        # )

        send_messages_task(message)
