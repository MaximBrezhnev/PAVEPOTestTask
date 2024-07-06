from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contact"

    contact_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    vk_id: Mapped[int] = mapped_column(unique=True)


class Account(Base):
    __tablename__ = "account"

    account_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    client_id: Mapped[int] = mapped_column(unique=True)
    client_secret: Mapped[str]
    code: Mapped[str]

