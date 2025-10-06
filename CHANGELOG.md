# Changelog

All notable changes to the AI Travel Agent project will be documented in this file.

## [0.2.0] - 2025-10-06

### Fixed

#### 📁 **Unique File Naming for Multiple Itineraries**
- **Issue**: Files in exports folder had generic names that got overwritten with each new query
  - Only `Lagos_Nigeria_itinerary.ics` included destination info
  - `travel_itinerary.md` and `calendar_events.txt` were generic and conflicted
  - No way to differentiate files from different queries
- **Fix**: Implemented dynamic file renaming with destination and start date
- **Changes**:
  - Added `rename_export_files()` function to rename files after crew generation
  - Files now named with pattern: `[YYYYMMDD]_[destination]_[type].[ext]`
  - Example: `20251105_Lagos_Nigeria_itinerary.md`
  - Added `get_export_filenames()` helper to get expected filenames
  - Updated `create_download_zip()` to use new filename pattern
  - ZIP filename now includes date: `20251105_Lagos_Nigeria_trip_files.zip`

**New File Naming Convention:**
- **Itinerary**: `[YYYYMMDD]_[destination]_itinerary.md`
- **Calendar Events**: `[YYYYMMDD]_[destination]_calendar_events.txt`
- **ICS File**: `[destination]_itinerary.ics` (already had destination)

**Benefits:**
- Each query generates uniquely named files
- No file overwrites when creating multiple itineraries
- Easy to identify which files belong to which trip
- Date prefix allows chronological sorting

#### 📥 **Fixed Full Itinerary Tab Download Button**
- **Issue**: Download button in "Full Itinerary" tab downloaded entire ZIP file instead of just the itinerary
- **User Intent**: Download button should provide only the itinerary text file, not all trip files
- **Fix**: Changed download to provide only the Markdown itinerary file
- **Changes**:
  - Updated Full Itinerary tab download to use `get_export_filenames()` 
  - Downloads single `.md` file instead of ZIP
  - Button label changed to "📥 Download Itinerary (Text)"
  - MIME type changed to `text/markdown`

**Benefits:**
- Clear separation: Full Itinerary tab = just itinerary file
- Export Files tab = all files in ZIP
- Users can quickly download just the text they're viewing

#### 📝 **Improved Download Button Descriptions**
- **Issue**: Unclear what was included in ZIP downloads
- **Fix**: Enhanced all download button labels and help text
- **Changes**:
  - Sidebar button: "📥 Download All Trip Files (ZIP)" with detailed help text
  - Full Itinerary tab: "📥 Download Itinerary (Text)" - single file download
  - Export tab: "📥 Download All Trip Files (ZIP)" with detailed description
  - Added help tooltips explaining exact contents of each download
  - Updated Export tab description to mention unique file naming

**New Descriptions Include:**
- Exact file types (Markdown, TXT, ICS)
- Purpose of each file
- Note about unique naming with destination and dates

**Files Modified:**
- `app.py` - Added `rename_export_files()`, `get_export_filenames()`, updated download buttons, improved descriptions

**Result:** Users can now generate multiple itineraries without file conflicts, and download buttons clearly indicate what's being downloaded!

---

## [0.1.9] - 2025-10-06

### Changed

#### 📥 **Improved Download Experience**
- **Feature**: Unified download system for both itinerary and calendar files
- **Changes**:
  - Removed format selector dropdown (Markdown, Plain Text, HTML) from sidebar
  - Removed format selector from "Full Itinerary" tab
  - Replaced file location display with direct download button in "Export Files" tab
  - All downloads now provide a single ZIP file containing both itinerary and calendar
  
**Download Contents:**
- **Itinerary** (Markdown format) - `[destination]_itinerary.md`
- **Calendar Events** (Text format) - `calendar_events.txt`
- **Calendar File** (ICS format) - `[destination]_itinerary.ics`

**Benefits:**
- One-click download of all trip files
- No need to choose formats or download separately
- Cleaner, simpler UI
- All files organized in a single ZIP archive

#### 📁 **Organized File Structure**
- **Feature**: Created dedicated `exports` folder for generated files
- **Changes**:
  - All generated files now saved to `exports/` directory
  - Itinerary: `exports/travel_itinerary.md`
  - Calendar events: `exports/calendar_events.txt`
  - Calendar file: `exports/[destination]_itinerary.ics`
  
**Benefits:**
- Cleaner project root directory
- Better file organization
- Easy to find all generated files in one place
- Easier to add to .gitignore if needed

**Files Modified:**
- `app.py` - Removed format selectors, added ZIP download functionality, updated file paths
- `src/ai_travel_agent/crew.py` - Updated output paths to use `exports/` folder
- `src/ai_travel_agent/tools/custom_tool.py` - Updated calendar file path to `exports/` folder

