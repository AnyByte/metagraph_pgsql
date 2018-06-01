import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from models.IdModels import Base
from models.IdModels import MetaVertex as Node
from models.IdModels import Relation as Edge

sys.setrecursionlimit(20000)

engine = create_engine("postgresql+psycopg2://maxavatar:1234@185.98.87.154:5432/id_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


def clear_db():
    session.query(Edge).delete()
    session.query(Node).delete()
    session.commit()


def add_remove_node(node_count=10):
    clear_db()

    nodes = []

    avg_time_total = 0
    avg_time_count = 0
    for n in range(node_count):
        n = Node("v{}".format(n))
        nodes.append(n)
        s = time.time()
        session.add(n)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1

        # print("+NODE id:{} --- {} seconds ---".format(n, time_delta))
    print("+NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in nodes:
        s = time.time()
        a = session.delete(n)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        # print("-NODE id:{} --- {} seconds ---".format(max_id, time_delta))

        max_id -= 1

    print("-NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    clear_db()


def add_remove_edge(edge_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    nodes = []
    for n in range(edge_count + 1):
        n = Node("v{}".format(n))
        nodes.append(n)
        session.add(n)
        session.commit()

    edges = []
    for n in range(len(nodes) - 1):
        s = time.time()
        e = Edge("", nodes[n], nodes[n + 1])
        edges.append(e)
        session.add(e)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        # print("+EDGE id:{} --- {} seconds ---".format(n, time_delta))
    print("+EDGE {} --- AVG {} seconds ---".format(edge_count, avg_time_total / avg_time_count))

    avg_time_total = 0
    avg_time_count = 0

    for i, e in enumerate(edges):
        s = time.time()
        session.delete(e)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        # print("-EDGE id:{} --- {} seconds ---".format(i, time_delta))
    print("-EDGE {} --- AVG {} seconds ---".format(edge_count, avg_time_total / avg_time_count))

    clear_db()


def edit_node(try_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    session.add(Node("test_-1"))
    session.commit()

    for n in range(try_count):
        s = time.time()
        session.query(Node).filter(Node.name == "test_{}".format(n - 1)).update({'name': "test_{}".format(n)})
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        # print("edit NODE id:{} --- {} seconds ---".format(n, time_delta))
    print("edit NODE {} --- AVG {} seconds ---".format(try_count, avg_time_total / avg_time_count))

    clear_db()


def get_flat(node_count=10):
    clear_db()

    N = Node("v{}".format(0))
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node("v{}".format(a))
        Edge("rel", N, n)
        session.add(n)
        session.commit()

    s = time.time()
    item = N.lower_relations
    time_delta = time.time() - s
    print("FOUND FLAT count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def get_depth(node_count=10):
    clear_db()

    nodes = []

    N = Node("v{}".format(0))
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node("v{}".format(a))
        Edge("rel", nodes[-1], n)
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    item = find_recur(N)
    time_delta = time.time() - s
    print("FOUND DEPTH count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def del_depth(node_count=10):
    clear_db()

    nodes = []

    N = Node("v{}".format(0))
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node("v{}".format(a))
        Edge("rel", nodes[-1], n)
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    del_recur(N)
    time_delta = time.time() - s
    print("DELETED DEPTH count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def del_flat(node_count=10):
    clear_db()

    nodes = []

    N = Node("v{}".format(0))
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node("v{}".format(a))
        Edge("rel", N, n)
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    del_recur(N)
    time_delta = time.time() - s
    print("DELETED FLAT count:{} --- {} seconds ---".format(node_count, time_delta))

    clear_db()


def find_recur(node):
    for lower_relation in node.lower_relations:
        find_recur(lower_relation.higher_node)
    return node


def del_recur(node):
    for lower_relation in node.lower_relations:
        del_recur(lower_relation.higher_node)
    session.delete(node)
    session.commit()


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
