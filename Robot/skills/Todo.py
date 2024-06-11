import datetime
from uuid import uuid4
from utils import factory
from utils.SpeechRecognition import Pyxi
from dataclasses import dataclass

# Class for todo list items
class Item:
    def __init__(self, _title=None):
        self.creation_date = datetime.date.today()
        self._title = _title if _title is not None else "empty"

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value

    def age(self):
        return datetime.date.today() - self.creation_date

# Class for todo list
class Todo_Skill():

    todos = []

    def __init__(self):
        print("Todo list created")
        self.current = -1

    def new_item(self, item: Item):
        print("adding " + item.title)
        self.todos.append(item)

    @property
    def items(self) -> list:
        return self.todos
    
    def show(self):
        print("*" * 80)
        for item in self.todos:
            print(item.title)

    def remove_item(self, title: str = None):
        if title is not None:
            for item in self.todos:
                if item.title == title:
                    self.todos.remove(item)
                    return True
            print("Item: " + title + " not found")
            return False
        else:
            print("Must state title")

    def empty_list(self):
        if len(self.todos) > 0:
            for item in self.todos[:]:
                try:
                    self.remove_item(item.title)
                except:
                    print("fail to remove". item.title)
        else:
            print("list is empty")


@dataclass
class Todo_Handler():
    name = 'todo_handler'
    todo = Todo_Skill()

    def commands(self, command:str):
        return ["add to-do", "add to do", "add item",
                "list to-do", "list to do", "lease to do",
                "romove to-do", "remove to do",
                "empty to-do", "empty to do"]

    def add_todo(self, robot:Pyxi)->bool:
        item = Item()
        try:
            print("what item to add?")
            item.title = robot.get_command()
            self.todo.new_item(item)
            print("added " + item.title)
            return True
        except:
            print("oops there was an error")
            return False

    def list_todo(self):
        if len(self.todo.todos) > 0:
            print("todo list:")
            for item in self.todo.todos:
                print(item.title)
        else:
            print("List is empty")

    def remove_todo(self, robot:Pyxi)->bool:
        print("what to remove?")
        try:
            item_title = robot.get_command()
            self.todo.remove_item(title=item_title)
            print("removed " + item_title)
            return True
        except:
            print("oops there was an error")
            return False
        
    def empty_todo(self)->bool:
        try:
            self.todo.empty_list()
            print("emptied list")
            return True
        except:
            print("oops there was an error")
            return False
    
    def handle_command(self, command:str, robot:Pyxi):
        
        if command in ["add to-do", "add to do", "add item"]:
            print("here")
            self.add_todo(robot=robot)
        if command in ["list to-do", "list to do", "lease to do"]:
            self.list_todo()
        if command in ["romove to-do", "remove to do"]:
            self.remove_todo(robot=robot)
        if command in ["empty to-do", "empty to do"]:
            self.empty_todo()

def initialize():
    factory.register('todo_handler', Todo_Handler)