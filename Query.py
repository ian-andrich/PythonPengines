import Collections
'''
This library implements the basic logic for the Pengine classes.
    - PengineBuilder: An interface for Pengine objects.
    - PengineState: For the current state of a Pengine Query, used in Pengine
    class.
    - Pengine: Base class used for performing queries -- this is the access
    point.
'''

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
