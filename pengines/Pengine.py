from pengines.Exceptions import CouldNotCreateException, \
    PengineNotReadyException, \
    PengineNotAvailableException
from pengines.State import State
from pengines.Builder import PengineBuilder
from pengines.Query import Query
import copy
from urllib.request import Request, urlopen
import json


class Pengine(object):
    def __init__(self, builder=None, slave_limit=-1, debug=False):
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
        self.state = State("not_created")

        # Initialize debug value, defaulting to False.
        self.debug = debug

        # Handle the builder logic.
        if builder is None:
            self.po = PengineBuilder()
        else:
            self.po = copy.deepcopy(builder)

        self.slave_limit = slave_limit
        self.ask = None
        try:
            self.pengineID = self.create()
        except PengineNotReadyException:
            self.state.current_state = "destroy"
            raise PengineNotReadyException("Pengine could not be created!!")

        # ToDo
        # Initialize state transitions
        # transitions = [("not_created", True, self.create, "idle"),
        #                ("idle", self.hasCurrentQuery, self.ask, "ask"),
        #                ("ask", self.queryHasNext, self.__next__, "ask")]

    def ask(self, query):
        '''
        Parameters:
            query :: str -> The prolog query as a string.

        Return:
            query::pengine.Query.Query() object.

        Errors:
            IOError raised if query cannot be created, or server cannot be
            contacted
        '''
        self.currentQuery = Query(self, query, True)
        try:
            answer = self.penginePost(self.po.urlserver,
                                      "application/x-prolog; charset=UTF-8",
                                      self.po.getRequestBodyAsk(self.ask))
            self.handleAnswer(answer)
        except IOError:
            self.destroy()
            raise PengineNotAvailableException()

    def doAsk(self, query, ask):
        # Check to make sure state is idle and can handle queries.
        if self.state.current_state != "idle":
            raise PengineNotReadyException("Not in a state to handle queries")
        # Begin running query.
        self.ask = ask
        if self.currentQuery is None:
            self.currentQuery = Query(self, query, True)
        else:
            raise PengineNotReadyException("Query already in place.")

        # Set pengine state to "ask", process response.
        self.state.current_state = "ask"
        answer = self.penginePost(self.po.getActualURL("send", self.po.getID()),
                                  "application/x-prolog; charset=UTF-8",
                                  self.po.getRequestBodyAsk(ask, self.getID()))
        self.handleAnswer(answer)

    def create(self):
        '''
        Configures the Pengine object.  Returns a pengine id string.'''
        assert self.state.current_state == "not_created"
        if self.debug:
            print("Starting call.")
        # Post the create request.
        url = self.po.getActualURL("create")
        contentType = "application/json"
        body = self.po.getRequestBodyCreate()
        if self.debug:
            print("Starting post request with URL {0}, content_type: {1}"\
                  ", and body: {2}".format(url, contentType, body))
        response = self.penginePost(url, contentType, body)
        if self.debug:
            print(response)
        # Parse request into JSON
        json_response = json.JSONDecoder().decode(response.body)
        # Begin setting various attributes.
        # Handle "event" key in JSON response.
        event_string = json_response["event"]
        if event_string == "destroy":
            self.state.current_state = "destroy"
        elif event_string == "create":
            self.state.current_state = "idle"
        else:
            raise CouldNotCreateException("Create request event was {} must be\
                                          create or \
                                          destroy".format(event_string))

        # Handle setting ask.
        if self.po.ask is not None:
            # If a query is present, immediately handle it.
            self.currentQuery = Query.Query(self, self.po.getAsk(), False)
            self.state.current_state = "ask"

        # Handle "answer" key
        if "answer" in json_response:
            self.handleAnswer(json_response["answer"])

        # Handle "id" key
        id_ = json_response["id"]
        if id_ is None:
            raise CouldNotCreateException("No pengine id in create message")
        return id_

    def destroy(self):
        pass

    def doNext(self, query):
        '''
        This method asks the Pengine object to request the next proof from the
        server.

        Parameters:
            query :: Query the query object to continue providing data to.
        '''
        assert self.state.current_state == "ask"
        if self.query != self.currentQuery:
            raise PengineNotReadyException("Cannot advance more than one query -\
                                           finish one before starting next.")

        url = self.po.getActualURL("send", self.getID())
        header = "application/x-prolog; charset=UTF-8",
        body = self.po.getRequestBodyNext()
        string_response_object = self.penginePost(url, header, body)
        self.handleAnswer(string_response_object)

    def doPullResponse(self):
        '''
        Returns a string off the server, if it has one to give.
            Otherwise, returns None.

        @raises PengineNotReadyExceptioni
        '''
        # Check it is in the correct state.
        if self.state.current_state != "idle" and \
                self.state.current_state != "ask":
            return None

        # Initialize Post request
        url = self.po.getActualURL("pull_response", self.getID())
        content_type = "application/x-prolog; charset=UTF-8"
        body_response = self.po.getRequestBodyPullResponse()
        response = self.penginePost(url, content_type, body_response)
        # Pass the response the handler
        self.handleAnswer(response)

    def doStop(self):
        '''Raises PengineNotReadyException'''
        assert self.state.current_state == "ask"
        respObject = self.penginePost(self.po.getActualURL("send",
                                                           self.getID()),
                                      "application/x-prolog; charset=UTF-8",
                                      self.po.getRequestBodyStop())
        self.handleAnswer(respObject)

    def dumpStateDebug(self):
        pass

    def iAmFinished(self, query):
        '''
        Query won't use pengine again.

        query:: Query() : The query we are through with
        '''
        if self.currentQuery == query:
            self.currentQuery = None

        if self.state.current_state == "ask":
            self.state.current_state = "idle"

    def penginePost(self, url, contentType, body):
        '''
        Posts body to the Pengine.
        url:: String of url
        contentType :: String -> Value of Content-Type header
        body :: String -> Body of POST request

        Return: python encoded string representing the body of the response.
                Parsing is the responsibility of the caller.
                    -- Note the format of a "create" request is Prolog encoded
                       But the format of an ask is "JSON encoded"

        Errors: IOError
        '''
        # Set up request header
        header = dict()
        header["User-Agent"] = "PythonPengine"
        header["Accept"] = "application/json"
        header["Accept-Language"] = "en-us,en;q=0.5"
        header["Content-type"] = contentType

        # Make sure body is utf-8
        if isinstance(body, bytes):
            body_utf8 = body
        elif isinstance(body, str):
            body_utf8 = body.encode("utf-8")
        else:
            raise TypeError("Don't know how to handle body parameter of type\
                            {}").format(type(body))

        try:
            # Send Post Request -- catch errors and close
            request_object = Request(url, data=body_utf8, headers=header)
            response = urlopen(request_object)
            response_string_utf8 = response.readall()
            response_string = response_string_utf8.decode("utf-8")
            # Catch bad status codes
            status = response.status
            if status < 200 or status > 299:
                err_msg = "Bad response code: {}  If query 500 was invalid?\
                    query threw Prolog exception".format(status)
                raise IOError(err_msg)
            return response_string
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
            if "event" in answer:
                event_val = json_answer["event"]
                # Handle "success" switch
                if json_answer[event_val] == "success":
                    if "data" in json_answer:
                        # json_answer["data"] should be a list
                        self.currentQuery.addNewData(json_answer["data"])
                    if "more" in json_answer:
                        if not isinstance(json_answer("more", bool)):
                            self.currentQuery.noMore()

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
            raise json.JSONDecodeError

    def getID(self):
        '''
        Getter method for the getID attribute.
        @return :: pengineID String
        @raises :: Assertion Error if current state not "ask" or "idle"
        '''
        current_state = self.state.current_state
        assert current_state == "ask" or current_state == "idle"
        return self.pengineID
