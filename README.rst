.. image:: https://travis-ci.org/ian-andrich/PythonPengines.svg?branch=master
    :target: https://travis-ci.org/ian-andrich/PythonPengines
Python Pengines
===============

This is a module for interfacing python with the Prolog Pengines
knowledge base.

API
---

Create a basic run pengine server script, and run it with swipl.

::

    :- use_module(library(http/thread_httpd)).
    :- use_module(library(http/http_dispatch)).
    :- use_module(library(pengines)).

    server(Port) :- http_server(http_dispatch, [port(Port)]).

    :- server(4242).

Initialize a basic PengineBuilder

::

    from pengines.Builder import PengineBuilder
    from pengines.Pengine import Pengine

    pengine_builder = PengineBuilder(urlserver="http://localhost:4242")

Create the pengine querying object.

::

    pengine = Pengine(builder=pengine_builder)

Make your query -- note the lack of ending period -- Pengine performs
the query like 'ask(member(X, [1,2,3], [])).'

::

    query = "member(X, [1,2,3])"
    pengine.doAsk(pengine.ask(query))
    print(pengine.currentQuery.availProofs)

Iterate through the proofs like this:

::

    while pengine.currentQuery.hasMore:
        pengine.doNext(pengine.currentQuery)
        print(pengine.currentQuery.availProofs)

Alternatively, the query can be provided to the builder:

::

    src_pl = "foo(a).\nfoo(b).\nfoo(c)."
    query = "foo(X)"
    factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, srctext=src_pl, ask=query)
    pengine = Pengine(builder=factory)
    results = pengine.currentQuery.availProofs
    print(results)

prologterms library
-------------------

The python library prologterms aims to make it easier to construct
prolog programs and query terms from within python.

For an example of how to use prologterms in conjunction with pengines,
see:

https://pypi.org/project/prologterms/

::

    from pengines.Builder import PengineBuilder
    from pengines.Pengine import Pengine
    from prologterms import TermGenerator, PrologRenderer, Program, Var

    P = TermGenerator()
    X = Var('X')
    Y = Var('Y')
    Z = Var('Z')
    R = PrologRenderer()

    p = Program(
        P.ancestor(X,Y) <= (P.parent(X,Z), P.ancestor(Z,Y)),
        P.ancestor(X,Y) <= P.parent(X,Y),
        P.parent('a','b'),
        P.parent('b','c'),
        P.parent('c','d')
    )

    q = P.ancestor(X,Y)

    factory = PengineBuilder(urlserver="http://localhost:4242",
                             srctext=R.render(p),
                             ask=R.render(q))
    pengine = Pengine(builder=factory, debug=True)
    while pengine.currentQuery.hasMore:
        pengine.doNext(pengine.currentQuery)
    for p in pengine.currentQuery.availProofs:
        print('{} <- {}'.format(p[X.name], p[Y.name]))
