import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.types import String

from models.DocModels import Base
from models.DocModels import Edge
from models.DocModels import MetaVertex as Node

sys.setrecursionlimit(20000)

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

        # print("+NODE id:{} --- {} seconds ---".format(n, time_delta))
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

        # print("-NODE id:{} --- {} seconds ---".format(max_id, time_delta))
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

        # print("+EDGE id:{} --- {} seconds ---".format(n, time_delta))
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

        # print("-EDGE id:{} --- {} seconds ---".format(n, time_delta))
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

        # print("edit NODE try:{} --- {} seconds ---".format(n, time_delta))
    print("edit NODE {} --- AVG {} seconds ---".format(try_count, avg_time_total / avg_time_count))

    clear_db()


def get_flat(node_count=10):
    clear_db()

    N = Node(data={'id': 0, 'parent': 0, 'value': 0})
    session.add(N)
    session.commit()
    for a in range(node_count + 1):
        a += 1
        n = Node(data={'id': a, 'parent': 0, 'value': 0})
        session.add(Edge(data={'from_id': 0, 'to_id': a, 'rel_type': 'rel', 'parent': 0, 'value': 0}))
        session.add(n)
        session.commit()

    s = time.time()
    items = session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == 0
                                       and Edge.data["rel_type"].astext.cast(String) == 'rel').all()
    for item in items:
        item = session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == item.data['to_id']).one()
    time_delta = time.time() - s
    print("FOUND FLAT count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def get_depth(node_count=10):
    clear_db()

    nodes = []

    N = Node(data={'id': 0, 'parent': 0, 'value': 0})
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node(data={'id': a, 'parent': 0, 'value': 0})
        session.add(Edge(data={'from_id': nodes[-1].data['id'], 'to_id': n.data['id'], 'rel_type': 'rel', 'parent': 0,
                               'value': 0}))
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    item = find_recur(session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == 0
                                                 and Edge.data["rel_type"].astext.cast(String) == 'rel').all())
    time_delta = time.time() - s
    print("FOUND DEPTH count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def del_depth(node_count=10):
    clear_db()

    nodes = []

    N = Node(data={'id': 0, 'parent': 0, 'value': 0})
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count + 1):
        a += 1
        n = Node(data={'id': a, 'parent': 0, 'value': 0})
        session.add(Edge(data={'from_id': nodes[-1].data['id'], 'to_id': n.data['id'], 'rel_type': 'rel', 'parent': 0,
                               'value': 0}))
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    del_recur(session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == 0
                                         and Edge.data["rel_type"].astext.cast(String) == 'rel').all())
    time_delta = time.time() - s
    print("DELETED DEPTH count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def del_flat(node_count=10):
    clear_db()

    N = Node(data={'id': 0, 'parent': 0, 'value': 0})
    session.add(N)
    session.commit()
    for a in range(node_count + 1):
        a += 1
        n = Node(data={'id': a, 'parent': 0, 'value': 0})
        session.add(Edge(data={'from_id': 0, 'to_id': a, 'rel_type': 'rel', 'parent': 0, 'value': 0}))
        session.add(n)
        session.commit()

    s = time.time()
    items = session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == 0
                                       and Edge.data["rel_type"].astext.cast(String) == 'rel').all()
    for item in items:
        session.delete(session.query(Edge).filter(Edge.data["to_id"].astext.cast(NUMERIC) == item.data['to_id']
                                                  and Edge.data["rel_type"].astext.cast(String) == 'rel').one())
        session.delete(session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == item.data['to_id']).one())
        session.commit()
    session.delete(session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == 0).one())
    session.commit()
    time_delta = time.time() - s
    print("DELETED FLAT count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def find_recur(nodes):
    for node in nodes:
        a = session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == node.data['to_id']
                                       and Edge.data["rel_type"].astext.cast(String) == 'rel').all()

        if len(a) == 0:
            return node

        return find_recur(a)


def del_recur(nodes):
    for node in nodes:
        a = session.query(Edge).filter(Edge.data["from_id"].astext.cast(NUMERIC) == node.data['to_id']
                                       and Edge.data["rel_type"].astext.cast(String) == 'rel').all()

        if len(a) == 0:
            session.delete(node)
            session.delete(
                session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == node.data['from_id']).one())
            session.delete(
                session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == node.data['to_id']).one())
            session.commit()
            return node

        session.delete(node)
        session.delete(session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == node.data['from_id']).one())
        session.commit()

        return del_recur(a)


if __name__ == "__main__":
    add_remove_node(10)

    add_remove_edge(10)

    edit_node(10)

    get_flat(10)

    get_flat(100)

    get_flat(500)

    get_flat(1000)

    get_flat(5000)

    get_flat(10000)

    get_depth(10)

    get_depth(100)

    get_depth(500)

    get_depth(1000)

    get_depth(5000)

    get_depth(10000)

    del_depth(10)

    del_depth(50)

    del_depth(100)

    del_flat(10)

    del_flat(50)

    del_flat(100)
