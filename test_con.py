import unittest
import psycopg2
import Storage
from unittest import mock

class TestFunction(unittest.TestCase):
    @mock.patch('Storage.connect')
    def test_connect_func(self, mock_connect):
        mock_connect.return_value=psycopg2.connect(dbname='Storage', user='postgres', 
                        password='Kim', host='localhost')
        self.assertEqual(mock_connect.return_value.closed,False)

    @mock.patch('Storage.connect')
    def test_connect_func_fail(self, mock_connect):
        mock_connect.return_value=psycopg2.connect(dbname='Storage', user='postgres', 
                        password='NeKim', host='localhost')
        self.assertEqual(mock_connect.return_value.closed,False)

    @mock.patch('psycopg2.connect')
    def test_select_func(self,mock_connect):
        expected=[[3]]
        mock_con = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_cur = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur.fetchall.return_value = expected  # return this when calling cur.fetchall()

        result = Storage.select(mock_cur)
        self.assertEqual(result, expected)






if __name__=='__main__':
    unittest.main()
