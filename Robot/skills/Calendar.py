import dateparser
from ics import Calendar, Event
from pathlib import Path
import os
import yaml
import pytz
import git
from datetime import datetime
from dateutil.relativedelta import *
from utils import factory
from utils.SpeechRecognition import Pyxi
from utils.videoPlayer import Animate
from utils.audioPlayer import Sound
from utils.emailSender import Email
from dataclasses import dataclass

calendar_filename = "/home/pi/Capstone Project/docs/myfile.ics"
temp_calendar_filename = '/home/pi/Capstone Project/docs/temp.ics'
calendar_datafile = '/home/pi/Capstone Project/Robot/skills/calendar.yaml'

class Calendar_Skill():
    calendar = Calendar()
    
    def add_event(self, begin:str, name:str, description:str=None)->bool:
        e = Event()
        e.name = name
        begin_datetime = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        e.begin = begin_datetime
        e.description = description
        
        try:
            self.calendar.events.add(e)
            return True
        except:
            print("Error occured when adding event")
            return False

    def remove_event(self, event_name:str)->bool:
        # find the event
        for event in self.calendar.events:
            if event.name == event_name:
                # found it
                self.calendar.events.remove(event)
                print("removing event:",event_name)
                return True
        
        # not found
        print("Sorry Could not find that event:",event_name)
        return False

    def parse_to_dict(self):
        dict = []
        for event in self.calendar.events:
            my_event = {}
            my_event['begin'] = event.begin.datetime
            my_event['name'] = event.name
            my_event['description'] = event.description
            dict.append(my_event)
            # print('parsing file:', yaml.dump(dict, default_flow_style=False))
        return dict
    
    def save(self):
        print("saving calendar")
        # Save the Calendar ICS file
        with open(temp_calendar_filename, 'w') as temp_file:
            temp_file.writelines(self.calendar)

        with open(temp_calendar_filename, 'r') as temp_file:
            with open(calendar_filename, 'w') as my_file:
                for line in temp_file:
                    # read replace the string and write to output file
                    my_file.write(line.replace('Z', ''))

        # Delete the temporary calendar file after copying
        os.remove(temp_calendar_filename)
        print("saved calendar")

        # first check that there are some entries in the dictionary, otherwise remove the file
        if self.calendar.events == set():
            print ("No Events - Removing YAML file")
            try:
                os.remove(calendar_datafile)
            except:
                print("oops couldn't delete the YAML file")
        else:
            with open(calendar_datafile,'w') as outfile:
                
                yaml.dump(self.parse_to_dict(), outfile, default_flow_style=False)

            # Commit and push the changes to GitHub
            self.commit_to_github("/home/pi/Capstone Project/docs/myfile.ics", commit_message="Update calendar file")

    def load(self):
        ''' load the Calendar data from the YAML file '''
        filename = calendar_datafile
        my_file = Path(filename)

        # check if the file exists
        if my_file.is_file():
            stream = open(filename,'r')
            events_list = yaml.safe_load(stream)
            if events_list is not None:
                for item in events_list:
                    e = Event()
                    e.begin = item['begin']
                    e.description = item['description']
                    e.name = item['name']
                    self.calendar.events.add(e)
        else:
            # file doesnt exist
            print("file does not exist")

    def list_events(self, period)->bool:
        if period == None:
            period = "this week"

        # check that there are events
        if self.calendar.events == set():
            # no events found
            print("No Events In Calendar")
            return []
        else:
            event_list = []
            now = pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.now())
            if period == "this week":
                nextperiod = now+relativedelta(weeks=+1)
            if period == "this month":
                nextperiod = now+relativedelta(months=+1)
            if period == "all":
                nextperiod = now+relativedelta(years=+100)
            for event in self.calendar.events:
                event_date = event.begin.datetime
                if (event_date >= now) and (event_date <= nextperiod):    
                    event_list.append(event)
            return event_list
        
    def commit_to_github(self, file_path, commit_message="Update file"):
        try:
            # Change directory to the repository directory
            os.chdir("/home/pi/Capstone Project")

            # Navigate into the repository directory
            repo = git.Repo('.')
            
            # Configure user identity if not already configured
            if not repo.config_reader().has_option('user', 'email'):
                repo.git.config('user.email', 'cheryltqr@yahoo.com')
            if not repo.config_reader().has_option('user', 'name'):
                repo.git.config('user.name', 'cheryl-toh')

            # Stage the changes
            repo.git.add(file_path)

            # Commit the changes
            repo.index.commit(commit_message)

            # Push the changes to the remote repository (main branch)
            origin = repo.remote(name='origin')
            origin.push(refspec=f"HEAD:refs/heads/main")

            print("Changes committed and pushed to GitHub successfully.")
        except Exception as e:
            print(f"Error committing and pushing to GitHub: {e}")
