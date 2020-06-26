"""
Assumes a bare-bones pengines service running on 4242

You can use this:

    docker run -p 4242:9083 -e PORT=9083 --name sparqlprog cmungall/sparqlprog

"""
import unittest
from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

from tests.log_testing import log_tests
import logging

log_tests(logging.DEBUG)

class PenginesTestCase(unittest.TestCase):

    def test_member(self):
        """

        """
        q = "member(X,[1,2,3])"
        factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, ask=q)
        pengine = Pengine(builder=factory)
        results = pengine.currentQuery.availProofs
        print(results)
        self.assertTrue(len(results) == 3)
        self.assertTrue( {'X':1} in results )
        self.assertTrue( {'X':2} in results )
        self.assertTrue( {'X':3} in results )

    def test_src(self):
        """

        """
        src = "foo(a).\nfoo(b).\nfoo(c)."
        q = "foo(X)"
        factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, srctext=src, ask=q)
        pengine = Pengine(builder=factory)
        results = pengine.currentQuery.availProofs
        print(results)
        self.assertTrue(len(results) == 3)
        self.assertTrue( {'X':'a'} in results )
        self.assertTrue( {'X':'b'} in results )
        self.assertTrue( {'X':'c'} in results )

    def test_chunk(self):
        """

        """
        src = "foo(a).\nfoo(b).\nfoo(c)."
        q = "foo(X)"
        factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, srctext=src, chunk=1, ask=q)
        pengine = Pengine(builder=factory)
        all_results = []
        results = pengine.currentQuery.availProofs
        print('INIT Results={}'.format(results))
        self.assertTrue(len(results) == 1)
        while pengine.currentQuery.hasMore:
            pengine.doNext(pengine.currentQuery)
            results = pengine.currentQuery.availProofs
            print('NEXT Results={}'.format(results))
        self.assertTrue( {'X':'a'} in results )
        self.assertTrue( {'X':'b'} in results )
        self.assertTrue( {'X':'c'} in results )
        self.assertEquals(len(results), 3)

    def test_iterator(self):
        """

        """
        q = "member(X,[1,2,3,4,5,6,7,8,9,10])"
        chunk_sizes = [1,2,3,4,100]

        for chunk in chunk_sizes:
            factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, chunk=chunk, ask=q)
            pengine = Pengine(builder=factory)
            results = []
            for r in pengine.currentQuery:
                print('ITER={}'.format(r))
                results.append(r)

            self.assertTrue(len(results) == 10)
            self.assertTrue( {'X':1} in results )
            self.assertTrue( {'X':2} in results )
            self.assertTrue( {'X':3} in results )



if __name__ == '__main__':
    unittest.main()
