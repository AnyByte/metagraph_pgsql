"""a directed graph example."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.decorators import *
from models.DocModels import *
import time


engine = create_engine("postgresql+psycopg2://maxavatar:1234@localhost:5432/doc_mgraph", echo=False)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()

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

if __name__ == "__main__":
    for n in range(10):
        start_time = time.time()
        session.add(Node())
        session.commit()
        print("--- %s seconds ---" % (time.time() - start_time))

# import time
#
# print(len(m.get_submeta_nodes('m1')))
#
