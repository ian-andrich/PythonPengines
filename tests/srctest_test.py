"""
Assumes a bare-bones pengines service running on 4242

You can use this:

    docker run -p 4242:9083 -e PORT=9083 --name sparqlprog cmungall/sparqlprog

"""
from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

def test_src():
    """
    
    """
    src = "foo(a).\nfoo(b).\nfoo(c)."
    q = "foo(X)"
    factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, srctext=src, ask=q)
    pengine = Pengine(builder=factory, debug=True)
    results = pengine.currentQuery.availProofs
    print(results)
    assert len(results) == 3
    assert( {'X':'a'} in results )
    assert( {'X':'b'} in results )
    assert( {'X':'c'} in results )
