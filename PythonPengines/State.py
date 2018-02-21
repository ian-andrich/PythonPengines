import collections

class State(object):
    ''' State Machine Class.
        Initializes to start_state, and optionally an iterator of states, or
        an iterator of (start_state, end_state) transitions.

        Errors: ValueError is raised if a transition is not allowed.
    '''
    def __init__(self, start_state, transitions=None):
        self.current_state = start_state  # Initialize a starting state.
        self.transitions = collections.defaultdict(list)

        # Initialize transitions if passed.
        if transitions is not None:
            for start, check, action, end in transitions:
                self.add_transition(start, check, action, end)

    @property
    def states(self):
        return self.transitions.keys()

    def add_transition(self, start, check, action, end):
        '''Adds an allowed state transition.
        start::String
        check:: pointer to a method with no parameters which returns a bool
            or a property of an object.
        action:: pointer to a method with no parameters
        end::String
        '''
        self.transitions[start].append((check, action, end))

    def run(self):
        current_state = self.current_state
        possible_transitions = self.transitions[current_state]
        # Perform checks until a valid transition is found.
        # Perform the action, then change the state.
        for check, action, end in possible_transitions:
            if hasattr(check, "__call__"):
                should_continue = check.__call__()
            else:
                should_continue = check
            if should_continue:
                action.__call__()
                self.current_state = end
        # Raise StateTransitionError if no valid checks.
        else:
            raise


class StateError(Exception):
    pass
