import dateparser
from ics import Calendar, Event
from pathlib import Path
import os
import yaml
import pytz
import git
import time
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
                video_player.display_text("Error")
                audio_player.play_sound("Error")
                time.sleep(2)
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
            period = "all"

        # check that there are events
        if self.calendar.events == set():
            # no events found
            print("No Events In Calendar")
            return None
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

            print(event_list)
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
            repo.git.add('--all')

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
        return [r".* calendar .*", r".* calendar", r"calendar .*", 
        r".* what's happening .*", r"what's happening .*", r".* what's happening",  "what's happening"
        r".* what is happening .*", r"what is happening .*", r".* what is happening",
        r".* event .*", r".* event", r"event .*",
        r".* events .*", r".* events", r"events .*"]
    

    def add_event(self, robot:Pyxi, video_player:Animate, audio_player:Sound)->bool:
        try:
            print("Event name")
            video_player.display_text("Event title?")
            audio_player.play_sound("Title")
            event_name = robot.get_command()
            
            video_player.display_text("Date Time?")
            audio_player.play_sound("TimeAndDate")
            event_begin = robot.get_command()
            parsed_date = dateparser.parse(event_begin, settings={'PREFER_DATES_FROM': 'future'})
            if parsed_date is None:
                video_player.play_animation("Confused")
                audio_player.play_sound("Dont-understand")
                print("Sorry, I couldn't understand the date and time you provided.")
                return False
            localized_date = pytz.timezone('Asia/Kuala_Lumpur').localize(parsed_date)
            event_isodate = localized_date.strftime("%Y-%m-%d %H:%M:%S")
            print("on: ", event_isodate)

            video_player.display_text("Description?")
            audio_player.play_sound("Description")
            print("What is the event description?")
            event_description = robot.get_command()
            audio_player.play_sound("Okay")
            video_player.play_animation("Loading")
            
            print("Ok, adding event " + event_name)
            success = self.calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
            print("event added")
            
            if success:
                video_player.play_animation("Push")
                audio_player.play_sound("Push")
                self.calendar.save()
                video_player.play_animation("Pushed")
                audio_player.play_sound("Pushed")
                time.sleep(0.2)
            else:
                video_player.display_text("Failed")
                audio_player.play_sound("Error")
                time.sleep(2)
            

            return True
        except:
            print("opps there was an error")
            video_player.display_text("Error")
            audio_player.play_sound("Error")
            time.sleep(2)
            return False
        
    def remove_event(self, robot:Pyxi, video_player:Animate, audio_player:Sound)->bool:
        
        video_player.display_text("Event title?")
        audio_player.play_sound("Title")
        try:
            event_name = robot.get_command()
            try:
                video_player.play_animation("Loading")
                success = self.calendar.remove_event(event_name=event_name)

                if success:
                    audio_player.play_sound("Rubbish")
                    video_player.play_animation("Remove_event")
                    print("Event removed successfully")
                    
                    video_player.play_animation("Push")
                    audio_player.play_sound("Push")
                    self.calendar.save()
                    video_player.play_animation("Pushed")
                    audio_player.play_sound("Pushed")
                    time.sleep(0.2)
                
                    return True
                else:
                    video_player.play_animation("Confused")
                    audio_player.play_sound("No_event")
                    time.sleep(3)
                
            except:
                video_player.play_animation("Confused")
                audio_player.play_sound("Dont-understand")
                print("Could not find ", event_name)
                time.sleep(4)
                return False
        except:
            print("oops there was an error")
            video_player.play_animation("Confused")
            audio_player.play_sound("Dont-understand")
            time.sleep(4)
            return False
        
    
    def list_events(self, period, video_player:Animate, audio_player:Sound, email:Email):
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
                event_time = event_date.strftime("%I:%M %p")
                name = event.name
                description = event.description

                content += f"- Date: {event_date}\n"
                content += f"  Name: {name}\n"
                content += f"  Time: {event_time}\n"
                content += f"  Description: {description}\n\n"

            # Send the email with structured content
            email.send_email(subject, content)
            audio_player.play_sound("Okay")
            video_player.play_animation("Email")
            time.sleep(2)
        
        else:
            audio_player.play_sound("ShowText")
            video_player.display_text("No event")
            time.sleep(3)

    def handle_command(self, command:str, robot:Pyxi, video_player:Animate, audio_player:Sound, email:Email):
        
        if "add" in command:
            self.add_event(robot=robot, video_player=video_player, audio_player=audio_player)
        elif "delete" in command or "cancel" in command or "remove" in command:
            self.remove_event(robot=robot, video_player=video_player, audio_player=audio_player)
        elif "this month" in command:
            self.list_events(period='this month', video_player=video_player, audio_player=audio_player)
        elif "this week" in command:
            self.list_events(period='this week', video_player=video_player, audio_player=audio_player)
        elif command in ['list all events', "what's happening"] or "send" in command or "list" in command or "what" in command:
            self.list_events(period='all', video_player=video_player, audio_player=audio_player, email=email)
        else:
            video_player.play_animation("Confused")
            audio_player.play_sound("Dont-understand")
            print("Unknown command")

def initialize():
    factory.register('calendar_handler', Calendar_Handler)
