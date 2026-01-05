import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.database import Base


class UserAnswer(Base):
    __tablename__ = 'user_answers'
    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id", ondelete='CASCADE'))
    roadmap_edge_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("roadmap_edges.id", ondelete='CASCADE'))
    accuracy: orm.Mapped[float] = orm.mapped_column(sa.Float)

    created_at: orm.Mapped[sa.DateTime] = orm.mapped_column(sa.DateTime, server_default=sa.func.now())
