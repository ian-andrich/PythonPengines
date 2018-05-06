from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

q = "between(1,1000,X)"
factory = PengineBuilder(urlserver="http://localhost:4242", destroy=False, ask=q)
pengine = Pengine(builder=factory, debug=True)
# Start query.
print()
print(pengine.currentQuery.availProofs, "Has More? ", pengine.currentQuery.hasMore)
print()
# Get next query.
print(pengine.state.current_state)
while pengine.currentQuery.hasMore:
    pengine.doNext(pengine.currentQuery)
print(pengine.currentQuery.availProofs)