**Result:** Simplified download experience with all files in one organized location!

---

## [0.1.8] - 2025-10-03

### Changed

#### 🔄 **Updated to GPT-4o (GPT-3.5-turbo Discontinued)**
- **Discovery**: GPT-3.5-turbo is no longer supported by OpenAI
- **Action**: Updated default model from GPT-4 to GPT-4o
- **Research Finding**: 
  - GPT-3.5-turbo has been discontinued
  - GPT-4 is being deprecated April 30, 2025
  - GPT-4o is now the recommended default model
  - o4-mini is the new cost-effective option
  
**Changes:**
- Updated `.env` MODEL from `gpt-4` to `gpt-4o`
- Updated model options documentation
- Added deprecation warnings for old models

**Benefits:**
- Using current, supported model
- Better performance with multimodal capabilities
- Future-proof configuration

**Files Modified:**
- `.env` - Updated MODEL and documentation

---

## [0.1.7] - 2025-10-03

### Added

#### 📥 **Enhanced Download Functionality**
- **Feature**: Multi-format download options for itinerary
- **Formats Available**:
  - **Markdown (.md)** - Original format with markdown syntax
  - **Plain Text (.txt)** - Clean text without formatting
  - **HTML (.html)** - Styled HTML document ready to view in browser
  
**Improvements:**
- Added format selector dropdown in sidebar
- Added format selector in "Full Itinerary" tab
- Download button now actually downloads files (was just showing info message)
- HTML export includes beautiful styling and formatting
- Text export removes all markdown syntax for clean reading
- Dynamic filename based on destination
- Proper MIME types for each format

**Files Modified:**
- `app.py` - Added format conversion functions and download UI
- `pyproject.toml` - Added markdown dependency

**Result:** Users can now download itineraries in 3 different formats with one click!

---

## [0.1.6] - 2025-10-03

### Fixed

#### ⏱️ **Removed Execution Traces Timeout Prompt**
- **Issue**: CrewAI showing "Would you like to view your execution traces? [y/N] (20s timeout)" 
- **Fix**: Disabled CrewAI telemetry and execution traces
- **Changes**:
  - Added `memory=False` to Crew configuration
  - Added `embedder=None` to Crew configuration
  - Added `CREWAI_TELEMETRY=false` to `.env` file
  
**Files Modified:**
- `src/ai_travel_agent/crew.py` - Disabled memory and embedder
- `.env` - Added CREWAI_TELEMETRY setting

**Result:** No more timeout prompts interrupting the workflow!

---

## [0.1.5] - 2025-10-03

### Changed

