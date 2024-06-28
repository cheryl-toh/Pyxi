import datetime
from uuid import uuid4
from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.emailSender import Email
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from dataclasses import dataclass
import time

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

    # Add-on: number of to-do


@dataclass
class Todo_Handler():
    name = 'todo_handler'
    todo = Todo_Skill()

    def commands(self, command:str):
        return [r".* to do .*", r".* to-do .*",  r".* to-do",  r".* to do"]

    def add_todo(self, robot:Pyxi, video_player:Animate, audio_player:Sound)->bool:
        item = Item()
        try:
            video_player.display_text("Item to add?")
            audio_player.play_sound("Title")
            item.title = robot.get_command()
            self.todo.new_item(item)
            audio_player.play_sound("Okay")
            print("added " + item.title)
            return True
        except:
            print("oops there was an error")
            return False

    def list_todo(self, video_player:Animate, audio_player:Sound, email:Email):
        if len(self.todo.todos) > 0:
            todo = "Your To-do list:\n"
            for item in self.todo.todos:
                todo += f"- {item.title}\n"
            email.send_email("To-do List", todo)
            audio_player.play_sound("Okay")
            video_player.play_animation("Email")
            time.sleep(2)
            
        else:
            video_player.display_text("List is empty")
            audio_player.play_sound("Showtext")
            print("List is empty")
            time.sleep(3)

    def remove_todo(self, robot:Pyxi, video_player:Animate, audio_player:Sound)->bool:
        video_player.display_text("Item title?")
        audio_player.play_sound("Title")
        try:
            item_title = robot.get_command()
            success = self.todo.remove_item(title=item_title)

            if success:
                audio_player.play_sound("Okay")
                time.sleep(0.1)
                audio_player.play_sound("Remove_event")
                video_player.play_animation("Rubbish")
                time.sleep(1)
            else:
                audio_player.play_sound("No_event")
                video_player.play_animation("Confused")
                time.sleep(3)
            
            return True
        except:
            audio_player.play_sound("Dont-understand")
            video_player.play_animation("Confused")
            time.sleep(3)
            return False
        
    def empty_todo(self, video_player:Animate, audio_player:Sound)->bool:
        try:
            self.todo.empty_list()
            audio_player.play_sound("Okay")
            time.sleep(0.1)
            audio_player.play_sound("Remove_event")
            video_player.play_animation("Rubbish")
            print("emptied list")
            time.sleep(1)
            return True
        except:
            print("oops there was an error")
            return False
    
    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        
        if "add" in command:
            print("here")
            self.add_todo(robot=robot, video_player=video_player, audio_player=audio_player)
        if "send" in command:
            self.list_todo(video_player=video_player, audio_player=audio_player, email=email)
        if "remove" in command:
            self.remove_todo(robot=robot, video_player=video_player, audio_player=audio_player)
        if "empty" in command:
            self.empty_todo(video_player=video_player, audio_player=audio_player)

def initialize():
    factory.register('todo_handler', Todo_Handler)