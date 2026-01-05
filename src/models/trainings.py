import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.constants import TrainingType
from src.app.database import Base


class Training(Base):
    __tablename__ = 'trainings'

    id: orm.Mapped[int] = orm.mapped_column(sa.INTEGER, primary_key=True)
    accuracy: orm.Mapped[float] = orm.mapped_column(sa.FLOAT)
    type: orm.Mapped[TrainingType] = orm.mapped_column(sa.String)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'))
