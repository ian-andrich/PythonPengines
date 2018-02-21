# Python Pengines 0.1.2
This is a module for interfacing python with the Prolog Pengines knowledge base.

## API
Create a basic run pengine server script, and run it with swipl.
~~~~
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(pengines)).

server(Port) :- http_server(http_dispatch, [port(Port)]).

:- server(4242)
~~~~

Initialize a basic PengineBuilder
~~~~
pengine_builder = PengineBuilder(urlserver="http://localhost:4242")
~~~~

Create the pengine querying object.
~~~~
pengine = Pengine(builder=pengine_builder)
pengine.create()
~~~~

Make your query -- note the lack of ending period -- Pengine performs the query like 'ask(member(X, [1,2,3], [])).'
~~~~
query = "member(X, [1,2,3])"
pengine.ask(query)
print(pengine.currentQuery.availProofs)
~~~~

Iterate through the proofs like this:

~~~~
while pengine.currentQuery.hasMore:
    pengine.doNext(pengine.currentQuery)
    print(pengine.currentQuery.availProofs)
~~~~

Major API changes coming in 0.2.0

Right now each pengine is only good for one query.

## v.0.1.4 : More fat fingering.
## V.0.1.3 : Fat fingered some pypi code.
## V.0.1.2 : Added repo to pypi under the name PythonPengines
