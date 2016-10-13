from State import State
from Builder import PengineBuilder
from Query import Query
import copy


class Pengine(object):
    def __init__(self, builder=None, slave_limit=-1):
        self.availOutput = None
        self.currentQuery = None
        self.pengineID = None
        if builder is None:
            self.po = PengineBuilder()
        else:
            self.po = copy.deepcopy(builder)
        self.slave_limit = slave_limit
        self.state = State()

        # Initialize state transitions
        transitions = [("not_created", True, self.create, "idle"),
                       ("idle", self.hasCurrentQuery, self.runquery, "ask"),
                       ("ask", self.queryHasNext, self.__next__, "ask")]

    def hasCurrentQuery(self):
        if self.currentQuery is False:
            return False
        return True

    def queryHasNext(self):
        pass

    def ask(self, query):
        if self.currentQuery is not None:
            raise StateError("Have not extracted all answers " +
                             "from previous query.")
        self.currentQuery = Query(self, query, True)
        return self.currentQuery

    def create(self):
        pass

    def destroy(self):
        pass

    def doAsk(self, query, ask):
        pass

    def doNext(self, query):
        pass

    def doPullResponse(self):
        pass

    def doStop(self):
        pass

    def dumpStateDebug(self):
        pass

    def _handleAnswer(self, answer):
        pass

    def iAmFinished(self, query):
        pass

    def isDestroyed(self):
        pass

    def penginePost(self, url, contentType, body):
        pass

