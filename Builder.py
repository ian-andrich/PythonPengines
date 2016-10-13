import json
import sys


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

    def getRequestBodyAsk(self, id, ask):
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
