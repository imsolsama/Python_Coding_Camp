from .base_command import BaseCommand
import os
import shutil
from typing import List

class CopyCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        super().__init__(options, args)
        self.description = 'Copy a file or directory to another location'
        self.usage = 'Usage: cp [source] [destination]'
        self.source_path = self.args[0] if self.args else None
        self.destination_path = self.args[1] if len(self.args) > 1 else None

    def execute(self) -> None:
        if not self.source_path or not self.destination_path:
            print("Error: Source and destination paths are required.")
            return

        if '-v' in self.options:
            print(f"cp: copying '{self.source_path}' to '{self.destination_path}'")

        if self.file_exists(self.destination_path, os.path.basename(self.source_path)):
            if '-i' in self.options:
                overwrite = input(f"cp: overwrite '{self.destination_path}'? (y/n) ")
                if overwrite.lower() != 'y':
                    return

        try:
            shutil.copy2(self.source_path, self.destination_path)
        except Exception as e:
            print(f"Error: {str(e)}")

    def file_exists(self, directory: str, file_name: str) -> bool:
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)
