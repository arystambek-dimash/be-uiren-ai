import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.database import Base


class User(Base):
    __tablename__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    email: orm.Mapped[sa.String] = orm.mapped_column(sa.String, unique=True)
    fullname: orm.Mapped[sa.String] = orm.mapped_column(sa.String)
    profile = orm.relationship('Profile', uselist=False,
                               lazy="selectin", )
