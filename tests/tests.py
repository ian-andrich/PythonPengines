from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

factory = PengineBuilder(urlserver="http://localhost:4242")
pengine = Pengine(builder=factory, debug=True)
# Start query.
pengine.ask("member(X, [1,2,3])")
print(pengine.currentQuery.availProofs, "Has More? ", pengine.currentQuery.hasMore)
# Get next query.
print(pengine.state.current_state)
while pengine.currentQuery.hasNext:
    pengine.doNext(pengine.currentQuery)
