from State import State, StateError
from Builder import PengineBuilder
from Query import Query
import copy
import requests
import json


class Pengine(object):
    def __init__(self, builder=None, slave_limit=-1):
        '''
        This Pengine object is used to run one or more queries of the
        Prolog Knowledge base set in the PengineBuilder.  builder::None ||
        PengineBuilder  Uses a new PengineBuilder with default settings,
        otherwise use the supplied PengineBuilder initialized with the
        desired settings.  A deepcopy is performed to preserve state.
        slave_limit::Int Sets limits on the number of slaves that this
        pengine can have.
        '''
        self.availOutput = None
        self.currentQuery = None
        self.pengineID = None
        if builder is None:
            self.po = PengineBuilder()
        else:
            self.po = copy.deepcopy(builder)
        self.slave_limit = slave_limit
        self.ask = None

        # Initialize state transitions
        self.state = State()
        transitions = [("not_created", True, self.create, "idle"),
                       ("idle", self.hasCurrentQuery, self.ask, "ask"),
                       ("ask", self.queryHasNext, self.__next__, "ask")]

    def ask(self):
        self.currentQuery = Query(self, query, True)
        try:
            answer = self.penginePost(self.po.urlserver,
                                      "application/x-prolog; charset=UTF-8"
                                      ,po.getRequestBodyAsk(self.ask))
            self.handleAnswer(answer)
        except IOError as e:
            self.destroy()
            raise PengineNotAvailableException()
        except SyntaxError as e:
            pass

    def doAsk(self, query, ask):
        # Check to make sure state is idle and can handle queries.
        if self.state.current_state != "idle":
            raise PengineNotReadyException("Not in a state to handle queries")
        # Begin running query.
        self.ask = ask
        if self.currentQuery is None:
            self.currentQuery = Query(pengine, query, True)
        else:
            raise PengineNotReadyException("Query already in place.")

        # Set pengine state to "ask", process response.
        self.state.current_state = "ask"
        answer = self.penginePost(
        self.po.getActualURL("send", self.po.getID()),
        "application/x-prolog; charset=UTF-8",
        po.getRequestBodyAsk(ask, self.getID()))
        self.handleAnswer(answer)

    def create(self):
        pass

    def destroy(self):
        pass

    def doNext(self, query):
        pass

    def doPullResponse(self):
        pass

    def doStop(self):
        '''
        Raises PengineNotReadyException
        '''
        try:
            respObject = penginePost(po.getActualUrl())
        except:
            pass

    def dumpStateDebug(self):
        pass

    def iAmFinished(self, query):
        if self.currentQuery == query:
            this.currentQuery = None

        if self.state.current_state == "ask":
            self.state.current_state = "idle"

    def penginePost(self, url, contentType, body):
        '''
        Posts body to the Pengine.
        url:: String of url
        contentType :: String -> Value of Content-Type header
        body :: String -> Body of POST request

        Errors: IOError
        '''
        try:
            # Set up request header
            header = dict()
            header["User-Agent"] = "JavaPengine"
            header["Accept"] = "application/json"
            header["Accept-Language"] = "en-us,en;q=0.5"
            header["Content-type", contentType]

            # Send Post Request
            session = requests.session()
            req = requests.Request('POST', url=self.po.urlserver, headers=header)
            prepped = req.prepare()
            prepped.body(body)
            response = s.send(prepped)
            # Catch bad status codes
            if response.status_code < 200 or response.status_code > 299:
                raise IOError("Bad response code.  If 500 query was invalid?\
                            query threw Prolog exception?")

            # Read in response.
            return response.json()
        except IOError as e:
            self.destroy()
            raise e

    def handleAnswer(self, answer):
        '''
        answer::json The JSON response from the initial post to the server

        Exceptions:
            json.JSONDecodeError
            SyntaxError
        '''
        try:
            # Turn the answer into the python equivalent of the JSON input
            json_answer = json.JSONDecoder.decode(answer)
            # ToDo
            raise
            if "event" in answer:
                event_val = json_answer["event"]
                # Handle "success" switch
                if json_answer[event_val] == "success":
                    if "data" in json_answer:
                        currentQuery.addNewData(answer.event_val)
                    if "more" in json_answer:
                        if not isinstance(json_answer("more", bool)):
                            currentQuery.noMore()

                # Handle "destroy" switch
                elif json_answer[event_val] == "destroy":
                    if "data" in json_answer:
                        self.handleAnswer(json_answer["data"])
                    if self.currentQuery is not None:
                        self.currentQuery.noMore()
                        self.state = "destroyed"

                # Handle "failure" switch
                elif json_answer[event_val] == "failure":
                    self.currentQuery.noMore()

                # Handle "stop" switch
                elif json_answer[event_val] == "stop":
                    self.currentQuery.noMore()

                # Handle "error" switch
                elif json_answer[event_val] == "error":
                    raise SyntaxError("Error - probably invalid Prolog query?")

                # Handle "died" switch
                elif json_answer[event_val] == "died":
                    self.state = "destroyed"

                # Default to raising a syntax error.
                else:
                    raise SyntaxError("Bad event in answer")
        except PengineNotReadyException:
            raise SyntaxError


        except json.JSONDecodeError:
            raise

    def getID(self):
        current_state = self.state.current_state
        assert current_state = "ask" or current_state = "idle"
        return self.pengineID
