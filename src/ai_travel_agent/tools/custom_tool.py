from crewai.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import os
import re


class CalendarGeneratorInput(BaseModel):
    """Input schema for CalendarGeneratorTool."""
    destination: str = Field(..., description="The travel destination")
    events_data: str = Field(..., description="Formatted calendar events data with title, date, time, location, and description for each event")
    start_date: str = Field(..., description="Trip start date in YYYY-MM-DD format")


class CalendarGeneratorTool(BaseTool):
    name: str = "Travel Calendar Generator"
    description: str = (
        "Generates a downloadable .ics calendar file from travel itinerary events. "
        "This tool takes formatted event data and creates a calendar file that can be "
        "imported into Google Calendar, Apple Calendar, Outlook, and other calendar applications."
    )
    args_schema: Type[BaseModel] = CalendarGeneratorInput

    def _parse_events(self, events_data: str, start_date_str: str) -> List[Dict]:
        """Parse the formatted events data into structured event dictionaries."""
        events = []
        current_event = {}
        
        # Split by lines and process
        lines = events_data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_event:
                    events.append(current_event)
                    current_event = {}
                continue
            
            # Parse event fields
            if line.startswith('- Title:') or line.startswith('Title:'):
                if current_event:
                    events.append(current_event)
                current_event = {'title': line.split(':', 1)[1].strip()}
            elif line.startswith('- Date:') or line.startswith('Date:'):
                current_event['date'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Start Time:') or line.startswith('Start Time:'):
                current_event['start_time'] = line.split(':', 1)[1].strip()
            elif line.startswith('- End Time:') or line.startswith('End Time:'):
                current_event['end_time'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Location:') or line.startswith('Location:'):
                current_event['location'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Description:') or line.startswith('Description:'):
                current_event['description'] = line.split(':', 1)[1].strip()
        
        # Add the last event if exists
        if current_event:
            events.append(current_event)
        
        return events

    def _create_datetime(self, date_str: str, time_str: str) -> datetime:
        """Create a datetime object from date and time strings."""
        try:
            # Try to parse the date
            date_formats = ['%Y-%m-%d', '%B %d, %Y', '%b %d, %Y', '%d/%m/%Y', '%m/%d/%Y']
            date_obj = None
            
            for fmt in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if not date_obj:
                # Try to extract date from string
                date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_str)
                if date_match:
                    date_obj = datetime(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
            
            # Parse time
            time_formats = ['%I:%M %p', '%H:%M', '%I %p', '%H']
            time_obj = None
            
            for fmt in time_formats:
                try:
                    time_obj = datetime.strptime(time_str.strip(), fmt)
                    break
                except ValueError:
                    continue
            
            if date_obj and time_obj:
                return datetime.combine(date_obj.date(), time_obj.time())
            elif date_obj:
                return date_obj
            
            # Fallback to current time
            return datetime.now()
        except Exception:
            return datetime.now()

    def _run(self, destination: str, events_data: str, start_date: str) -> str:
        """Generate an .ics calendar file from the events data."""
        try:
            # Create calendar
            cal = Calendar()
            cal.add('prodid', '-//AI Travel Agent//Travel Itinerary//EN')
            cal.add('version', '2.0')
            cal.add('calscale', 'GREGORIAN')
            cal.add('method', 'PUBLISH')
            cal.add('x-wr-calname', f'{destination} Travel Itinerary')
            cal.add('x-wr-timezone', 'UTC')
            
            # Parse events
            events = self._parse_events(events_data, start_date)
            
            if not events:
                return "Error: No events could be parsed from the provided data."
            
            # Add events to calendar
            for event_data in events:
                event = Event()
                
                # Set event properties
                event.add('summary', event_data.get('title', 'Travel Activity'))
                
                # Create datetime objects
                start_dt = self._create_datetime(
                    event_data.get('date', start_date),
                    event_data.get('start_time', '09:00 AM')
                )
                
                end_dt = self._create_datetime(
                    event_data.get('date', start_date),
                    event_data.get('end_time', '10:00 AM')
                )
                
                # Ensure end is after start
                if end_dt <= start_dt:
                    end_dt = start_dt + timedelta(hours=1)
                
                event.add('dtstart', start_dt)
                event.add('dtend', end_dt)
                event.add('dtstamp', datetime.now(pytz.utc))
                
                if event_data.get('location'):
                    event.add('location', event_data['location'])
                
                if event_data.get('description'):
                    event.add('description', event_data['description'])
                
                # Add unique ID
                event.add('uid', f"{start_dt.strftime('%Y%m%d%H%M%S')}-{event_data.get('title', 'event').replace(' ', '-')}@ai-travel-agent")
                
                cal.add_component(event)
            
            # Save to file in exports directory
            os.makedirs('exports', exist_ok=True)
            filename = f"{destination.replace(' ', '_')}_itinerary.ics"
            filepath = os.path.join(os.getcwd(), 'exports', filename)
            
            with open(filepath, 'wb') as f:
                f.write(cal.to_ical())
            
            return f"Calendar file successfully created: {filename}\nTotal events added: {len(events)}\nYou can import this file into Google Calendar, Apple Calendar, Outlook, or any other calendar application."
        
        except Exception as e:
            return f"Error generating calendar file: {str(e)}"
