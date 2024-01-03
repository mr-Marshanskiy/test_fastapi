from sqlalchemy import Column, String, Text

from common.models import DateMixin


class Article(DateMixin):
    __tablename__ = 'articles_article'
    title = Column(String(255), nullable=False)
    text = Column(Text(), nullable=False)
