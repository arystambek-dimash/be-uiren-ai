import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.constants import SystemLanguage, EnglishLevel
from src.app.database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    age: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    system_language: orm.Mapped[SystemLanguage] = orm.mapped_column(
        sa.String,
        nullable=True,
        default=SystemLanguage.KAZAKH
    )
    learning_goal: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    current_english_level: orm.Mapped[EnglishLevel] = orm.mapped_column(sa.String, nullable=True)
    interests: orm.Mapped[list] = orm.mapped_column(sa.ARRAY(sa.String), default=list)
    daily_training_spend: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=5, comment="Минут өлшем бірлігі")
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(
        "users.id", ondelete="CASCADE"
    ),
        unique=True,
        nullable=False)
