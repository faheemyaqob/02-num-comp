import streamlit as st
import random
from PIL import Image
import io
import base64

# Embedded images as base64 strings
def get_base64_image(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode()

# Sidebar with rules
with st.sidebar:
    st.header("🧠 How to Play")
    st.write("""
    1. Think of a secret number (1-100)
    2. I'll try to guess it
    3. Tell me if I'm:
       - 📉 Too Low
       - 📈 Too High
       - 🎯 Correct!
    """)
    st.markdown("---")
    st.write("✨ **Pro Tip**: I'll always guess in 7 tries or less!")
    st.markdown("---")
    st.write("Built with ❤️ and Streamlit")

# Main game
st.title("🔢 Number Mind Reader")
st.subheader("I can guess your number in 7 tries or less!")

# Initialize game state
if 'game' not in st.session_state:
    st.session_state.game = {
        'low': 1,
        'high': 100,
        'guess': random.randint(1, 100),
        'attempts': 0,
        'active': False
    }

def start_game():
    st.session_state.game = {
        'low': 1,
        'high': 100,
        'guess': random.randint(1, 100),
        'attempts': 0,
        'active': True
    }

# Start/Restart button
if st.button("🎮 Start Game", type="primary"):
    start_game()
    st.rerun()

g = st.session_state.game  # Shorter reference

if g['active']:
    # Display current guess
    st.markdown(f"""
    ### My guess #{g['attempts']+1}:
    # 🔮 **{g['guess']}**
    """)
    
    # Feedback buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📉 Too Low", help="My guess is below your number"):
            g['low'] = g['guess'] + 1
            g['attempts'] += 1
            g['guess'] = (g['low'] + g['high']) // 2
            st.rerun()
    
    with col2:
        if st.button("🎯 Correct!", type="primary", help="I guessed it!"):
            g['attempts'] += 1
            st.balloons()
            st.success(f"""
            ## 🏆 Got it in {g['attempts']} tries!
            Your number was {g['guess']}!
            """)
            g['active'] = False
    
    with col3:
        if st.button("📈 Too High", help="My guess is above your number"):
            g['high'] = g['guess'] - 1
            g['attempts'] += 1
            g['guess'] = (g['low'] + g['high']) // 2
            st.rerun()
    
    # Cheat detection
    if g['high'] < g['low']:
        st.error("""
        ## 🚨 Impossible!
        You must have changed your number!
        """)
        g['active'] = False
else:
    # Start screen
    st.markdown("""
    ## Ready to challenge me?
    Think of any number between 1 and 100...
    """)
    st.write("⬆️ Click **Start Game** when ready!")