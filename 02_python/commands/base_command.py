# commands/base_command.py
import os
from typing import List

"""
TODO 3-1: The BaseCommand class has a show_usage method implemented, but the execute method is not 
implemented and is passed on to the child class. Think about why this difference is made.

Answer (You may write your answer in either Korean or English):

BaseCommand 클래스는 show_usage 메소드가 구현되어 있지만, execute 메소드는 구현되어 있지 않고 자식 클래스에게 넘겨지고 있다, 이는 BaseCommand 클래스가 추상 클래스이기 때문이다.
즉 'execute' 메소드는 BaseCommand 클래스를 상속받은 자식 클래스에서 구현해서 사용해야 한다.

TODO 3-2: The update_current_path method of the BaseCommand class is slightly different from other methods. 
It has a @classmethod decorator and takes a cls argument instead of self. In Python, this is called a 
class method, and think about why it was implemented as a class method instead of a normal method.

Answer (You may write your answer in either Korean or English):

BaseCommand 클래스의 update_current_path 메소드는 다른 메소드와 약간 다르다. @classmethod 데코레이터를 가지고 있고 self 대신 cls 인자를 받는다.
이는 Python에서 클래스 메소드로서, 이 메소드가 클라스 자체에 작용하며 모든 인스턴스에서 공유하는 속성인 current_path를 업데이트하기 위해서다.


"""
class BaseCommand:
    """
    Base class for all commands. Each command should inherit from this class and 
    override the execute() method.
    
    For example, the MoveCommand class overrides the execute() method to implement 
    the mv command.

    Attributes:
        current_path (str): The current path. Usefull for commands like ls, cd, etc.
    """

    current_path = os.getcwd()

    @classmethod
    def update_current_path(cls, new_path: str):
        """
        Update the current path.
        You need to understand how class methods work.

        Args:
            new_path (str): The new path. (Must be an relative path)
        """
        BaseCommand.current_path = os.path.join(BaseCommand.current_path, new_path)

    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize a new instance of BaseCommand.

        Args:
            options (List[str]): The command options (e.g. -v, -i, etc.)
            args (List[str]): The command arguments (e.g. file names, directory names, etc.)
        """
        self.options = options
        self.args = args
        self.description = 'Helpful description of the command'
        self.usage = 'Usage: command [options] [arguments]'

    def show_usage(self) -> None:
        """
        Show the command usage.
        """
        print(self.description)
        print(self.usage)

    def execute(self) -> None:
        """
        Execute the command. This method should be overridden by each subclass.
        """
        raise NotImplementedError