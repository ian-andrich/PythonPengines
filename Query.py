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
    def __init__(self, pengine):
        '''pengine :: Pengine, ask :: String, queryMaster :: Boolean'''
        self.availProofs = None
        self.hasMore = True
        self.pengine = pengine

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
        if not self.hasMore:
            return

        self.hasMore = False
        if not self.availProofs:
            p.iAmFinished(self)

    def stop(self):
        pass

    def addNewData(self, data):
        '''
        Returns True if we __think__ we have more data.
        data::String
        '''
        for item in newDataPoints:
            raise
            pass
        return self.hasMore or not self.availProofs.isEmpty()
