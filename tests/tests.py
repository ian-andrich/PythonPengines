from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine

factory = PengineBuilder(urlserver="http://localhost:4243")
pengine = Pengine(builder=factory)
