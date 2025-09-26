import streamlit as st
from utils import run_agent_sync
import os

st.set_page_config(page_title="MCP POC", page_icon="🤖", layout="wide")

st.title("Model Context Protocol(MCP) - Learning Path Generator")

# Initialize session state for progress
if 'current_step' not in st.session_state:
    st.session_state.current_step = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'last_section' not in st.session_state:
    st.session_state.last_section = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# Sidebar title and configuration
st.sidebar.title("Learning Path")
st.sidebar.subheader("Configuration")

# API Key input (prefill from env or secrets if available)
default_google_key = os.environ.get("GOOGLE_API_KEY", "")
try:
    if not default_google_key:
        default_google_key = st.secrets.get("GOOGLE_API_KEY", "")  # type: ignore[attr-defined]
except Exception:
    pass
google_api_key = st.sidebar.text_input("Google API Key", value=default_google_key, type="password", help="You can also set env var GOOGLE_API_KEY before launch.")

# Pipedream URLs (prefill from env if present)
st.sidebar.subheader("Pipedream URLs")
default_youtube_url = os.environ.get("YOUTUBE_PIPEDREAM_URL", "")
default_drive_url = os.environ.get("DRIVE_PIPEDREAM_URL", "")
default_notion_url = os.environ.get("NOTION_PIPEDREAM_URL", "")
youtube_pipedream_url = st.sidebar.text_input(
    "YouTube URL (Required)",
    value=default_youtube_url,
    placeholder="Enter your Pipedream YouTube URL",
    help="Set env var YOUTUBE_PIPEDREAM_URL to prefill."
)

# Secondary tool selection
secondary_tool = st.sidebar.radio(
    "Select Secondary Tool:",
    ["Drive", "Notion"]
)

# Secondary tool URL input
if secondary_tool == "Drive":
    drive_pipedream_url = st.sidebar.text_input(
        "Drive URL",
        value=default_drive_url,
        placeholder="Enter your Pipedream Drive URL",
        help="Set env var DRIVE_PIPEDREAM_URL to prefill."
    )
    notion_pipedream_url = None
else:
    notion_pipedream_url = st.sidebar.text_input(
        "Notion URL",
        value=default_notion_url,
        placeholder="Enter your Pipedream Notion URL",
        help="Set env var NOTION_PIPEDREAM_URL to prefill."
    )
    drive_pipedream_url = None

 

# Quick guide before goal input
st.info("""
**Quick Guide:**
1. Enter your Google API key and YouTube URL (required)
2. Select and configure your secondary tool (Drive or Notion)
3. Enter a clear learning goal, for example:
    - "I want to learn python basics in 3 days"
    - "I want to learn data science basics in 10 days"
""")

# Main content area
st.header("Enter Your Goal")
user_goal = st.text_input("Enter your learning goal:",
                        help="Describe what you want to learn, and we'll generate a structured path using YouTube content and your selected tool.")

# Progress area
progress_container = st.container()
progress_bar = st.empty()

def update_progress(message: str):
    """Update progress in the Streamlit UI"""
    st.session_state.current_step = message
    
    # Determine section and update progress
    if "Setting up agent with tools" in message:
        section = "Setup"
        st.session_state.progress = 0.1
    elif "Added Google Drive integration" in message or "Added Notion integration" in message:
        section = "Integration"
        st.session_state.progress = 0.2
    elif "Creating AI agent" in message:
        section = "Setup"
        st.session_state.progress = 0.3
    elif "Generating your learning path" in message:
        section = "Generation"
        st.session_state.progress = 0.5
    elif "Learning path generation complete" in message:
        section = "Complete"
        st.session_state.progress = 1.0
        st.session_state.is_generating = False
    else:
        section = st.session_state.last_section or "Progress"
    
    st.session_state.last_section = section
    
    # Show progress bar
    progress_bar.progress(st.session_state.progress)
    
    # Update progress container with current status
    with progress_container:
        # Show section header if it changed
        if section != st.session_state.last_section and section != "Complete":
            st.write(f"**{section}**")
        
        # Show message with tick for completed steps
        if message == "Learning path generation complete!":
            st.success("All steps completed! 🎉")
        else:
            prefix = "✓" if st.session_state.progress >= 0.5 else "→"
            st.write(f"{prefix} {message}")

# Generate Learning Path button
if st.button("Generate Learning Path", type="primary", disabled=st.session_state.is_generating):
    if not google_api_key:
        st.error("Please enter your Google API key in the sidebar.")
    elif not youtube_pipedream_url:
        st.error("YouTube URL is required. Please enter your Pipedream YouTube URL in the sidebar.")
    elif (secondary_tool == "Drive" and not drive_pipedream_url) or (secondary_tool == "Notion" and not notion_pipedream_url):
        st.error(f"Please enter your Pipedream {secondary_tool} URL in the sidebar.")
    elif not user_goal:
        st.warning("Please enter your learning goal.")
    else:
        try:
            # Set generating flag
            st.session_state.is_generating = True
            
            # Reset progress
            st.session_state.current_step = ""
            st.session_state.progress = 0
            st.session_state.last_section = ""
            
            result = run_agent_sync(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                user_goal=user_goal,
                progress_callback=update_progress
            )
            
            # Display results
            st.header("Your Learning Path")
            # print(result)
            if result and "messages" in result:
                for msg in result["messages"]:
                    st.markdown(f"📚 {msg.content}")

            else:
                st.error("No results were generated. Please try again.")
                st.session_state.is_generating = False
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your API keys and URLs, and try again.")
            st.session_state.is_generating = False
