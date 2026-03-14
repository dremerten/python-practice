"""
This code sets up a basic logger that outputs log messages to the console.

import logging
    Imports Python's built-in logging module, which is used to record
    events, debug information, warnings, and errors in applications.

import sys
    Imports the sys module so we can access system-level objects like
    sys.stdout (the standard console output stream).

logger = logging.getLogger(__name__)
    Creates or retrieves a logger instance associated with the current
    module. Using __name__ helps organize logs by module when working
    in larger applications.

stream_handler = logging.StreamHandler(sys.stdout)
    Creates a logging handler that sends log messages to sys.stdout,
    meaning the logs will be printed to the terminal/console.

logger.addHandler(stream_handler)
    Attaches the stream handler to the logger so that any messages
    logged with this logger will be written to the console.

Note:
    The logging level is not set here, so by default the logger will
    only display messages with level WARNING or higher unless a
    different level is configured.
"""

import logging  # Import the logging module to record messages (info, warnings, errors)
import sys      # Import sys to access system-level objects like stdout

logger = logging.getLogger(__name__)  
# Create or retrieve a logger for this module.
# __name__ helps identify which module/file the log messages come from.

stream_handler = logging.StreamHandler(sys.stdout)  
# Create a handler that sends log messages to the console (stdout).

logger.addHandler(stream_handler)  
# Attach the handler to the logger so logs will appear in the terminal.