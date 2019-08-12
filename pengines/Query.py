import json
'''
This library implements the basic logic for the Pengine classes.
    - PengineBuilder: An interface for Pengine objects.
    - PengineState: For the current state of a Pengine Query, used in Pengine
    class.
    - Pengine: Base class used for performing queries -- this is the access
    point.
'''


class Query(object):
    '''
    Query objects are the objects which hold hte current query information.

    pengine :: Pengine The pengine this query is bound to.
    ask:: String describing the query.
    queryMaster :: Bool Immediately run query
    '''
    def __init__(self, pengine, ask, queryMaster=True):
        '''pengine :: Pengine, ask :: String, queryMaster :: Boolean'''
        if pengine.debug:
            print("Initializing query with query: {}".format(ask))
        self.availProofs = []
        self.hasMore = True
        self.pengine = pengine
        self.ask = ask
        if queryMaster:
            pengine.doAsk(self, ask)
        return None

    def dumpDebugState(self):
        pass

    def hasNext(self):
        '''Return True if we __think__ we have more data, else False.'''
        return self.hasMore or not self.availProofs == []

    def __iter__(self):
        return self
    
    def __next__(self):
        p = self.pengine
        if self.availProofs != []:
            data = self.availProofs.pop(0)
            if not self.hasMore and self.availProofs == []:
                p.iAmFinished(self)

            return data
        else:
            if self.hasMore:
                p.doNext(p.currentQuery)
                if self.availProofs != []:
                    return self.availProofs.pop(0)
            raise StopIteration

    def noMore(self):
        if not self.hasMore:
            return False

        self.hasMore = False
        if not self.availProofs:
            self.pengine.iAmFinished(self)

    def stop(self):
        ''' Stop the query on the slave.  We're done.
        Equivalent to typing period at the top-level in Prolog.

        Raises: PengineNotReadyException
        '''
        self.pengine.doStop()
        self.hasMore = False
        self.availProofs = []
        self.pengine.iAmFinished(self)

    def addNewData(self, data):
        '''
        Returns True if we __think__ we have more data.
        data::String
        '''
        for item in data:
            self.availProofs.append(item)
        return self.hasMore or not self.availProofs == []
