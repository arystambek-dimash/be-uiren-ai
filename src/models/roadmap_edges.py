import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.constants import EnglishLevel
from src.app.database import Base


class RoadmapEdges(Base):
    __tablename__ = 'roadmap_edges'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    level: orm.Mapped[EnglishLevel] = orm.mapped_column(sa.Enum(EnglishLevel))
    x: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=0)
    title: orm.Mapped[str] = orm.mapped_column(sa.String)
    description_of_edge: orm.Mapped[str] = orm.mapped_column(sa.String)
    __table_args__ = (
        sa.CheckConstraint('x >= -1 AND x <= 1', name='x_coordinate_constraint'),
    )
    study_words = orm.relationship("StudyWord", cascade="all, delete-orphan")
    questions = orm.relationship("Question", back_populates="edge", cascade="all, delete-orphan")
    user_answers = orm.relationship("UserAnswer", cascade="all, delete-orphan")
