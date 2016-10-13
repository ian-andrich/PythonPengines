from State import State
from Builder import PengineBuilder
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
        self.state = PengineState()

        # Initialize state transitions
        transitions = [("not_created", True, self.create, "idle"),
                       ("idle", self.currentQuery, self.runquery, "ask")]


    def ask(self, query):


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



class PengineState(State):
    def __init__(self):
        super().__init__("not_created", states={"not_created",
                                                "idle",
                                                "ask",
                                                "destroyed"})

