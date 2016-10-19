from Builder import PengineBuilder
from Pengine import Pengine

factory = PengineBuilder(urlserver="http://localhost:4243/")
pengine = Pengine(builder=factory)
