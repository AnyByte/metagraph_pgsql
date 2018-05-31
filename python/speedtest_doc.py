from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from models.DocModels import Base
from models.DocModels import Edge
from models.DocModels import MetaVertex as Node
import time
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql.expression import cast

engine = create_engine("postgresql+psycopg2://maxavatar:1234@185.98.87.154:5432/doc_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


def clear_db():
    session.query(Node).delete()
    session.query(Edge).delete()
    session.commit()


def add_remove_node(node_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0
    max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(max_id, max_id + node_count):
        s = time.time()
        session.add(Node(data={'id': n, 'parent': 0, 'value': 0}))
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1

        print("+NODE id:{} --- {} seconds ---".format(n, time_delta))
    print("+NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    avg_time_total = 0
    avg_time_count = 0
    for n in range(node_count):
        max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]
        s = time.time()
        a = session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == max_id).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1

        print("-NODE id:{} --- {} seconds ---".format(max_id, time_delta))
    print("-NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    clear_db()


def add_remove_edge(edge_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    for n in range(edge_count):
        s = time.time()
        session.add(Edge(data={'from_id': n, 'to_id': n + 1, 'parent': 0, 'value': 0}))
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("+EDGE id:{} --- {} seconds ---".format(n, time_delta))
    print("+EDGE {} --- AVG {} seconds ---".format(edge_count, avg_time_total / avg_time_count if avg_time_count > 0
    else 1))

    avg_time_total = 0
    avg_time_count = 0

    for n in range(edge_count):
        s = time.time()
        a = session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == n,
                                       Edge.data["to_id"].astext.cast(NUMERIC) == n + 1).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("-EDGE id:{} --- {} seconds ---".format(n, time_delta))
    print("-EDGE {} --- AVG {} seconds ---".format(edge_count, avg_time_total / avg_time_count if avg_time_count > 0
    else 1))

    clear_db()


def edit_node(try_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    session.add(Node(data={'id': 0, 'parent': 0, 'value': 0}))
    session.commit()

    for n in range(try_count):
        s = time.time()
        session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == 0).update({'data': {'id': 0,
                                                                                               'parent': 0,
                                                                                               'value': n}},
                                                                                     synchronize_session='fetch')
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("edit NODE try:{} --- {} seconds ---".format(n, time_delta))
    print("edit NODE {} --- AVG {} seconds ---".format(try_count, avg_time_total / avg_time_count))

    clear_db()


if __name__ == "__main__":
    # add_remove_node(100)

    # add_remove_edge(100)

    edit_node(10)
