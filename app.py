#!/usr/bin/env python
"""
AI Travel Agent - Streamlit Web Application
A modern, interactive UI for generating personalized travel itineraries
"""

import streamlit as st
from datetime import datetime, timedelta
import os
from pathlib import Path
import warnings
from dotenv import load_dotenv
from io import BytesIO
import zipfile

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from ai_travel_agent.crew import AiTravelAgent

# Page configuration
st.set_page_config(
    page_title="AI Travel Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark professional theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app background */
    .main {
        background-color: #0f1419;
    }
    
    /* Header styling - Dark theme */
    .main-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: #e2e8f0;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #2d3748;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    .main-header p {
        margin: 0.75rem 0 0 0;
        font-size: 1.05rem;
        opacity: 0.8;
        font-weight: 400;
        color: #94a3b8;
    }
    
    /* Sidebar dark theme */
    section[data-testid="stSidebar"] {
        background-color: #1a1f2e;
        border-right: 1px solid #2d3748;
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1rem;
    }
    
    /* Sidebar headings */
    section[data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #e2e8f0;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] label {
        color: #cbd5e1;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    section[data-testid="stSidebar"] p {
        color: #94a3b8;
    }
    
    /* Chat message styling - Dark theme */
    .chat-message {
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #2d3748;
        animation: fadeIn 0.3s ease-in;
        line-height: 1.6;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background-color: #1e293b;
        border-left: 3px solid #3b82f6;
        margin-left: 2rem;
        color: #e2e8f0;
        font-weight: 400;
    }
    
    .assistant-message {
        background-color: #1a2332;
        border-left: 3px solid #10b981;
        margin-right: 2rem;
        color: #e2e8f0;
        font-weight: 400;
    }
    
    .system-message {
        background-color: #1f2937;
        border-left: 3px solid #f59e0b;
        color: #e2e8f0;
        font-weight: 400;
    }
    
    .chat-message strong {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.7;
        color: #94a3b8;
    }
    
    /* Button styling - Dark theme */
    .stButton > button {
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        border: 1px solid #2d3748;
        font-size: 0.95rem;
        width: 100%;
        background-color: #1e293b;
        color: #ffffff;
    }
    
    .stButton > button:hover {
        background-color: #334155;
        border-color: #475569;
        transform: translateY(-1px);
    }
    
    /* Primary button */
    button[kind="primary"] {
        background-color: #3b82f6 !important;
        color: white !important;
        border: 1px solid #2563eb !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #2563eb !important;
        border-color: #1d4ed8 !important;
    }
    
    /* Control section styling - Dark theme */
    .control-header {
        font-size: 0.85rem;
        font-weight: 700;
        color: #94a3b8;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2d3748;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Stats box - Dark theme */
    .stats-container {
        background-color: #1e293b;
        padding: 1.25rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #2d3748;
        border-left: 3px solid #3b82f6;
    }
    
    .stats-container h3 {
        margin: 0 0 0.75rem 0;
        font-size: 0.85rem;
        font-weight: 700;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stats-container p {
        margin: 0.4rem 0;
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 400;
    }
    
    .stats-container strong {
        color: #e2e8f0;
    }
    
    /* Info boxes - Dark theme */
    .info-box {
        background-color: #1e293b;
        padding: 1.25rem;
        border-radius: 10px;
        border-left: 3px solid #10b981;
        border: 1px solid #2d3748;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #1e293b;
        padding: 1.75rem;
        border-radius: 10px;
        border: 1px solid #10b981;
        margin: 1rem 0;
    }
    
    /* Tab styling - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a1f2e;
        padding: 0.5rem;
        border-radius: 10px;
        border-bottom: 1px solid #2d3748;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #94a3b8;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e293b;
        color: #e2e8f0;
    }
    
    /* Input fields - Dark theme */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border-radius: 8px;
        border: 1px solid #2d3748;
        padding: 0.6rem;
        font-size: 0.95rem;
        background-color: #1e293b;
        color: #e2e8f0;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        background-color: #1e293b;
    }
    
    /* Expander - Dark theme */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #2d3748 !important;
        color: #e2e8f0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #3b82f6 !important;
        background-color: #1e293b !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background-color: #1a1f2e !important;
        border: 1px solid #2d3748;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem !important;
    }
    
    /* Ensure all sidebar inputs are visible - Dark theme */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="select"],
    section[data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748 !important;
    }
    
    section[data-testid="stSidebar"] input:focus,
    section[data-testid="stSidebar"] textarea:focus {
        border-color: #3b82f6 !important;
        background-color: #1e293b !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Date picker in sidebar */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {
        background-color: #1e293b !important;
        border-color: #2d3748 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
        color: #e2e8f0 !important;
        background-color: #1e293b !important;
    }
    
    /* Number input in sidebar */
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {
        margin: 1.5rem 0;
        border-color: #2d3748;
    }
    
    /* Streamlit specific overrides for dark theme */
    [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Alert boxes dark theme */
    .stAlert {
        background-color: #1e293b;
        border: 1px solid #2d3748;
        color: #e2e8f0;
    }
    
    .stWarning {
        background-color: #1e293b;
        border-left: 3px solid #f59e0b;
    }
    
    .stInfo {
        background-color: #1e293b;
        border-left: 3px solid #3b82f6;
    }
    
    .stSuccess {
        background-color: #1e293b;
        border-left: 3px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'itinerary_generated' not in st.session_state:
        st.session_state.itinerary_generated = False
    if 'current_itinerary' not in st.session_state:
        st.session_state.current_itinerary = None
    if 'conversation_context' not in st.session_state:
        st.session_state.conversation_context = []
    if 'last_inputs' not in st.session_state:
        st.session_state.last_inputs = None

def clear_session():
    """Clear all session data"""
    st.session_state.messages = []
    st.session_state.itinerary_generated = False
    st.session_state.current_itinerary = None
    st.session_state.conversation_context = []
    st.session_state.last_inputs = None
    st.rerun()

def rename_export_files(destination, start_date):
    """Rename exported files to include destination and start date for uniqueness"""
    # Clean up destination name for filename
    clean_dest = destination.replace(', ', '_').replace(' ', '_')
    date_prefix = start_date.replace('-', '')
    
    # Rename itinerary markdown file
    old_itinerary = 'exports/travel_itinerary.md'
    new_itinerary = f'exports/{date_prefix}_{clean_dest}_itinerary.md'
    if os.path.exists(old_itinerary):
        # Remove old file if it exists
        if os.path.exists(new_itinerary):
            os.remove(new_itinerary)
        os.rename(old_itinerary, new_itinerary)
    
    # Rename calendar events text file
    old_events = 'exports/calendar_events.txt'
    new_events = f'exports/{date_prefix}_{clean_dest}_calendar_events.txt'
    if os.path.exists(old_events):
        # Remove old file if it exists
        if os.path.exists(new_events):
            os.remove(new_events)
        os.rename(old_events, new_events)
    
    return new_itinerary, new_events

def get_export_filenames(destination, start_date):
    """Get the expected export filenames based on destination and start date"""
    clean_dest = destination.replace(', ', '_').replace(' ', '_')
    date_prefix = start_date.replace('-', '')
    
    return {
        'itinerary': f'exports/{date_prefix}_{clean_dest}_itinerary.md',
        'calendar_events': f'exports/{date_prefix}_{clean_dest}_calendar_events.txt',
        'ics': f'exports/{clean_dest}_itinerary.ics'
    }

def create_download_zip():
    """Create a ZIP file containing both itinerary and calendar files"""
    destination = st.session_state.last_inputs.get('destination', 'itinerary').replace(', ', '_').replace(' ', '_')
    start_date = st.session_state.last_inputs.get('start_date', '').replace('-', '')
    
    # Get expected filenames
    filenames = get_export_filenames(
        st.session_state.last_inputs.get('destination', 'itinerary'),
        st.session_state.last_inputs.get('start_date', '')
    )
    
    # Create a BytesIO object to store the zip file
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add itinerary markdown file
        if os.path.exists(filenames['itinerary']):
            zip_file.write(filenames['itinerary'], os.path.basename(filenames['itinerary']))
        
        # Add calendar events text file
        if os.path.exists(filenames['calendar_events']):
            zip_file.write(filenames['calendar_events'], os.path.basename(filenames['calendar_events']))
        
        # Add ICS calendar file
        if os.path.exists(filenames['ics']):
            zip_file.write(filenames['ics'], os.path.basename(filenames['ics']))
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue(), f"{start_date}_{destination}_trip_files.zip"

def display_message(role, content, icon=None):
    """Display a chat message with styling"""
    if role == "user":
        css_class = "user-message"
        default_icon = "👤"
    elif role == "assistant":
        css_class = "assistant-message"
        default_icon = "🤖"
    else:
        css_class = "system-message"
        default_icon = "ℹ️"
    
    icon = icon or default_icon
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{icon} {role.title()}:</strong><br/>
        {content}
    </div>
    """, unsafe_allow_html=True)

def generate_itinerary(destination, days, start_date, preferences):
    """Generate travel itinerary using CrewAI agents"""
    inputs = {
        'destination': destination,
        'days': str(days),
        'start_date': start_date,
        'preferences': preferences
    }
    
    # Store inputs for context
    st.session_state.last_inputs = inputs
    
    with st.spinner('🔍 Researching destination and planning your perfect trip...'):
        try:
            # Run the crew
            crew = AiTravelAgent()
            result = crew.crew().kickoff(inputs=inputs)
            
            # Rename files to include destination and date for uniqueness
            itinerary_file, events_file = rename_export_files(destination, start_date)
            
            # Read generated files from exports folder
            itinerary_content = ""
            if os.path.exists(itinerary_file):
                with open(itinerary_file, 'r', encoding='utf-8') as f:
                    itinerary_content = f.read()
            
            # Store in session state
            st.session_state.current_itinerary = itinerary_content
            st.session_state.itinerary_generated = True
            
            # Add to conversation context
            context_summary = f"Generated itinerary for {destination} ({days} days starting {start_date})"
            st.session_state.conversation_context.append({
                'type': 'itinerary_generation',
                'inputs': inputs,
                'timestamp': datetime.now().isoformat(),
                'summary': context_summary
            })
            
            return True, itinerary_content
        except Exception as e:
            return False, str(e)

def answer_question(question):
    """Answer questions about the itinerary using GPT"""
    from openai import OpenAI
    
    # Build context from conversation history
    context_messages = []
    
    # Add itinerary context
    if st.session_state.current_itinerary:
        context_messages.append({
            "role": "system",
            "content": f"""You are a helpful travel assistant. You have generated the following itinerary:

{st.session_state.current_itinerary}

Answer questions about this itinerary, provide suggestions, and help the user modify their plans. Be concise, helpful, and friendly."""
        })
    
    # Add conversation history
    for msg in st.session_state.messages[-5:]:  # Last 5 messages for context
        if msg['role'] in ['user', 'assistant']:
            context_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
    
    # Add current question
    context_messages.append({
        "role": "user",
        "content": question
    })
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        model = os.getenv('MODEL', 'gpt-4')  # Default to gpt-4 if not set
        response = client.chat.completions.create(
            model=model,
            messages=context_messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Add to conversation context
        st.session_state.conversation_context.append({
            'type': 'qa',
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
        return answer
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main application"""
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 AI Travel Agent</h1>
        <p>Your intelligent travel companion powered by GPT-4o</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Logo and title
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://img.icons8.com/fluency/96/000000/around-the-globe.png", width=60)
        with col2:
            st.markdown("### ✈️ Trip Planner")
        
        st.markdown("---")
        
        # New itinerary form
        with st.expander("📝 Generate New Itinerary", expanded=not st.session_state.itinerary_generated):
            destination = st.text_input(
                "🗺️ Destination",
                value="Paris, France",
                placeholder="e.g., Tokyo, Japan"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                days = st.number_input(
                    "📅 Days",
                    min_value=1,
                    max_value=30,
                    value=5
                )
            with col2:
                start_date = st.date_input(
                    "🗓️ Start Date",
                    value=datetime.now() + timedelta(days=30)
                )
            
            preferences = st.text_area(
                "✨ Your Preferences",
                value="""Budget: Mid-range ($100-200/day)
Interests: Culture, food, photography
Style: Mix of popular sites and local experiences
Pace: Relaxed, with downtime""",
                height=150,
                placeholder="Tell us about your travel style, budget, interests..."
            )
            
            if st.button("🚀 Generate Itinerary", type="primary", use_container_width=True):
                # Add user message
                st.session_state.messages.append({
                    'role': 'user',
                    'content': f"Generate a {days}-day itinerary for {destination} starting {start_date.strftime('%Y-%m-%d')}"
                })
                
                # Generate itinerary
                success, result = generate_itinerary(
                    destination,
                    days,
                    start_date.strftime('%Y-%m-%d'),
                    preferences
                )
                
                if success:
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': f"✅ I've created your personalized {days}-day itinerary for {destination}! Check it out below."
                    })
                    st.success("Itinerary generated successfully!")
                    st.rerun()
                else:
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': f"❌ Sorry, I encountered an error: {result}"
                    })
                    st.error(f"Error: {result}")
        
        # Session controls
        st.markdown('<div class="control-header">🔧 Session Controls</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Session", use_container_width=True, help="Reset all data and start fresh"):
            clear_session()
        
        # Download section - combined itinerary and calendar
        if st.session_state.itinerary_generated and st.session_state.current_itinerary:
            # Create and download ZIP file with both itinerary and calendar
            zip_data, zip_filename = create_download_zip()
            
            st.download_button(
                label="📥 Download All Trip Files (ZIP)",
                data=zip_data,
                file_name=zip_filename,
                mime="application/zip",
                use_container_width=True,
                help="Download itinerary (Markdown), calendar events (TXT), and calendar file (ICS) in one ZIP archive"
            )
        
        # Session info
        if st.session_state.itinerary_generated:
            st.markdown("""
            <div class="stats-container">
                <h3>📊 Session Statistics</h3>
                <p><strong>💬 Messages:</strong> {}</p>
                <p><strong>🧠 Context Items:</strong> {}</p>
                <p><strong>📍 Destination:</strong> {}</p>
            </div>
            """.format(
                len(st.session_state.messages),
                len(st.session_state.conversation_context),
                st.session_state.last_inputs.get('destination', 'N/A') if st.session_state.last_inputs else 'N/A'
            ), unsafe_allow_html=True)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["💬 Chat & Ask Questions", "📄 Full Itinerary", "📥 Export Files"])
    
    with tab1:
        st.markdown("### Ask me anything about your itinerary!")
        
        # Display chat messages
        if st.session_state.messages:
            for message in st.session_state.messages:
                display_message(message['role'], message['content'])
        else:
            st.info("👋 Welcome! Generate an itinerary to get started, then ask me questions about your trip!")
        
        # Chat input
        if st.session_state.itinerary_generated:
            with st.container():
                question = st.chat_input("Ask a question about your itinerary...")
                
                if question:
                    # Add user question
                    st.session_state.messages.append({
                        'role': 'user',
                        'content': question
                    })
                    
                    # Get answer
                    with st.spinner('🤔 Thinking...'):
                        answer = answer_question(question)
                    
                    # Add assistant response
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': answer
                    })
                    
                    st.rerun()
        else:
            st.warning("⚠️ Please generate an itinerary first to start asking questions!")
    
    with tab2:
        if st.session_state.current_itinerary:
            st.markdown("### 📋 Your Complete Itinerary")
            st.markdown(st.session_state.current_itinerary)
            
            # Download just the itinerary file
            filenames = get_export_filenames(
                st.session_state.last_inputs.get('destination', 'itinerary'),
                st.session_state.last_inputs.get('start_date', '')
            )
            
            if os.path.exists(filenames['itinerary']):
                with open(filenames['itinerary'], 'r', encoding='utf-8') as f:
                    itinerary_content = f.read()
                
                st.download_button(
                    label="📥 Download Itinerary (Text)",
                    data=itinerary_content,
                    file_name=os.path.basename(filenames['itinerary']),
                    mime="text/markdown",
                    use_container_width=True,
                    type="primary",
                    help="Download only the itinerary as a Markdown text file"
                )
        else:
            st.info("📝 Generate an itinerary to see it here!")
    
    with tab3:
        st.markdown("### 📥 Export Your Trip")
        
        if st.session_state.itinerary_generated:
            st.markdown("""
            <div class="success-box">
                <h4>✅ Files Generated Successfully!</h4>
                <p>Your trip files have been created with unique names in the exports folder:</p>
                <ul>
                    <li><strong>[date]_[destination]_itinerary.md</strong> - Complete day-by-day itinerary</li>
                    <li><strong>[date]_[destination]_calendar_events.txt</strong> - Event details for calendar import</li>
                    <li><strong>[destination]_itinerary.ics</strong> - Calendar file (iCal format)</li>
                </ul>
                <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">Each file is uniquely named with the destination and start date to prevent conflicts when generating multiple itineraries.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📆 Import to Calendar")
            st.markdown("""
            **Google Calendar:**
            1. Open Google Calendar
            2. Click ⚙️ Settings → Import & Export
            3. Select the `.ics` file
            4. Choose your calendar
            
            **Apple Calendar:**
            1. Double-click the `.ics` file
            2. Select destination calendar
            3. Click OK
            
            **Outlook:**
            1. File → Open & Export → Import/Export
            2. Select "Import an iCalendar (.ics) file"
            3. Browse and import
            """)
            
            # Download all files button
            st.markdown("#### 📁 Download Your Files")
            st.markdown("""
            Click the button below to download all your trip files in a single ZIP archive:
            - **Itinerary** (Markdown format) - Your complete day-by-day travel plan
            - **Calendar Events** (Text format) - Formatted event details for reference
            - **Calendar File** (ICS format) - Import directly into your calendar app
            
            All files are uniquely named with your destination and start date.
            """)
            
            zip_data, zip_filename = create_download_zip()
            
            st.download_button(
                label="📥 Download All Trip Files (ZIP)",
                data=zip_data,
                file_name=zip_filename,
                mime="application/zip",
                use_container_width=True,
                type="primary",
                help="Download all trip files (itinerary, calendar events, and ICS file) in one ZIP archive"
            )
        else:
            st.info("📝 Generate an itinerary to export files!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with ❤️ using CrewAI & Streamlit | Powered by OpenAI GPT-4o</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