#### 🌙 **Complete Dark Theme Redesign**
- **Change**: Transformed entire UI from flashy gradients to professional dark theme
- **Reason**: User preference for darker, more subdued professional appearance
- **New Color Scheme**:
  - **Background:** Dark navy/slate (#0f1419, #1a1f2e, #1e293b)
  - **Text:** Light gray/white (#e2e8f0, #cbd5e1)
  - **Accents:** Blue (#3b82f6), Green (#10b981), Amber (#f59e0b)
  - **Borders:** Subtle dark gray (#2d3748, #475569)
  
**Key Changes:**
- Header: Dark gradient background instead of purple
- Sidebar: Navy background (#1a1f2e) with subtle borders
- Chat messages: Dark slate backgrounds with accent borders
- Buttons: Dark with blue accents, subtle hover effects
- Input fields: Dark backgrounds with blue focus states
- Tabs: Dark theme with selected state highlighting
- Stats box: Dark with blue accent border
- All text: Light colors for high contrast on dark backgrounds

**Design Philosophy:**
- Professional, subdued color palette
- No flashy gradients - solid dark colors
- Subtle accents using blue, green, amber
- High readability with proper contrast
- Modern, clean aesthetic

**Files Modified:**
- `app.py` - Complete CSS overhaul for dark theme (380+ lines)

---

## [0.1.4] - 2025-10-03

### Fixed

#### 🎨 **Sidebar UI Visibility Issues**
- **Issue**: Form fields in sidebar had poor visibility (dark text on dark backgrounds)
- **Fix**: Complete sidebar styling overhaul with high-contrast, clean design
- **Changes**:
  - White background for all input fields with dark text (#1a1a1a)
  - Styled expander with white content area and visible borders
  - Improved header layout with logo and title alignment
  - Added focus states with purple highlight (#667eea)
  - Better spacing and padding throughout sidebar
  - Fixed date picker and number input visibility
  - Added divider styling for clear sections
  
**Specific Improvements:**
- Input fields: White bg, dark text, 2px borders
- Expander: White content area with padding
- Labels: Dark gray (#2d3748), bold, clear
- Dividers: Proper spacing (1.5rem margins)
- Logo: Aligned with "Trip Planner" header
- All controls now clearly visible and accessible

**Files Modified:**
- `app.py` - Enhanced sidebar CSS and layout structure

---

## [0.1.3] - 2025-10-03

### Fixed

#### 🚦 **Rate Limit Handling**
- **Issue**: GPT-4o experiencing rate limits during high demand periods
- **Fix**: Changed default model to GPT-4 for better availability
- **Changes**:
  - Updated `.env` to use `MODEL=gpt-4` instead of `gpt-4o`
  - Made model configurable via environment variable
  - Added `python-dotenv` for proper env loading
  - Added model options documentation in `.env`
  - Created `RATE_LIMIT_FIX.md` guide
  
**Files Modified:**
- `.env` - Changed to gpt-4, added model options comments
- `app.py` - Load model from environment variable
- `pyproject.toml` - Added python-dotenv dependency
- `RATE_LIMIT_FIX.md` - Created comprehensive troubleshooting guide

**Benefits:**
- More stable API availability
- Easy model switching (just edit .env)
- Better error handling

---

## [0.1.2] - 2025-10-03

### Improved

#### 🎨 **UI/UX Enhancements**
- **Improved text visibility** in chat messages with darker, high-contrast colors
  - User messages: Dark blue text (#0D47A1) on light blue gradient background
  - Assistant messages: Dark green text (#1B5E20) on light green gradient background
  - System messages: Dark orange text (#E65100) on light orange gradient background
- **Reorganized sidebar controls** for better visual hierarchy
  - Added styled section header for "Session Controls"
  - Stacked buttons vertically instead of side-by-side
  - Added helpful tooltips to buttons
- **Enhanced session statistics display**
  - Moved from plain info box to styled gradient container
  - Improved color scheme (purple/indigo gradient)
  - Better typography and spacing
- **Added custom font** (Inter) for modern, professional look
- **Improved button styling** with gradients and hover effects
- **Better spacing and padding** throughout the interface
- **Hide Streamlit branding** for cleaner appearance
- **Smooth animations** for chat messages (fade-in effect)

**Files Modified:**
- `app.py` - Completely redesigned CSS and sidebar layout

---

## [0.1.1] - 2025-10-03

### Fixed

#### 🐛 **SerperDevTool Initialization Error**
- **Issue**: App crashed when SerperDevTool failed to initialize (missing SERPER_API_KEY)
- **Fix**: Added error handling in `crew.py` to gracefully handle missing API keys
- **Changes**:
  - Wrapped SerperDevTool initialization in try-except block
  - Made search tool optional (works without it, though with limited web search)
  - Removed tool reference from `agents.yaml` (tools now added programmatically)
  - Added SERPER_API_KEY placeholder to `.env` file
- **Files Modified**:
  - `src/ai_travel_agent/crew.py` - Added error handling and conditional tool assignment
  - `src/ai_travel_agent/config/agents.yaml` - Removed tools section from destination_researcher
  - `.env` - Added SERPER_API_KEY entry

**How to Fix**:
Get a free Serper API key at https://serper.dev/ and add it to your `.env` file, or the app will work without web search capabilities.

---

## [0.1.0] - 2025-10-03

### Added - Initial AI Travel Agent Implementation

#### 🎨 **Streamlit Web Application (`app.py`)**
- Created modern, interactive web interface with Streamlit
- Implemented session state management to remember conversation context
- Added chat interface for asking follow-up questions about itineraries
- Implemented "Clear Session" functionality to reset conversations
- Created three-tab layout:
  - **Chat & Ask Questions**: Interactive Q&A about generated itineraries
  - **Full Itinerary**: Display complete trip details with download option
  - **Export Files**: Instructions for calendar import and file locations
- Added real-time conversation memory using GPT-4o for contextual responses
- Implemented modern UI with custom CSS styling and gradient headers
- Added file download functionality for markdown itineraries
- Created session info sidebar showing message count and context items

#### 🤖 **Travel Agent Configuration**

**Agents (`src/ai_travel_agent/config/agents.yaml`):**
- **Destination Researcher**: Researches attractions, accommodations, restaurants, and local experiences
  - Equipped with SerperDevTool for web search capabilities
  - Specializes in finding hidden gems and seasonal events
- **Itinerary Planner**: Creates balanced day-by-day travel schedules
  - Optimizes activity timing and logistics
  - Balances sightseeing with rest time
- **Calendar Formatter**: Formats itineraries for calendar applications
  - Equipped with CalendarGeneratorTool
  - Ensures proper event formatting with dates, times, and locations

**Tasks (`src/ai_travel_agent/config/tasks.yaml`):**
- **research_destination_task**: Comprehensive destination research
  - Finds 10-15 attractions/activities
  - Recommends 5-7 restaurants
  - Suggests 3-5 accommodation options
  - Provides practical travel tips and local insights
- **plan_itinerary_task**: Creates detailed day-by-day itineraries
  - Includes specific times for all activities
  - Provides meal recommendations
  - Estimates daily costs
  - Considers opening hours and travel times
  - Outputs to `travel_itinerary.md`
- **format_calendar_task**: Transforms itinerary into calendar events
  - Creates structured event data with titles, dates, times, locations
  - Outputs to `calendar_events.txt`

#### 🛠️ **Custom Tools (`src/ai_travel_agent/tools/custom_tool.py`)**
- **CalendarGeneratorTool**: Generates .ics calendar files
  - Parses formatted event data into iCalendar format
  - Supports multiple date/time formats
  - Creates calendar-compatible files for Google Calendar, Apple Calendar, Outlook
  - Handles event properties: title, start/end times, location, description
  - Generates unique event UIDs

#### 🎯 **Crew Implementation (`src/ai_travel_agent/crew.py`)**
- Configured AiTravelAgent crew with three specialized agents
- Integrated SerperDevTool for web search
- Integrated CalendarGeneratorTool for calendar exports
- Set up sequential process workflow
- Added proper tool initialization in `__init__` method
- Created agent methods: `destination_researcher()`, `itinerary_planner()`, `calendar_formatter()`
- Created task methods: `research_destination_task()`, `plan_itinerary_task()`, `format_calendar_task()`

#### 📝 **Main Application (`src/ai_travel_agent/main.py`)**
- Updated `run()` function with travel-specific inputs
- Changed from generic "AI LLMs" topic to travel planning
- Added input parameters:
  - `destination`: Travel destination
  - `days`: Trip duration
  - `start_date`: Trip start date (YYYY-MM-DD format)
  - `preferences`: Detailed travel preferences (budget, interests, style, etc.)
- Added informative console output with emojis and formatting
- Updated `train()` and `test()` functions with travel examples
- Added success messages with file location information

#### 📦 **Dependencies (`pyproject.toml`)**
- Updated project description
- Added `icalendar>=6.0.1` for calendar file generation
- Added `pytz>=2024.1` for timezone handling
- Added `streamlit>=1.28.0` for web interface
- Added `openai>=1.0.0` for GPT-4o API access

#### 📚 **Documentation (`README.md`)**
- Completely rewrote README for travel agent application
- Added comprehensive feature list with emojis
- Created detailed installation instructions
- Added usage examples for different trip types:
  - Weekend city breaks
  - Adventure travel
  - Family vacations
- Documented the three-agent architecture
- Added calendar import instructions for Google Calendar, Apple Calendar, and Outlook
- Included troubleshooting section
- Added API key setup instructions

### Technical Details

**Files Created:**
- `app.py` - Streamlit web application (432 lines)
- `CHANGELOG.md` - This file

**Files Modified:**
- `src/ai_travel_agent/config/agents.yaml` - Replaced generic agents with travel specialists
- `src/ai_travel_agent/config/tasks.yaml` - Created travel-specific tasks
- `src/ai_travel_agent/tools/custom_tool.py` - Replaced example tool with CalendarGeneratorTool (172 lines)
- `src/ai_travel_agent/crew.py` - Updated crew configuration for travel agents (87 lines)
- `src/ai_travel_agent/main.py` - Updated with travel inputs and formatting (110 lines)
- `pyproject.toml` - Added new dependencies
- `README.md` - Complete rewrite with travel agent documentation (243 lines)

### Features Summary

✅ **Core Functionality:**
- AI-powered destination research
- Personalized itinerary generation
- Calendar export (.ics format)
- Budget-aware planning
- Preference matching

✅ **Streamlit UI Features:**
- Session state management
- Conversation memory
- Follow-up question capability
- Clear session functionality
- Modern, responsive design
- File download options
- Real-time chat interface
- Multi-tab organization

✅ **Output Files:**
- `travel_itinerary.md` - Markdown itinerary
- `calendar_events.txt` - Event details
- `[destination]_itinerary.ics` - Calendar file

### Running the Application

**Command-line version:**
```bash
crewai run
```

**Streamlit web interface:**
```bash
streamlit run app.py
```

### Notes
- Requires OpenAI API key and Serper API key in `.env` file
- Uses GPT-4o for intelligent planning and Q&A
- Session state persists during browser session
- All generated files saved to project root directory
