'''
This library implements the basic logic for the Pengine classes.
    - PengineBuilder: An interface for Pengine objects.
    - PengineState: For the current state of a Pengine Query, used in Pengine
    class.
    - Pengine: Base class used for performing queries -- this is the access
    point.
'''


class State(object):
    ''' State Machine Class.
        Initializes to start_state, and optionally an iterator of states, or
        an iterator of (start_state, end_state) transitions.

        Errors: ValueError is raised if a transition is not allowed.
    '''
    def __init__(self, start_state, states=None, transitions=None):
        self._current_state = start_state  # Initialize a starting state.
        self.states = start_state
        self.states = {}
        self.transitions = {}
        if states is not None:
            for state in states:
                self.states.add(state)
        if transitions is not None:
            for transition in transitions:
                start, end = transition
                self.states.add(start)
                self.states.add(end)
                self.add_transition(start, end)

    def add_transition(self, start, end):
        '''Adds an allowed state transition'''
        self.transitions.add((start, end))

    def change_state(self, target_state):
        current_state = self._current_state
        if (current_state, target_state) in self.transitions:
            self.current_state = target_state
        else:
            error_message = "Transitions from {0} to {1} not allowed".format(
                current_state, target_state)
            raise ValueError(error_message)


class PengineBuilder(object):
    def __init__(self):
        self.alias = None
        self.application = None
        self.ask = None
        self.chunk = None
        self.destroy = None
        self.format = None
        self.server = None
        self.srctext = None
        self.srcurl = None

    def PengineBuilder(self):
        pass

    def clone(self):
        pass

    def dumpDebugState():
        pass

    def getActualURL(self, action):
        pass

    def getActualURLWithId(self, action, id):
        pass

    def getAlias(self):
        pass

    def getApplication(self):
        pass

    def getAsk(self):
        pass

    def getChunk(self):
        pass

    def getRequestBodyAsk(self, id, ask):
        pass

    def getRequestBodyCreate(self):
        pass

    def getRequestBodyDestroy(self):
        pass

    def getRequestBodyNext(self):
        pass

    def getRequestBodyPullResponse(self):
        pass

    def getRequestBodyStop(self):
        pass

    def getRequestBodyStop2(self):
        pass

    def getServer(self):
        pass

    def getSrcText(self):
        pass

    def getSrcURL(self):
        pass

    def hasAsk(self):
        pass

    def isDestroy(self):
        pass

    def newPengine(self):
        pass

    def removeAsk(self):
        pass

    def setAlias(self, alias):
        pass

    def setApplication(self, application):
        pass

    def setAsk(self, ask):
        pass

    def setChunk(self, chunk):
        '''Chunk is a string.'''
        pass

    def setDestroy(self, destroy):
        '''destroy is a bool'''
        pass

    def setServer(self, urlstring):
        '''urlstring is a string'''
        pass

    def setServerByURL(self, server):
        '''server is a url'''
        pass

    def setSrcText(self, srctext):
        '''srctext is a string'''
        pass

    def setSrcURL(self, srcurl):
        '''srcurl a URL'''
        pass


class PengineState(State):
    def __init__(self):
        self.state = "not_created"
        # Initialize states
        self._states = {"not_created", "idle", "ask", "destroyed"}


class Pengine(object):
    def __init__(self):
        self.availOutput = None
        self.currentQuery = None
        self.pengineID = None
        self.po = None
        self.slave_limit = None
        self.state = None

    def ask(self, query):
        pass

    def create(self, po):
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

    def getCurrentQuery(self):
        pass

    def getId(self):
        pass

    def getOutput(self):
        pass

    def getSlaveLimit(self):
        pass

    def _handleAnswer(self, answer):
        pass

    def iAmFinished(self, query):
        pass

    def isDestroyed(self):
        pass

    def penginePost(self, url, contentType, body):
        pass


class Query(object):
    def __init__(self, pengine, ask, queryMaster):
        '''pengine :: Pengine, ask :: String, queryMaster :: Boolean'''
        self.availProofs = None
        self.hasMore = None
        self.pengine = None

    def addNewData(self, newDataPoints):
        '''newDataPoints :: JSON'''
        pass

    def dumpDebugState(self):
        pass

    def hasNext(self):
        pass

    def _next(self):
        pass

    def noMore(self):
        pass

    def stop(self):
        pass
