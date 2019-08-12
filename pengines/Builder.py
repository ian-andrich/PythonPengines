import json
import sys
import logging
from pengines.Exceptions import PengineNotReadyException


class PengineBuilder(object):
    def __init__(self,
                 urlserver=None,
                 application=None,
                 ask=None,
                 chunk=100,
                 destroy=True,
                 srctext=None,
                 srcurl=None,
                 format_type="json",
                 alias=None,
                 debug=False):
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
        self.debug = False

    def getRequestBodyCreate(self):
        '''
        String a representation of the request body for the create action.
        Return:
            json encoding of self.destroy, self.chunk, self.format_type,
            self.srctext, self.srcurl
        '''
        data = dict()
        if not self.destroy:
            data["destroy"] = False

        if self.chunk > 1:
            data["chunk"] = self.chunk

        data["format"] = self.format_type

        if self.srctext is not None:
            data["src_text"] = self.srctext

        if self.srcurl is not None:
            data["srcurl"] = self.srcurl

        if self.ask is not None:
            data["ask"] = self.ask
            
        if self.application is not None:
            data["application"] = self.application

        return json.JSONEncoder().encode(data)

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

    def getActualURL(self, action, id_=None):
        '''
        This class dispatches to self._getActualURL(action, id_) or
            self._getActualURL_(action) depending on the presence of id.
        returns the full url needed to accomplish the task.
        '''
        if id_ is not None:
            return self._getActualURL(action, id_)
        else:
            return self._getActualURL_(action)

    def _getActualURL_(self, action):
        '''
        action :: String -> an action like "create", "destroy", etc.
        return :: String -> The full URL needed to perform the action.
        '''
        if self.urlserver is None:
            raise PengineNotReadyException("Need to set server to get URL")
        # Verify the server url ends in a '/'
        if self.urlserver[-1] != "/":
            urlserver = self.urlserver + "/"
        else:
            urlserver = self.urlserver
        relative = "pengine/{}".format(action)
        new = urlserver + relative
        logging.info("Builder._getActualURL log.")
        logging.info("New value is :", new)
        return new

    def _getActualURL(self, action, id_):
        '''
        Parses in the relative information necessary to perform a query on
        Pengines into a full URL form.

        action::String -> Action to be performed "send", "post", etc.
        id::String -> The id of the pengine in question.
        '''
        # Verify server url is set, otherwise raise PengineNotReadyException
        print("_getActualURL is firing.")
        if self.urlserver is None:
            raise PengineNotReadyException("Cannot get actual URL without \
                                           setting the server")
        # Catch missing ending '/' if applicable.
        if self.urlserver[-1] != "/":
            urlserver = self.urlserver + "/"
        else:
            urlserver = self.urlserver

        relative = "pengine/{0}?format=json&id={1}".format(action, id_)
        url = urlserver + relative
        print("_getActualURL is returning {}".format(url))
        return url

    def getRequestBodyNext(self):
        '''
        Returns the POST body to get the next result.
        Todo: Remove this Javaism.
        '''
        return "next."

    def getReqestBodyStop(self):
        '''
        Returns 'stop
        Todo: Remove this Javaism.
        '''
        return "stop."
