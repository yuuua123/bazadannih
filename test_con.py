import unittest
import psycopg2
from Storage import connect
class TestCon(unittest.TestCase):
    def testConn(self):
        conn = psycopg2.connect(dbname='Storage', user='postgres', 
                    password='Kim', host='localhost')
        self.assertEqual(conn.closed,False)
        conn.close()


unittest.main()
