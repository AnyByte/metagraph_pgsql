from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from models.IdModels import *
from models.IdModels import TreeNode as Node
import time
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql.expression import cast

engine = create_engine("postgresql+psycopg2://maxavatar:1234@localhost:5433/id_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


def add_node(node_count=10):
    avg_time_total = 0
    avg_time_count = 0
    max_id = session.query(func.max(TreeNode.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1
    for n in range(max_id, max_id + node_count):
        s = time.time()
        session.add(Node(f"v{n}"))
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"+NODE id:{n} --- {time_delta} seconds ---")
    print(f"+NODE {node_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def add_edge(edge_count=99):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(edge_count):

        if max_id > 1:
            n1 = session.query(Node).filter(Node.node_id == max_id - 1).one()
            n2 = session.query(Node).filter(Node.node_id == max_id - 2).one()

            s = time.time()

            session.add(Edge(n1, n2))
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
        print(f"-NODE id:{max_id} --- {time_delta} seconds ---")

        max_id -= 1

    print(f"-NODE {node_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


def remove_edge(edge_count=10):
    avg_time_total = 0
    avg_time_count = 0

    max_id = session.query(func.max(Node.node_id)).first()[0]
    max_id = 1 if max_id is None else int(max_id) + 1

    for n in range(edge_count):
        s = time.time()
        a = session.query(Edge).filter(Edge.higher_id == max_id - 2, Edge.lower_id == max_id - 1).one()
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
        session.query(Node).filter(Node.node_id == max_id - 1).update({'name': f"{Node.name} {n}"})
        session.commit()
        time_delta = time.time() - s
        avg_time_total += time_delta
        avg_time_count += 0 if time_delta == 0 else 1
        print(f"edit NODE id:{max_id} --- {time_delta} seconds ---")
    print(f"edit NODE {try_count} --- AVG {avg_time_total/avg_time_count} seconds ---")


if __name__ == "__main__":
    nodes = []
    edges = []
    N = Node(f"v{0}")
    nodes.append(N)
    session.add(N)
    session.commit()
    for a in range(1000):
        a += 1
        n = Node(f"v{a}", nodes[-1])
        nodes.append(n)
        session.add(n)
        session.commit()
        print(n)
    print('bb')
    session.commit()
    print('cc')

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v1").all()
    time_delta = time.time() - s
    print(f"AAA id:{1} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v9").all()
    time_delta = time.time() - s
    print(f"AAA id:{10} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v99").all()
    time_delta = time.time() - s
    print(f"AAA id:{100} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v499").all()
    time_delta = time.time() - s
    print(f"AAA id:{500} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v999").all()
    time_delta = time.time() - s
    print(f"AAA id:{1000} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v4999").all()
    time_delta = time.time() - s
    print(f"AAA id:{5000} --- {time_delta} seconds ---")

    s = time.time()
    max_id = session.query(Node).filter(Node.name == "v9999").all()
    time_delta = time.time() - s
    print(f"AAA id:{10000} --- {time_delta} seconds ---")

    # for x in range(499):
    #     edges.append(Edge(nodes[x], nodes[x+1]))
    # session.add_all(edges)

    session.commit()

    # edit_node(100)

    # start_time = time.time()
    # session.delete(N)
    # session.commit()
    #
    # print("--- %s seconds ---" % (time.time() - start_time))

    # edit_node(1000)
    # add_node(1000)
    # add_edge(999)
    # remove_edge(999)
    # remove_node()
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
