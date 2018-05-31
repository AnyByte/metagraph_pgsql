from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

Base = declarative_base()


class MetaVertex(Base):
    # Название таблицы
    __tablename__ = 'metavertex'

    # Primary key вершины
    id = Column(Integer, primary_key=True)

    # Название вершины (v1)
    name = Column(String(50), nullable=False)

    # Данные вершины
    data = Column(String)

    # При создании вершины указывается её имя (v1)
    # и опционально объект родительской вершины
    def __init__(self, name):
        self.name = name  # Вершине задаётся имя

    # Представление объекта
    def __repr__(self):
        return "MetaVertex(name=%r, node_id=%r)" % (
            self.name,
            self.id
        )

    # Список соседей справа, то есть
    # <ЭТА ВЕРШИНА> ---ребро---> Список айди вершин
    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    # Список соседей слева, то есть
    # Список айди вершин <---ребро--- <ЭТА ВЕРШИНА>
    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]

    # Список соседей справа, то есть
    # <ЭТА ВЕРШИНА> ---ребро---> Список айди вершин
    def higher_relations(self):
        return [x.higher_node for x in self.lower_relations]

    # Список соседей слева, то есть
    # Список айди вершин <---ребро--- <ЭТА ВЕРШИНА>
    def lower_relations(self):
        return [x.lower_node for x in self.higher_relations]


class Relation(Base):
    # Название таблицы
    __tablename__ = 'relation'

    # Тип связи
    rel_type = Column(String, nullable=False)

    # Внешний ключ начального айди ребра, зависимый от айди вершины
    # <ЭТОТ КЛЮЧ> ---ребро--->
    lower_id = Column(
        Integer,
        ForeignKey('metavertex.id'),
        primary_key=True)

    # Внешний ключ конечного айди ребра, зависимый от айди вершины
    # ---ребро---> <ЭТОТ КЛЮЧ>
    higher_id = Column(
        Integer,
        ForeignKey('metavertex.id'),
        primary_key=True)

    # Связь начальной вершины ребра от айди ребра из таблицы node
    lower_node = relationship(
        MetaVertex,
        primaryjoin=lower_id == MetaVertex.id,
        backref=backref('lower_edges', cascade="all,delete"))

    # Связь конечной вершины ребра от айди ребра из таблицы node
    higher_node = relationship(
        MetaVertex,
        primaryjoin=higher_id == MetaVertex.id,
        backref=backref('higher_edges', cascade="all,delete"))

    # Связь начальной вершины ребра от айди ребра из таблицы node
    lower_rel = relationship(
        MetaVertex,
        primaryjoin=lower_id == MetaVertex.id and rel_type == "rel",
        backref=backref('lower_relations', cascade="all,delete"))

    # Связь конечной вершины ребра от айди ребра из таблицы node
    higher_rel = relationship(
        MetaVertex,
        primaryjoin=higher_id == MetaVertex.id and rel_type == "rel",
        backref=backref('higher_relations', cascade="all,delete"))

    def __init__(self, rel, n1, n2):
        self.rel_type = rel  # Тип отношения
        self.lower_node = n1  # Начальная вершины
        self.higher_node = n2  # Конечная вершина
