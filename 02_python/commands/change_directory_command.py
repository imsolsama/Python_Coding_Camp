from .base_command import BaseCommand
import os
import shutil
from typing import List

class ChangeDirectoryCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        super().__init__(options, args)
        self.description = 'Change the current working directory'
        self.usage = 'Usage: cd [options] [directory]'
        self.destination_path = self.args[0] if self.args else None

    def execute(self) -> None:
        if not self.destination_path:
            print("Error: Destination path is required.")
            return

        if '-v' in self.options:
            print(f"cd: changing directory to '{self.destination_path}'")

        try:
            os.chdir(self.destination_path)
        except Exception as e:
            print(f"cd: cannot change directory to '{self.destination_path}': {str(e)}")
