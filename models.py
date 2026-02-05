from typing import Annotated

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import ARRAY

from database import Base

# pyright: reportUninitializedInstanceVariable=false

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_array = Annotated[list[str], mapped_column(ARRAY(String))]

organization_practice_table = Table(
    "organization_practice",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),  # pyright:ignore[reportUnknownArgumentType]
    Column("practice_id", ForeignKey("practice.id"), primary_key=True),  # pyright:ignore[reportUnknownArgumentType]
)


class Building(Base):
    __tablename__: str = "building"

    id: Mapped[int_pk]
    address: Mapped[str]  # lat,lng, N.E.
    coordinates: Mapped[str]

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building",
        cascade="all, delete-orphan",
    )


class Organization(Base):
    __tablename__: str = "organization"
    
    id: Mapped[int_pk]
    name: Mapped[str]
    phone_numbers: Mapped[str_array]
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    practices: Mapped[list["Practice"]] = relationship(
        secondary=organization_practice_table,
        back_populates="organizations",
    )


class Practice(Base):
    __tablename__: str = "practice"

    id: Mapped[int_pk]
    name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("practice.id"))

    parent: Mapped["Practice | None"] = relationship(
        back_populates="children",
        remote_side="Practice.id",
    )
    children: Mapped[list["Practice"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations: Mapped[list["Organization"]] = relationship(
        secondary=organization_practice_table,
        back_populates="practices",
    )

    @property
    def level(self):
        level = 0
        current = self.parent
        while current:
            level += 1
            current = current.parent
        return level
