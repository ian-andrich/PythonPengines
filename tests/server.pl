:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(pengines)).

server(Port) :- http_server(http_dispatch, [port(Port)]).

:- server(4242),T is 10**10,sleep(T).
