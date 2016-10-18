''' This module handles all of the exceptions specific to the Python
Pengines logic.'''

# CouldNotCreateException
class CouldNotCreateException(Exception):
    def __init__(self, message):
        self.message = message

# PengineNotReadyException
class PengineNotReadyException(Exception):
    def __init__(self, message):
        self.message = message

# PengineNotAvailableException
class PengineNotAvailableException(Exception):
    def __init__(self, message):
        self.message = message
