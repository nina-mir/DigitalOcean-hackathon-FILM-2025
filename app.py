import streamlit as st
from src.chatbot_coordinator import ChatbotCoordinator
from src.response_formatter import ResponseFormatter
import pandas as pd

# Page config 
st.set_page_config(
    page_title="SF Film Locations Chat",
    page_icon="🎬🌉🌁😶‍🌫️🌫️👩🏽‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✨ BEAUTIFUL CUSTOM CSS
st.markdown("""
<style>
    /* Main chat container */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ✨ BEAUTIFUL HEADER
st.markdown("""
<div class="main-header">
    <h1>🎬 San Francisco Film Locations</h1>
    <p>Explore thousands of filming locations using natural language</p>
</div>
""", unsafe_allow_html=True)



# Initialize session state
def initialize_session_state():
    """Setup session variables on first run"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'coordinator' not in st.session_state:
        st.session_state.coordinator = ChatbotCoordinator()
    
    if 'formatter' not in st.session_state:
        st.session_state.formatter = ResponseFormatter()
    
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None

# Main app function
def main():
    initialize_session_state()
    
    # Sidebar
    display_sidebar()
    
    # Create a container for chat history with max height
    chat_container = st.container()
    
    with chat_container:
        display_chat_history()
    
    # Input ALWAYS at bottom, outside containers
    handle_user_input()

def display_chat_history():
    """Render all previous messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display additional components (maps, dataframes)
            if "map_html" in message:
                st.components.v1.html(message["map_html"], height=500)
            
            if "dataframe" in message:
                st.dataframe(message["dataframe"])

def handle_user_input():
    """Process new user messages"""
    user_input = None
    
    # Check if there's a pending query from sidebar button
    if 'pending_query' in st.session_state:
        user_input = st.session_state.pending_query
        # Clear it so it doesn't repeat
        del st.session_state.pending_query
    else:
        # Normal chat input
        user_input = st.chat_input("Ask me about SF film locations...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process and respond
        with st.chat_message("assistant"):
            with st.spinner("🔍 Processing your query..."):
                response = process_user_message(user_input)
                display_response(response)

def process_user_message(user_input: str):
    """Send message to coordinator and get response"""
    coordinator = st.session_state.coordinator
    formatter = st.session_state.formatter
    
    try:
        print(f"\n🔍 APP: Processing message: '{user_input}'")
        
        # Route message and get results
        result = coordinator.handle_message(
            user_input,
            context={'last_result': st.session_state.last_result}
        )
        
        print(f"🔍 APP: Got result from coordinator")
        print(f"🔍 APP: Result type: {result.get('type')}")
        print(f"🔍 APP: Result keys: {result.keys()}")
        
        # Store result for follow-ups
        st.session_state.last_result = result
        
        # Format for display
        print(f"🔍 APP: Calling formatter.format_response()")
        formatted_response = formatter.format_response(result)
        
        print(f"🔍 APP: Got formatted response")
        print(f"🔍 APP: Formatted keys: {formatted_response.keys()}")
        
        return formatted_response
        
    except Exception as e:
        print(f"\n❌ APP ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'content': f"⚠️ Oops! Something went wrong: {str(e)}",
            'type': 'error'
        }

def display_response(response):
    """Display formatted response"""
    # Display text content
    st.markdown(response['content'])
    
    # Display dataframe if present
    if 'dataframe' in response:
        df = response['dataframe']
        
        # Show dataframe
        if len(df) > 20:
            with st.expander(f"📊 View All {len(df)} Results", expanded=False):
                st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
        
        # Add download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            key=f"download_{hash(str(df))}"  # Unique key
        )
    
    # Display map if present
    if 'map_html' in response:
        st.components.v1.html(response['map_html'], height=500)
    
    # Add response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['content'],
        **{k: v for k, v in response.items() if k != 'content'}
    })


def display_sidebar():
    """Enhanced sidebar with examples and stats"""
    with st.sidebar:
        st.markdown("### 🎯 Quick Start")
        
        example_queries = [
            ("🌉", "What films were shot at the Golden Gate Bridge?"),
            ("📍","Find all movies shot within 0.5 mile radius of the Union Square. List the film names and the specific location."),
            ("🎭", "Show me all Hitchcock filming locations"),
            ("🎭","Any films made in 1910s in SF?"),
            ("📅", "How many movies from the 1970s?"),
            ("⭐", "Which actor appeared in the most films?"),
            ("🎬", "Films with 'matrix' in the title")
        ]
        
        for emoji, query in example_queries:
            if st.button(
                f"{emoji} {query}", 
                key=f"example_{hash(query)}", 
                use_container_width=True
            ):
                st.session_state.pending_query = query
                st.rerun()
        
        st.markdown("---")
        
        # 📈 DATABASE STATS - COOL!
        st.markdown("### 📈 Database Stats")
        try:
            gdf = st.session_state.coordinator.query_processor.gdf
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📍 Locations", f"{len(gdf):,}")
                unique_films = gdf[['Title', 'Year']].drop_duplicates()
                st.metric("🎬 Films", f"{len(unique_films):,}")
            
            with col2:
                unique_actors = pd.concat([
                    gdf['Actor_1'], gdf['Actor_2'], gdf['Actor_3']
                ]).dropna().nunique()
                st.metric("⭐ Actors", f"{unique_actors:,}")
                
                years = pd.to_numeric(gdf['Year'], errors='coerce').dropna()
                if len(years) > 0:
                    st.metric("📅 Years", f"{int(years.min())}-{int(years.max())}")
        except Exception as e:
            st.info("Stats loading...")
        
        st.markdown("---")
        
        # HELP SECTION
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            **Ask questions like:**
            - "Films shot at [location]"
            - "All [director] movies"
            - "Which actor appeared most?"
            - "How many movies from [year]?"
            
            **Features:**
            - 🗺️ Interactive maps
            - 📊 Downloadable data tables
            - 💬 Natural language queries
            """)
        
        # RESET BUTTON
        st.markdown("---")
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_result = None
            st.success("Chat cleared!")
            st.rerun()





if __name__ == "__main__":
    main()
