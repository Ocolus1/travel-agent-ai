#!/usr/bin/env python
import sys
import warnings
from datetime import datetime, timedelta

from ai_travel_agent.crew import AiTravelAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to generate a personalized travel itinerary.
    
    You can customize the following inputs:
    - destination: Where you want to travel
    - days: Number of days for the trip
    - start_date: When the trip starts (YYYY-MM-DD format)
    - preferences: Your travel preferences (budget, interests, style, etc.)
    """
    
    # Default example inputs - customize these for your trip!
    inputs = {
        'destination': 'Paris, France',
        'days': '5',
        'start_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),  # 30 days from now
        'preferences': '''
        Budget: Mid-range ($100-200 per day)
        Interests: Art, history, local cuisine, photography
        Travel style: Mix of popular attractions and local experiences
        Accommodation: Boutique hotel or nice Airbnb in central location
        Pace: Relaxed, with time to enjoy cafes and explore neighborhoods
        Special requests: Vegetarian-friendly restaurants, avoid very crowded tourist traps
        '''
    }
    
    print("\n" + "="*80)
    print("🌍 AI TRAVEL AGENT - Generating Your Personalized Itinerary")
    print("="*80)
    print(f"\n📍 Destination: {inputs['destination']}")
    print(f"📅 Duration: {inputs['days']} days")
    print(f"🗓️  Start Date: {inputs['start_date']}")
    print(f"✨ Preferences: {inputs['preferences'].strip()}")
    print("\n" + "="*80 + "\n")
    
    try:
        result = AiTravelAgent().crew().kickoff(inputs=inputs)
        
        print("\n" + "="*80)
        print("✅ ITINERARY GENERATION COMPLETE!")
        print("="*80)
        print("\n📄 Check the following files:")
        print("   - travel_itinerary.md (detailed day-by-day itinerary)")
        print("   - calendar_events.txt (calendar event details)")
        print("   - [destination]_itinerary.ics (importable calendar file)")
        print("\n💡 Import the .ics file into your calendar app to add all events automatically!")
        print("\n" + "="*80 + "\n")
        
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'destination': 'Tokyo, Japan',
        'days': '7',
        'start_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
        'preferences': 'Budget: Mid-range, Interests: Culture, food, technology'
    }
    try:
        AiTravelAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiTravelAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'destination': 'Barcelona, Spain',
        'days': '4',
        'start_date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'preferences': 'Budget: Budget-friendly, Interests: Architecture, beaches, nightlife'
    }
    
    try:
        AiTravelAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
