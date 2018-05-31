from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from models.IdModels import Base
from models.IdModels import Relation as Edge
from models.IdModels import MetaVertex as Node
import time
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql.expression import cast

engine = create_engine("postgresql+psycopg2://maxavatar:1234@localhost:5433/id_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


def clear_db():
    session.query(Edge).delete()
    session.query(Node).delete()
    session.commit()


def add_remove_node(node_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0
    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1
    for n in range(max_id, max_id + node_count):
        s = time.time()
        session.add(Node(f"v{n}"))
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1

        print("+NODE id:{} --- {} seconds ---".format(n, time_delta))
    print("+NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(node_count):
        s = time.time()
        a = session.query(Node).filter(Node.node_id == max_id).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("-NODE id:{} --- {} seconds ---".format(max_id, time_delta))

        max_id -= 1

    print("-NODE {} --- AVG {} seconds ---".format(node_count, avg_time_total / avg_time_count))

    clear_db()


def add_remove_edge(edge_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    nodes = []
    for n in range(edge_count + 1):
        n = Node(f"v{n}")
        nodes.append(n)
        session.add(n)
        session.commit()

    edges = []
    for n in range(len(nodes) - 1):
        s = time.time()
        e = Edge(nodes[n], nodes[n])
        edges.append(e)
        session.add(e)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("+EDGE id:{} --- {} seconds ---".format(n, time_delta))
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
        print("-EDGE id:{} --- {} seconds ---".format(i, time_delta))
    print("-EDGE {} --- AVG {} seconds ---".format(edge_count, avg_time_total/avg_time_count))

    clear_db()


def edit_node(try_count=10):
    clear_db()

    avg_time_total = 0
    avg_time_count = 0

    session.add(Node("test_-1"))
    session.commit()

    for n in range(try_count):
        s = time.time()
        session.query(Node).filter(Node.name == "test_{}".format(n-1)).update({'name': "test_{}".format(n)})
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print("edit NODE id:{} --- {} seconds ---".format(n, time_delta))
    print("edit NODE {} --- AVG {} seconds ---".format(try_count, avg_time_total/avg_time_count))

    clear_db()


def get_flat(node_count=10):
    clear_db()

    nodes = []
    edges = []
    N = Node(f"v{0}")
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(node_count):
        a += 1
        n = Node(f"v{a}")
        Edge(False, n, nodes[-1])
        nodes.append(n)
        session.add(n)
        session.commit()

    s = time.time()
    item_num = int(node_count/2)
    item = session.query(Node).filter(Node.name == "v{}".format(item_num)).all()
    time_delta = time.time() - s
    print("FOUND ITEM v{} FLAT count:{} --- {} seconds ---".format(item_num, node_count, time_delta))

    clear_db()


def get_depth():
    pass


if __name__ == "__main__":
    # add_remove_node(100)
    #
    # add_remove_edge(100)

    # edit_node(10)

    get_flat(10)
