from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql.json import JSONB

Base = declarative_base()


class MetaVertex(Base):
    # Название таблицы
    __tablename__ = 'metavertex'

    # Primary key вершины, он в принципе не нужен,
    # но его проще оставить,
    # поскольку в случае с постгресом его нельзя просто так убрать
    id = Column(Integer, primary_key=True)

    # JSONB с данными вида
    # {"id": <АЙДИ ВЕРШИНЫ>, "parent": <АЙДИ РОДИТЕЛЬСКОЙ ВЕРШИНЫ>,
    # "value": <ЦЕЛОЧИСЛЕННОЕ ЗНАЧЕНИЕ ДЛЯ ФИЛЬТРАЦИИ>}
    data = Column(JSONB)


class Edge(Base):
    # Название таблицы
    __tablename__ = 'edge'

    # Primary key ребра, он в принципе не нужен, но его проще оставить,
    # поскольку в случае с постгресом его нельзя просто так убрать
    edge_id = Column(Integer, primary_key=True)

    # JSONB с данными вида
    # {"id": <АЙДИ ВЕРШИНЫ>, "from_id": <АЙДИ ПЕРВОЙ ВЕРШИНЫ>,
    # "to_id": <АЙДИ ВТОРОЙ ВЕРШИНЫ>
    # "parent": <АЙДИ РОДИТЕЛЬСКОЙ ВЕРШИНЫ>,
    # "value": <ЦЕЛОЧИСЛЕННОЕ ЗНАЧЕНИЕ ДЛЯ ФИЛЬТРАЦИИ>}
    data = Column(JSONB)
