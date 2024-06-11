from typing import Protocol


class Skill(Protocol):

    def commands(self, command:str):
        # return command here
        pass

    def handle_command(self, command:str):
        # hand command here
        pass