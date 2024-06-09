import dateparser
from ics import Calendar, Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
from dataclasses import dataclass

calendar_filename = 'docs\\myfile.ics'
temp_calendar_filename = 'docs\\temp.ics'
calendar_datafile = 'Robot\\myfile.yaml'

class Calendar_skill():
    calendar = Calendar()
    # calendar.load()

    def __init__(self):
        print("")
        print("Calendar skill loaded")

    # def commands(self, command:str):
    #     return ['add event','add to calendar','new event','add a new event',
    #             'delete event','remove event','cancel event',
    #             'list events',"what's on this month","what's coming up this month",
    #             "what's on this week","what's coming up this week","what's happening",
    #             'list all events']
    
    def add_event(self, begin:str, name:str, description:str=None)->bool:
        e = Event()
        e.name = name
        # Parse the provided begin string to datetime
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

# calendar = Calendar_skill()
# parsed_date = dateparser.parse("next week at 6 30 pm", settings={'PREFER_DATES_FROM': 'future'})
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