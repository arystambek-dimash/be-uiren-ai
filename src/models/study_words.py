import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.app.database import Base


class StudyWord(Base):
    __tablename__ = 'study_words'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    word_ru: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False)
    word_kk: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False)
    word_en: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False)

    usage_context_kk: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False)
    usage_context_en: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False)
    usage_context_ru: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False)

    edge_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("roadmap_edges.id", ondelete='CASCADE'))
