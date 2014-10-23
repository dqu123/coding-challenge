#! /usr/bin/env python
"""
  David Qu
  Hangtime coding challenge
  
  This Python 2.7.6 script will parse the json and print out
  prelimary results for an initial report on the data.
"""
import json


""" 
  @summary: We parse the json from events.json into events by opening
            events.json and then closing the file.

  @var: events = a list of the events (which are python dictionaries).
"""
events_file = open('events.json')
events = json.load(events_file)
events_file.close()
num_events = len(events)


"""
  @summary: First let's sort events based on the number of participants

  @var: events is changed to the sorted version by descending 
        ['attenanceCount']['yes']
"""
events = sorted(events, 
    key=lambda event: event['attendanceCount']['yes'], reverse=True)

print 'Top ten events by participation'
for i in range(10):
    print 'Event %d: %s, %d participants. Location: %s'  % (i + 1, events[i]['name'], 
        events[i]['attendanceCount']['yes'], events[i]['location'])
