import datetime
from uuid import uuid4

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
class Todo():

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