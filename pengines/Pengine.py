from pengines.Exceptions import CouldNotCreateException, \
    PengineNotReadyException, \
    PengineNotAvailableException
from pengines.State import State
from pengines.Builder import PengineBuilder
from pengines.Query import Query
import copy
from urllib.request import Request, urlopen
import json
import urllib


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

        # self.create() gets pengineID
        self.slave_limit = slave_limit
        try:
            self.pengineID = self.create()
        except PengineNotReadyException:
            self.state.current_state = "destroy"
            raise PengineNotReadyException("Pengine could not be created!!")

        if self.debug:
            print("Initialization complete.")
        return None

    def ask(self, query):
        '''
        Parameters:
            query::str -> The prolog query as a string.

        Return:
            query::pengine.Query.Query() object.

        Errors:
            IOError raised if query cannot be created, or server cannot be
            contacted
        '''
        if self.debug:
            print("Starting the call to ask.")
            print("Current state is {}".format(self.state.current_state))
        self.currentQuery = Query(self, query, False)
        print("Call to ask is complete")
        return self.currentQuery

    def doAsk(self, query):
        # Check to make sure state is idle and can handle queries.
        if self.state.current_state != "idle":
            raise PengineNotReadyException("Not in a state to handle queries")
        # Begin running query.
        if self.currentQuery is None:
            self.currentQuery = query

        # Set pengine state to "ask", process response.
        self.state.current_state = "ask"
        answer = self.penginePost(self.po.getActualURL("send", self.pengineID),
                                  "application/x-prolog; charset=UTF-8",
                                  self.po.getRequestBodyAsk(query.ask,
                                                            self.getID()))
        self.handleAnswer(answer)

    def create(self):
        '''
        Configures the Pengine object.  Returns a pengine id string.

        Modifies state -- to "idle" if created successfully.  Else "destroy"
        '''
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

        # Begin setting various attributes.

        # Set the event state to destroy if request failed, or idle and waiting
        # for a query.
        event_string = response["event"]
        if event_string == "destroy":
            self.state.current_state = "destroy"
        elif event_string == "create":
            self.state.current_state = "idle"
        else:
            err_msg = "Create request event was {}, but must be create or"\
                "destroy".format(event_string)
            raise CouldNotCreateException(err_msg)

        # Handle setting ask.
        if self.po.ask is not None:
            # If a query is present, immediately handle it.
            self.currentQuery = Query(self, self.po.ask, False)
            self.state.current_state = "ask"

        # Handle "answer" key
        if "answer" in response:
            self.handleAnswer(response["answer"])

        # Handle "id" key
        id_ = response["id"]
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
        if self.debug:
            print("pengines.Pengine().doNext is firing with query ", query)
        # ToDo assert self.state.current_state == "ask"
        if query != self.currentQuery:
            raise PengineNotReadyException("Cannot advance more than one query -\
                                           finish one before starting next.")

        url = self.po.getActualURL("send", self.getID())
        contentType = "application/x-prolog; charset=UTF-8"
        body = self.po.getRequestBodyNext()
        if self.debug:
            print("url: {0}; body: {2}; contentType: {1}".format(url,
                                                            contentType,
                                                            body))
        string_response_object = self.penginePost(url, contentType, body)
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
        raise TypeError("doPullNot implemented exception")

    def doStop(self):
        '''Raises PengineNotReadyException'''
        assert self.state.current_state == "ask"
        respObject = self.penginePost(self.po.getActualURL("send",
                                                           self.getID()),
                                      "application/x-prolog; charset=UTF-8",
                                      self.po.getRequestBodyStop())
        self.handleAnswer(respObject)
        pass

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

        Return: response_dict::dict -> A dict representing the JSON encoded response.
        Errors: IOError -> If there is a problem posting, an IOError is raised.
        '''
        if self.debug:
            print("Starting Post request.")
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

        if self.debug:
            print("URL is: ", url)
            print("Data (body) : ", body_utf8)
            print("Headers: ", header)
        try:
            # Send Post Request -- catch errors and close
            request_object = Request(url, data=body_utf8, headers=header)
            response = urlopen(request_object)
            response_string_utf8 = response.read()
            response_string = response_string_utf8.decode("utf-8")
            if self.debug:
                print("response_string is :", response_string)
            response_dict = json.JSONDecoder().decode(response_string)
            # Catch bad status codes
            status = response.status
            if status < 200 or status > 299:
                err_msg = "Bad response code: {}  If query 500 was invalid?\
                    query threw Prolog exception".format(status)
                raise IOError(err_msg)
            return response_dict
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
        if self.debug:
            print("pengines.Pengine().handleAnswer({})".format(answer))
        try:
            if "event" in answer:
                event_val = answer["event"]
                if self.debug:
                    print("pengine.Pengine().handleAnswer reports {}".format(event_val))
                # Handle "success" switch
                if event_val == "success":
                    if "data" in answer:
                        # answer["data"] should be a list
                        self.currentQuery.addNewData(answer["data"])
                    if "more" in answer:
                        self.currentQuery.hasMore = answer["more"]

                # Handle "destroy" switch
                elif event_val == "destroy":
                    if "data" in answer:
                        self.handleAnswer(answer["data"])
                    if self.currentQuery is not None:
                        self.currentQuery.noMore()
                        self.state.current_state = "destroyed"

                # Handle "failure" switch
                elif event_val == "failure":
                    self.currentQuery.noMore()

                # Handle "stop" switch
                elif event_val == "stop":
                    self.currentQuery.noMore()

                # Handle "error" switch
                elif event_val == "error":
                    raise SyntaxError("Error - probably invalid Prolog query?")

                # Handle "died" switch
                elif event_val == "died":
                    self.state.current_state = "destroyed"

                # Default to raising a syntax error.
                else:
                    raise SyntaxError("Bad event in answer")
        except PengineNotReadyException:
            raise SyntaxError

    def getID(self):
        '''
        Getter method for the getID attribute.
        @return :: pengineID String
        @raises :: Assertion Error if current state not "ask" or "idle"
        '''
        current_state = self.state.current_state
        assert current_state == "ask" or current_state == "idle"
        return self.pengineID
