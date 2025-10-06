# 🌍 AI Travel Agent

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/Ocolus1/travel-agent-ai)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An intelligent AI-powered travel agent that generates **personalized travel itineraries** using **OpenAI GPT-4o**. This application automates the entire process of researching destinations, planning activities, and organizing your dream vacation with the ability to export your itinerary directly to your calendar.

Built with [CrewAI](https://crewai.com), this multi-agent system leverages specialized AI agents working together to deliver comprehensive travel plans tailored to your preferences.

**🔗 GitHub Repository:** [https://github.com/Ocolus1/travel-agent-ai](https://github.com/Ocolus1/travel-agent-ai)

## 📑 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [What You Get](#what-you-get)
- [Architecture](#-architecture)
- [Customization](#-customization)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [What's New](#-whats-new)
- [Contributing](#-contributing)

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Ocolus1/travel-agent-ai.git
cd travel-agent-ai

# 2. Install dependencies
pip install uv
crewai install

# 3. Set up API keys in .env file
echo "OPENAI_API_KEY=your_openai_key" > .env
echo "SERPER_API_KEY=your_serper_key" >> .env

# 4. Launch the web app
streamlit run app.py
```

## ✨ Features

### Core Features
- 🔍 **Smart Destination Research** - Automatically discovers attractions, activities, restaurants, and accommodations
- 📅 **Customizable Itineraries** - Generate day-by-day plans based on your trip duration and preferences
- 🤖 **GPT-4o Intelligence** - Powered by OpenAI's advanced language model for personalized recommendations
- 📆 **Calendar Export** - Download your itinerary as a `.ics` file to import into Google Calendar, Apple Calendar, Outlook, or any calendar app
- 💰 **Budget Awareness** - Plans activities and dining within your specified budget range
- 🎯 **Preference Matching** - Tailors recommendations to your interests, travel style, and special requirements
- 🗺️ **Realistic Planning** - Accounts for travel time, opening hours, and optimal activity sequencing

### Web Interface Features
- 🎨 **Modern Dark Theme UI** - Professional, eye-friendly dark interface with subtle accents
- 💬 **Interactive Chat** - Ask questions about your itinerary and get instant AI-powered answers
- 🧠 **Conversation Memory** - Maintains context across your entire session
- 📁 **Unique File Naming** - Each itinerary saved with destination and date (no overwrites!)
- 📥 **One-Click Downloads** - Download all trip files (itinerary, calendar, ICS) in a single ZIP
- 🔄 **Multi-Itinerary Support** - Generate multiple trips without file conflicts
- 📊 **Session Statistics** - Track messages, context items, and current destination

## 🚀 Installation

### Prerequisites

- **Python**: 3.10, 3.11, 3.12, or 3.13
- **UV Package Manager** (recommended) or pip

### Setup Instructions

1. **Clone or download this repository**

2. **Install UV** (if not already installed):
```bash
pip install uv
```

3. **Navigate to the project directory**:
```bash
cd ai_travel_agent
```

4. **Install dependencies**:
```bash
crewai install
```
Or with pip:
```bash
pip install -e .
```

5. **Set up environment variables**:

Create a `.env` file in the project root and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**How to get API keys:**
- **OpenAI API Key**: Sign up at [OpenAI Platform](https://platform.openai.com/) and generate an API key
- **Serper API Key**: Sign up at [Serper.dev](https://serper.dev/) for web search capabilities (free tier available)

## 📖 Usage

### 🌐 Web Interface (Recommended)

Launch the modern Streamlit web interface for an interactive experience:

```bash
streamlit run app.py
```

**Features:**
- 🎨 Beautiful, modern UI with gradient headers
- 💬 Chat interface to ask questions about your itinerary
- 🧠 Session memory - remembers conversation context
- 🔄 Generate new itineraries without losing history
- 🗑️ Clear session to start fresh
- 📥 Download itineraries directly from the browser
- 📊 View session statistics and context

**How to Use:**
1. Fill in the trip details in the sidebar (destination, days, start date, preferences)
2. Click "🚀 Generate Itinerary"
3. View your itinerary in the "Full Itinerary" tab
4. Ask follow-up questions in the "Chat & Ask Questions" tab
5. Export files from the "Export Files" tab

### 🖥️ Command Line Interface

Run the travel agent with default settings (Paris, 5 days):
```bash
crewai run
```

### Customize Your Trip (CLI)

Edit the inputs in `src/ai_travel_agent/main.py` to customize your travel plan:

```python
inputs = {
    'destination': 'Tokyo, Japan',        # Where you want to go
    'days': '7',                          # Trip duration
    'start_date': '2025-11-15',          # Start date (YYYY-MM-DD)
    'preferences': '''
        Budget: Mid-range ($150-250 per day)
        Interests: Japanese culture, sushi, temples, technology, anime
        Travel style: Mix of guided tours and independent exploration
        Accommodation: Traditional ryokan or modern hotel
        Pace: Moderate, with some early mornings and late nights
        Special requests: Halal food options, accessible transportation
    '''
}
```

Then run:
```bash
crewai run
```

### What You Get

After running, the AI Travel Agent generates files in the `exports/` folder:

1. **`[YYYYMMDD]_[destination]_itinerary.md`** - Detailed day-by-day itinerary with:
   - Morning, afternoon, and evening activities
   - Restaurant recommendations for each meal
   - Estimated costs and timing
   - Practical tips and alternatives
   - Example: `20251105_Paris_France_itinerary.md`

2. **`[YYYYMMDD]_[destination]_calendar_events.txt`** - Structured event data for calendar import
   - Example: `20251105_Paris_France_calendar_events.txt`

3. **`[destination]_itinerary.ics`** - Calendar file ready to import into:
   - Google Calendar
   - Apple Calendar
   - Microsoft Outlook
   - Any iCalendar-compatible app
   - Example: `Paris_France_itinerary.ics`

**Note:** Files are uniquely named with date and destination to prevent overwrites when creating multiple itineraries!

### Importing to Your Calendar

**Google Calendar:**
1. Open Google Calendar
2. Click the "+" next to "Other calendars"
3. Select "Import"
4. Choose the `.ics` file
5. Select which calendar to add events to

**Apple Calendar:**
1. Double-click the `.ics` file
2. Choose which calendar to import to
3. Click "OK"

**Outlook:**
1. Go to Calendar view
2. Select "File" > "Open & Export" > "Import/Export"
3. Choose "Import an iCalendar (.ics) file"
4. Select the file and import

## 🏗️ Architecture

The AI Travel Agent uses a multi-agent system with three specialized agents:

### Agents

1. **Destination Researcher** 🔍
   - Researches attractions, activities, restaurants, and accommodations
   - Uses web search to find current information
   - Considers seasonal events and local insights

2. **Itinerary Planner** 📋
   - Creates balanced day-by-day schedules
   - Optimizes routes and timing
   - Matches activities to preferences and budget

3. **Calendar Formatter** 📆
   - Transforms itinerary into calendar events
   - Generates `.ics` files for easy import
   - Ensures proper event formatting with times and locations

### Workflow

```
Input (destination, dates, preferences)
    ↓
Destination Researcher → Research findings
    ↓
Itinerary Planner → Day-by-day itinerary
    ↓
Calendar Formatter → Calendar events + .ics file
    ↓
Output (itinerary.md, calendar_events.txt, .ics file)
```

## 🛠️ Customization

### Modify Agents

Edit `src/ai_travel_agent/config/agents.yaml` to customize agent behavior, goals, and backstories.

### Modify Tasks

Edit `src/ai_travel_agent/config/tasks.yaml` to change what each agent focuses on.

### Add Custom Tools

Create new tools in `src/ai_travel_agent/tools/custom_tool.py` to extend functionality.

## 📋 Examples

### Weekend City Break
```python
inputs = {
    'destination': 'Barcelona, Spain',
    'days': '3',
    'start_date': '2025-11-20',
    'preferences': 'Budget: Budget-friendly, Interests: Architecture, beaches, tapas'
}
```

### Adventure Travel
```python
inputs = {
    'destination': 'Queenstown, New Zealand',
    'days': '6',
    'start_date': '2026-01-10',
    'preferences': 'Budget: Flexible, Interests: Hiking, bungee jumping, wine tasting'
}
```

### Family Vacation
```python
inputs = {
    'destination': 'Orlando, Florida',
    'days': '7',
    'start_date': '2025-12-15',
    'preferences': 'Budget: Mid-range, Interests: Theme parks, family-friendly, kid activities'
}
```

## 🐛 Troubleshooting

**API Key Errors:**
- Ensure your `.env` file contains valid API keys
- Check that the `.env` file is in the project root directory

**Import Errors:**
- Run `crewai install` or `pip install -e .` again
- Ensure you're using Python 3.10-3.13

**Calendar Import Issues:**
- Check that the `.ics` file was generated successfully
- Try opening the `.ics` file in a text editor to verify it's not empty

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Serper API Documentation](https://serper.dev/docs)

## 📈 What's New

### Version 0.2.0 (Latest)
- ✅ **Unique File Naming** - Files now include date and destination (no more overwrites!)
- ✅ **Improved Downloads** - Clear separation between single file and ZIP downloads
- ✅ **Better Organization** - All exports saved to dedicated `exports/` folder

### Previous Updates
- 🌙 **Dark Theme UI** - Professional, eye-friendly interface
- 📥 **ZIP Downloads** - All trip files in one convenient archive
- 💬 **Chat Interface** - Ask questions about your itinerary
- 🧠 **Session Memory** - Contextual conversations
- 🔄 **GPT-4o Support** - Latest OpenAI model integration

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star the repository

Visit the [GitHub repository](https://github.com/Ocolus1/travel-agent-ai) to contribute.

## 📄 License

This project is open source and available under the MIT License.

## 🌟 Star History

If you find this project useful, please consider giving it a star on [GitHub](https://github.com/Ocolus1/travel-agent-ai)! ⭐

## 📞 Support

For issues, questions, or feature requests, please visit the [GitHub Issues](https://github.com/Ocolus1/travel-agent-ai/issues) page.

---

**Happy Travels! 🌏✈️**

Made with ❤️ using [CrewAI](https://crewai.com) and [Streamlit](https://streamlit.io)
