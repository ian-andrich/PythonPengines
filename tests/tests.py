from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False)
pengine = Pengine(builder=factory, debug=True)
# Start query.
pengine.ask("member(X, [1,2,3])")
pengine.doAsk(pengine.currentQuery)
print()
print(pengine.currentQuery.availProofs, "Has More? ", pengine.currentQuery.hasMore)
print()
# Get next query.
print(pengine.state.current_state)
while pengine.currentQuery.hasMore:
    pengine.doNext(pengine.currentQuery)
