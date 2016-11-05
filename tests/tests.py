from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

factory = PengineBuilder(urlserver="http://localhost:4242")
pengine = Pengine(builder=factory, debug=True)
pengine.ask("member(X, [1,2,3]).")
