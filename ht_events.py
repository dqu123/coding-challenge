#! /usr/bin/env python
"""
  David Qu
  Caltech Class of 2017
  Hangtime coding challenge
  
  This Python 2.7.6 script will parse the json and print out
  prelimary results for an initial report on the data.
  The variables created can be modified to satify additionary
  queries.
  
  Important functions defined include:

  sort_by_participants(events)
  sort_by_date(events) 
  filter_by_attended(events)
  filter_by_location(events)
  filter_by_month(events)
  map_to_participants(events)
  map_to_locations(events)

  These extend sorted, filter and map for use with Hangtime JSON events
  that are extracted to Python 2.7.6 via json.load and a .json file.
"""
import json
import datetime
import codecs
import sys

# Avoid issues with Unicode when redirecting to file
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

################################################################################
# PARSE JSON                                                                   #
################################################################################
""" 
  @summary: We parse the json from events.json into events by opening
            events.json and then closing the file.

  @var: events_file = python file object for events.json, is closed after use
  @var: events = a list of the events (which are python dictionaries)
  @var: num_events = total number of events
"""
events_file = open('events.json')
events = json.load(events_file)
events_file.close()
num_events = len(events)


################################################################################
# FUNCTIONS FOR SORTING BY PARTICIPATION                                       #
################################################################################
def sort_by_participants(events):
    """
      @function: sort_by_participants(events)
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the list of events sorted by the
          JSON attribute event.attendanceCount.yes
    """
    return sorted(events,
            key=lambda eve: eve['attendanceCount']['yes'], reverse=True)


def filter_by_attended(events): 
    """
      @function: filter_by_attended(events)
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the list of events that have 
          event.attendanceCount.yes > 0
    """
    return filter(lambda eve: eve['attendanceCount']['yes'] > 0, events)


def map_to_participants(events):
    """
      @function: map_to_participants(events) 
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the list of numbers of participants
        for each event.
    """
    return map(lambda eve: eve['attendanceCount']['yes'], events)



################################################################################
# LOCATION BASED SEARCHING                                                     #
################################################################################
def is_in_location(event, location): 
    """
      @function: is_in_location(event, location)
      @arg: event is a JSON event in Hangtime format.
      @arg: location is a string literal location.
      @return: Returns True if the location matches and false otherwise.
    """
    return event['location'] == location

def filter_by_location(location, events):
    """
      @function: filter_by_location(location, events)
      @arg: location is a string literal location.
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the filtered list with only events in the
          designated location.

      @notes: Unfortunately, the Hangtime format does not have
         consistent location formats, so it may be difficult to
         do queries such as all events in San Francisco.
    """
    return filter(lambda x: is_in_location(x, location), events)

def map_to_locations(events):
    """
      @function: map_to_location(events) 
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the list of locations for each event.
    """
    return map(lambda eve: eve['location'], events)


################################################################################
# CHRONOLOGICAL SEARCHING                                                      #
################################################################################
def sort_by_date(events):
    """
      @function: sort_by_date(events)
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the sorted list of events ordered by
          event.startTime
    """
    return sorted(events,
    key=lambda eve: eve['startTime']) # Events by Date


def in_month(event, month):
    """
      @function: in_month(event, month)
      @arg: event is a JSON event in Hangtime format.
      @month: month is an integer 1:12 representing a month.
      @return: Returns true if the event is in the specificed month 
        and false otherwise.

      @notes: This is a helper function for filter_by_month.
    """
    t = datetime.datetime.strptime(event['startTime'], 
         "%Y-%m-%dT%H:%M:%S.%fZ")
    if t.month == month:
         return True
    else: 
         return False

def filter_by_month(m, events):
    """
      @function: filter_by_month(m, events)
      @arg: m is an integer representing a specific month.
      @arg: events is a list of JSON events in Hangtime format.
      @return: Returns the filtered list of events in the specified month.
    """
    return filter(lambda x: in_month(x, m), events)
    
    
###############################################################################
# PRINTING EVENTS                                                             #
###############################################################################
def print_with_location(events):
    """
      @function: print_with_location(events) 
      @arg: events is a list of JSON events in Hangtime format.
      @return: Prints out all the events in order, numbered, with
          the number of event.attendanceCount.yes participants, and
          the event.location

      @notes: This function can be easily modified to print other attributes 
          as needed.
    """
    for i in range(len(events)):
        print 'Event %d: %s, %d participants. Location: %s'  % (i + 1, events[i]['name'], 
        events[i]['attendanceCount']['yes'], events[i]['location'])

def print_with_date(events):
    """
      @function: print_with_date(events)
      @arg: events is a list of JSON events in Hangtime format.
      @return: Prints out all the events in order, numbered, with
          the number of event.attendanceCount.yes participants
          and the event.startTime

      @notes: The start time can be manipulated 
          using the datetime python module.
    """
    for i in range(len(events)):
        print 'Event %d: %s, %d participants. Date: %s'  % (i + 1,
            events[i]['name'],
            events[i]['attendanceCount']['yes'], 
            events[i]['startTime'])

################################################################################
# STATISTICS/REPORT                                                            #
################################################################################
"""
    We print out a report and showcase the utility of the above functions.
    This file may be used as module for manipulating the Hangtime JSON events
    in Python 2.7.6.
"""
# General Statistics
events = sort_by_participants(events)
attended_events = filter_by_attended(events)
total_people = sum(map_to_participants(attended_events))

print 'Hangtime General Statistics'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'Number of people participating in Hangtime events: %d' % total_people
print 'Number of attended_events: %d' % len(attended_events)
print 'Total number of events: %d' % num_events
print 'Average number of people at all events: %d' % (total_people / num_events)
print 'Average number of people at participated events: %d' % (total_people / len(attended_events))
print ''

print 'Top ten events by participation'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print_with_location(events[:10])
print ''


# Searching by specific location
attended_locations = map_to_locations(attended_events)
test_location = 'San Francisco Public Library'
sf_events = filter_by_location(test_location, events)
 
print 'Sample Query: SELECT Events in %s' % test_location
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + len(test_location) * '~'
print_with_date(sf_events)
print ''


# Chronological Data
eve_by_date = sort_by_date(events)
attended_by_date = filter_by_attended(events)
first_date = datetime.datetime.strptime(eve_by_date[0]['startTime'], 
         "%Y-%m-%dT%H:%M:%S.%fZ")
last_date = datetime.datetime.strptime(eve_by_date[-1]['startTime'], 
         "%Y-%m-%dT%H:%M:%S.%fZ")
interval = last_date - first_date

print 'Chronological Data'
print '~~~~~~~~~~~~~~~~~~'
print 'Dates range from %s to %s' % (eve_by_date[0]['startTime'],
         eve_by_date[-1]['startTime'])
print 'Interval: %d weeks' % (interval.days / 7)
print 'Average events per week: %d' % (num_events * 7 / interval.days)
print 'Number of non-September dates: %d' %(num_events - len(filter_by_month(9, eve_by_date)))
print ''

print 'Sample Query: March Events'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
print_with_date(filter_by_month(3, eve_by_date))
print ''

# Longer Listings 
print 'Locations of attended events by popularity'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
for i in range(len(attended_locations)):
    print 'Location %d: %s' % (i + 1, attended_locations[i])
print ''

print 'Chronological listing of attended events'
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print_with_date(attended_by_date)
