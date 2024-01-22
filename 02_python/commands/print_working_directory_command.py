from .base_command import BaseCommand
import os
from typing import List

class PrintWorkingDirectoryCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        super().__init__(options, args)
        self.description = 'Print the current working directory'
        self.usage = 'Usage: pwd'

    def execute(self) -> None:
        print(os.getcwd())