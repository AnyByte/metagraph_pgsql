from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from models.DocModels import *
import time
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql.expression import cast

engine = create_engine("postgresql+psycopg2://maxavatar:1234@localhost:5433/doc_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


def add_node(node_count=100):
    avg_time_total = 0
    avg_time_count = 0
    max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1
    for n in range(max_id, max_id + node_count):
        s = time.time()
        session.add(Node(data={'id': n}))
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"+NODE id:{n} --- {time_delta} seconds ---")
    print(f"+NODE {node_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def add_edge(edge_count=99):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(edge_count):

        if max_id > 1:
            s = time.time()
            session.add(Edge(data={'lower_id': max_id-1, 'higher_id': max_id}))
            session.commit()
            time_delta = time.time() - s
            avg_time_total += time_delta
            avg_time_count += 0 if time_delta == 0 else 1
            print(f"+EDGE id:{n} --- {time_delta} seconds ---")

            max_id -= 1

    print(f"+EDGE {edge_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def remove_node(node_count=10):
    avg_time_total = 0
    avg_time_count = 0
    s = time.time()
    for n in range(node_count):
        max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]

        a = session.query(Node).filter(Node.data["id"].astext.cast(NUMERIC) == max_id).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
    print(f"-NODE id:{max_id} --- {time_delta} seconds ---")
    # print(f"-NODE {node_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def remove_edge(edge_count=10):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(edge_count):
        s = time.time()
        a = session.query(Edge).filter(Edge.data["lower_id"].astext.cast(NUMERIC) == max_id-2,
                                       Edge.data["higher_id"].astext.cast(NUMERIC) == max_id - 1).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"-EDGE id:{max_id} --- {time_delta} seconds ---")

        max_id -= 1

    print(f"-EDGE {edge_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def add_metavertex(edge_count=10):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(edge_count):
        s = time.time()
        a = session.query(Edge).filter(Edge.data["lower_id"].astext.cast(NUMERIC) == max_id-2,
                                       Edge.data["higher_id"].astext.cast(NUMERIC) == max_id - 1).one()
        session.delete(a)
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"-EDGE id:{max_id} --- {time_delta} seconds ---")

        max_id -= 1

    print(f"-EDGE {edge_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def edit_node(try_count=10):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(try_count):
        s = time.time()
        session.query(Node).filter(Node.node_id == max_id - 1).update({'data': {'value': n}})
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"edit EDGE id:{max_id} --- {time_delta} seconds ---")
    print(f"edit EDGE {try_count} --- AVG {avg_time_total/avg_time_count} seconds ---")

# create a directed graph like this:
#       n1 -> n2 -> n1
#                -> n5
#                -> n7
#          -> n3 -> n6


# n1 = Node()
# n2 = Node()
# n3 = Node()
# n4 = Node()
# n5 = Node()
# n6 = Node()
# n7 = Node()
#
# Edge(n1, n2)
# Edge(n1, n3)
# Edge(n2, n1)
# Edge(n2, n5)
# Edge(n2, n7)
# Edge(n3, n6)
#
# session.add_all([n1, n2, n3, n4, n5, n6, n7])
# session.commit()
#
# assert [x for x in n3.higher_neighbors()] == [n6]
# assert [x for x in n3.lower_neighbors()] == [n1]
# assert [x for x in n2.lower_neighbors()] == [n1]
# assert [x for x in n2.higher_neighbors()] == [n1, n5, n7]


def find(node_count, a):
    avg_time_total = 0
    avg_time_count = 0

    ids = []

    max_id = session.query(func.max(Node.data["id"].astext.cast(NUMERIC))).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    ids.append(0)

    session.add(Node(data={'id': 0, 'parent': None, 'value': 0}))
    session.commit()

    for n in range(max_id, max_id + node_count):
        # s = time.time()

        val = a if n == (max_id + node_count) - 1 else 0

        session.add(Node(data={'id': n, 'parent': ids[-1], 'value': val}))
        session.commit()

        ids.append(n)
        # time_delta = time.time() - s
        # avg_time_total += time_delta
        # avg_time_count += 0 if time_delta == 0 else 1
    #     print(f"+NODE id:{n} --- {time_delta} seconds ---")
    # print(f"+NODE {node_count} --- AVG {avg_time_total/avg_time_count} seconds ---")

    s = time.time()

    max_id = session.query(Node).filter(Node.data["parent"].astext.cast(NUMERIC) == 0,
                                        Node.data["value"].astext.cast(NUMERIC) == a).all()

    time_delta = time.time() - s
    print(f"AAA id:{node_count} --- {time_delta} seconds ---")


if __name__ == "__main__":
    find(10, 1)
    session.query(Node).delete()
    find(10, 1)
    session.query(Node).delete()
    find(10, 1)
    session.query(Node).delete()
    find(10, 1)
    session.query(Node).delete()
    find(50, 2)
    session.query(Node).delete()
    find(100, 2)
    session.query(Node).delete()
    find(50, 2)
    find(500, 3)
    find(1000, 4)
    find(5000, 5)
    find(10000, 6)
    # edit_node(1000)

    # add_node(11)
    # remove_node(11)
    #
    # add_edge(999)
    # remove_edge(998)
    # a = session.query(Node).filter(
    #     Node.data["id"].astext.cast(NUMERIC) == 0
    # ).all()
    # print("kek")
    # for n in range(10):
    #     start_time = time.time()
    #     session.add(Node())
    #     session.commit()
    #     print("--- %s seconds ---" % (time.time() - start_time))

# import time
#
# print(len(m.get_submeta_nodes('m1')))
#
