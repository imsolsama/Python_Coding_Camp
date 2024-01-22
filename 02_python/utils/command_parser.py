# utils/command_parser.py
import logging
from typing import Dict, Any

# TODO 10-1: Add a logger object.
logger = logging.getLogger(__name__)

class CommandParser:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def parse_command(self, input_command: str) -> Dict[str, Any]:
        tokens = input_command.split()
        command_name = tokens[0]
        options = [token for token in tokens[1:] if token.startswith('-')]
        positional_args = [token for token in tokens[1:] if not token.startswith('-')]

        # Log command name, options, and arguments
        logger.info(f"Command name: {command_name}")
        logger.info(f"Options: {options}")
        logger.info(f"Positional args: {positional_args}")

        if self.verbose:
            print(f"Command name: {command_name}")
            print(f"Options: {options}")
            print(f"Positional arguments: {positional_args}")

        return {
            'command_name': command_name,
            'options': options,
            'args': positional_args
        }