@dataclass
class Calendar_Handler():
    name = 'calendar_handler'
    calendar = Calendar_Skill()
    calendar.load()
    
    def commands(self, command:str):
        return ['add event','add to calendar','new event','add a new event',
                'delete event','remove event','cancel event',
                'list events',"what's on this month","what's coming up this month",
                "what's on this week","what's coming up this week","what's happening",
                'list all events']
    

    def add_event(self, robot:Pyxi)->bool:
        try:
            print("Event name")
            event_name = robot.get_command()
            print("name: ", event_name)
            # Add-on: display on screen
            # Add-on: display sound
            print("When is this event?")
            event_begin = robot.get_command()
            parsed_date = dateparser.parse(event_begin, settings={'PREFER_DATES_FROM': 'future'})
            if parsed_date is None:
                # Add-on: dont understand sound
                print("Sorry, I couldn't understand the date and time you provided.")
                return False
            localized_date = pytz.timezone('Asia/Kuala_Lumpur').localize(parsed_date)
            event_isodate = localized_date.strftime("%Y-%m-%d %H:%M:%S")
            print("on: ", event_isodate)
            # Add-on: display on screen
            # Add-on: display sound
            print("What is the event description?")
            event_description = robot.get_command()
            print("desc: ", event_description)
            # Add-on: okay sound
            print("Ok, adding event " + event_name)
            self.calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
            print("event added")
            # Add-on: play deploying animation
            self.calendar.save()
            # Add-on: play done deploy animation
            return True
        except:
            print("opps there was an error")
            return False
        
    def remove_event(self, robot:Pyxi)->bool:
        # Add-on: display on screen
        # Add-on: display sound
        print("name of event")
        try:
            event_name = robot.get_command()
            try:
                self.calendar.remove_event(event_name=event_name)
                # Add-on: okay sound
                print("Event removed successfully")
                # Add-on: play deploying animation
                self.calendar.save()
                # Add-on: play done deploy animation
                return True
            except:
                # Add-on: sound and animation of cannot find event
                print("Could not find ", event_name)
                return False
        except:
            print("oops there was an error")
            return False
        
    # Add-on: send email of all events
    def list_events(self, period, email:Email):
        # Get the current date and time
        current_datetime = datetime.now()
        this_period = self.calendar.list_events(period=period)
        if this_period is not None:
            subject = f"Events in the Calendar as of {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            content = f"Events in the Calendar - {len(this_period)} events\n\n"

            for event in this_period:
                event_date = event.begin.datetime
                weekday = event_date.strftime("%A")
                day = str(event_date.day)
                month = event_date.strftime("%B")
                year = event_date.strftime("%Y")
                time = event_date.strftime("%I:%M %p")
                name = event.name
                description = event.description

                content += f"- Date: {event_date}\n"
                content += f"  Name: {name}\n"
                content += f"  Time: {time}\n"
                content += f"  Description: {description}\n\n"

            # Send the email with structured content
            email.send_email(subject, content)

        # Add another function to commit the ics file to github

    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        
        if command in ['add event','add to calendar','new event','add a new event']:
            self.add_event(robot=robot)
        if command in ['delete event','remove event','cancel event']:
            self.remove_event(robot=robot)
        if command in ['list events',"what's on this month","what's coming up this month"]:
            self.list_events(period='this month')
        if command in ["what's on this week","what's coming up this week","what's happening"]:
            self.list_events(period='this week')
        if command in ['list all events']:
            self.list_events(period='all', email=email)

def initialize():
    factory.register('calendar_handler', Calendar_Handler)

# calendar = Calendar_Skill()
# parsed_date = dateparser.parse("tomorrow at 6 30 pm", settings={'PREFER_DATES_FROM': 'future'})
# tz_kl = pytz.timezone('Asia/Kuala_Lumpur')
# parsed_date = parsed_date.replace(hour=18, minute=30)
# localized_date = tz_kl.localize(parsed_date)

# event_isodate = localized_date.strftime("%Y-%m-%d %H:%M:%S")
# print("on: ", event_isodate)
# calendar.add_event(event_isodate, "event 1", "description 1")
# calendar.save()
# events = calendar.list_events(period='all')

# for e in events:
#     print(e.name, e.begin.datetime)