import datetime

import pytz
from Robot.SpeechRecognition import Pyxi
from Robot.Todo import Todo, Item
from Robot.Weather import OpenWeatherApi
from Robot.Calendar import Calender_skill
import dateparser

robot = Pyxi()
weather_api = OpenWeatherApi()
todo = Todo()
calendar = Calender_skill()
calendar.load()
command = ""

def add_todo()->bool:
    item = Item()
    try:
        print("what item to add?")
        item.title = robot.listen()
        todo.new_item(item)
        print("added " + item.title)
        return True
    except:
        print("oops there was an error")
        return False

def list_todo():
    if len(todo.todos) > 0:
        print("todo list:")
        for item in todo.todos:
            print(item.title)
    else:
        print("List is empty")

def remove_todo()->bool:
    print("what to remove?")
    try:
        item_title = robot.listen()
        todo.remove_item(title=item_title)
        print("removed " + item_title)
        return True
    except:
        print("oops there was an error")
        return False
    
def empty_todo()->bool:
    try:
        todo.empty_list()
        print("emptied list")
        return True
    except:
        print("oops there was an error")
        return False

def add_event()->bool:
    try:
        print("Event name")
        event_name = robot.listen()
        print("name: ", event_name)
        print("When is this event?")
        event_begin = robot.listen()
        parsed_date = dateparser.parse(event_begin, settings={'PREFER_DATES_FROM': 'future'})
        if parsed_date is None:
            print("Sorry, I couldn't understand the date and time you provided.")
            return False
        localized_date = pytz.timezone('Asia/Kuala_Lumpur').localize(parsed_date)
        event_isodate = localized_date.strftime("%Y-%m-%d %H:%M:%S")
        print("on: ", event_isodate)
        print("What is the event description?")
        event_description = robot.listen()
        print("desc: ", event_description)
        print("Ok, adding event " + event_name)
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        print("event added")
        calendar.save()
        return True
    except:
        print("opps there was an error")
        return False
    
def remove_event()->bool:
    print("name of event")
    try:
        event_name = robot.listen()
        try:
            calendar.remove_event(event_name=event_name)
            print("Event removed successfully")
            calendar.save()
            return True
        except:
            print("Could not find ", event_name)
            return False
    except:
        print("oops there was an error")
        return False
    
def list_events(period):
    this_period = calendar.list_events(period=period)
    if this_period is not None:
        message = "There "
        if len(this_period) > 1:
            message += 'are '
        else:
            message += 'is '
        message += str(len(this_period)) 
        if len(this_period) > 1:
            message += ' events'
        else:
            message += ' event'
        message += " in the diary"
        print(message)
        for event in this_period:
            event_date = event.begin.datetime
            weekday = event_date.strftime("%A")
            day = str(event_date.day)
            month = event_date.strftime("%B")
            year = event_date.strftime("%Y")
            time = event_date.strftime("%I:%M %p")
            name = event.name
            description = event.description
            message = "On " + weekday + " " + day + " of " + month + " " + year + " at " + time    
            message += ", there is an event called " + name
            message += " with an event description of " + description
            print(message)

while True and command != "goodbye":

    try:
        command = robot.listen()
        command = command.lower()
        print("command was: ", command)
    except:
        print("oops there was an error")
        command = ""

    if command == "pyxi" or command == "pixie":
        print("HUH")
        command = ""

    elif command in ["add to-do", "add to do", "add item"]:
        add_todo()
        command = ""

    elif command in ["list to-do", "list to do", "lease to do"]:
        list_todo()
        command = ""
    
    elif command in ["romove to-do", "remove to do"]:
        remove_todo()
        command = ""

    elif command in ["empty to-do", "empty to do"]:
        empty_todo()
        command = ""

    elif command == "what's the weather":
        weather_data = weather_api.weather
        if weather_data:
            print(weather_data)
        else:
            print("couldn't fetch weather")
    
    elif command == "what's the temperature":
        temp_data = weather_api.temp
        print(temp_data)

    elif command in ['add event','add to calendar','new event','add a new event']:
        add_event()

    elif command in ['delete event','remove event','cancel event']:
        remove_event()

    elif command in ['list events',"what's on this month","what's coming up this month"]:
        list_events(period='this month')
    
    elif command in ["what's on this week","what's coming up this week"]:
        list_events(period='this week')

    elif command in ["what's happening", 'list all events']:
        list_events(period='all')
        