import json
from urllib.parse import urlparse
import sys
from Exceptions import PengineNotReadyException


class PengineBuilder(object):
    def __init__(self,
                 urlserver=None,
                 application="sandbox",
                 ask=None,
                 chunk=1,
                 destroy=True,
                 srctext=None,
                 srcurl=None,
                 format_type="json",
                 alias=None):
        self.alias = alias
        self.application = application
        self.ask = ask
        self.chunk = chunk
        self.destroy = destroy
        self.format_type = format_type
        self.urlserver = urlserver
        self.srctext = srctext
        self.srcurl = srcurl
        self.request_body = self.getRequestBodyCreate()

    def getRequestBodyCreate(self):
        '''Returns the string to be passed to the Pengine, according to the
        values passed to the builder '''
        data = dict()
        if not self.destroy:
            data["destroy"] = False

        if self.chunk > 1:
            data["chunk"] = self.chunk

        if self.srctext is not None:
            data["srctext"] = self.srctext

        if self.srcurl is not None:
            data["srcurl"] = self.srcurl

        if self.ask is not None:
            data["ask"] = self.ask

        return json.dumps(data)

    def getRequestBodyAsk(self, ask, id=None):
        '''
        ask::String The prolog query.
        id::String The id of the pengine id that is transmitting.
            Currently not used.
        '''
        return "ask({},[]).".format(ask)

    def dumpDebugState(self):
        '''Dumps debug information to stderr'''
        # Initialize the destroy string printout to stderr
        if self.destroy:
            destroy_string = "destroy at end of query"
        else:
            destroy_string = "retain at end of query"

        serialized = ["--- PengineBuilder ----",
                      "alias {}".format(self.alias),
                      "application {}".format(self.application),
                      "ask {}".format(self.ask),
                      "chunk size {}".format(self.chunk),
                      destroy_string,
                      "server {}".format(self.urlserver),
                      "srctext {}".format(self.srctext),
                      "srcurl {}".format(self.srcurl),
                      "--- end PengineBuilder ---"]
        for line in serialized:
            sys.stderr.write(line)

    def getActualURL(self, action, id):
        '''
        Parses in the relative information necessary to perform a query on
        Pengines into a full URL form.

        action::String -> Action to be performed "send", "post", etc.
        id::String -> The id of the pengine in question.
        '''
        # Verify server url is set, otherwise raise PengineNotReadyException
        if self.urlserver is None:
            raise PengineNotReadyException("Cannot get actual URL without \
                                           setting the server")
        relative = "/pengine/{1}?format=json&id={2}".format(action, self.id)
        uribase = urlparse(self.urlserver)
        uribase.path = relative
        return uribase.geturl()

    def getRequestBodyNext(self):
        '''
        Returns the POST body to get the next result.
        '''
        return "next."
