# Initialize logging -- try except is to import from main application, otehrwise
# use sane defaults.

# import logging
# try:  # Python 2.7+
#     from logging import NullHandler
# except ImportError:
#     class NullHandler(logging.Handler):
#         def emit(self, record):
#             pass
#
# logging.getLogger(__name__).addHandler(NullHandler())
