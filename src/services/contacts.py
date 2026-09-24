from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactCreate):
        await self._ensure_email_is_free(body.email)
        try:
            return await self.repository.create_contact(body)
        except IntegrityError:
            await self.repository.db.rollback()
            raise _email_conflict()

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ):
        return await self.repository.get_contacts(
            skip, limit, first_name, last_name, email
        )

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        if body.email is not None:
            await self._ensure_email_is_free(body.email, exclude_id=contact_id)
        try:
            return await self.repository.update_contact(contact_id, body)
        except IntegrityError:
            await self.repository.db.rollback()
            raise _email_conflict()

    async def remove_contact(self, contact_id: int):
        return await self.repository.remove_contact(contact_id)

    async def get_upcoming_birthdays(self, days: int = 7):
        return await self.repository.get_upcoming_birthdays(days)

    async def _ensure_email_is_free(self, email: str, exclude_id: int | None = None):
        existing = await self.repository.get_contact_by_email(email)
        if existing is not None and existing.id != exclude_id:
            raise _email_conflict()


def _email_conflict() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Contact with this email already exists",
    )
