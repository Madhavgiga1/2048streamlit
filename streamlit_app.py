import streamlit as st
import streamlit.components.v1 as components
import copy
import gamelogic

# Page config
st.set_page_config(
    page_title="2048 Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Hide Streamlit stuff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Prevent scrolling - AGGRESSIVE */
    html, body {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    .main {
        overflow-y: hidden !important;
        padding-bottom: 0 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #faf8ef 0%, #f0e4d7 100%);
        overflow: hidden !important;
    }
    
    .block-container {
        padding: 1rem 1rem 0.5rem 1rem !important;
        max-width: 500px !important;
    }
    
    /* Title - Medium size */
    .game-title {
        font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #776e65;
        text-align: center;
        margin: 10px 0 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Score containers */
   .score-container {
        padding: 8px 12px;  /* Was 10px 15px */
    }


    
    .score-label {
        font-size: 11px;
        text-transform: uppercase;
        font-weight: bold;
        opacity: 0.8;
    }
    
    .score-value {
        font-size: 19px;
        font-weight: bold;
        margin-top: 3px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #8f7a66;
        color: white;
        font-size: 21px;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 8px;
        width: 100%;
        height: 40px;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background-color: #9f8a76;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Game container */
    .game-container {
        background: #bbada0;
        border-radius: 8px;
        padding: 8px;
        margin: 8px auto;
        max-width: 420px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Instructions */
    .instructions {
        text-align: center;
        color: #776e65;
        font-size: 11px;
        margin: 10px 0;
        font-family: 'Clear Sans', Arial, sans-serif;
    }
    
    .key-hint {
        display: inline-block;
        background: #8f7a66;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 0 3px;
        font-weight: bold;
        font-size: 11px;
    }
    
    /* Alerts - compact */
    .stAlert {
        border-radius: 6px;
        font-family: 'Clear Sans', Arial, sans-serif;
        padding: 8px;
        font-size: 13px;
        margin: 5px 0;
    }
    
    /* Hide that annoying warning */
    .stException {
        display: none !important;
    }
    
    /* Reduce column padding */
    [data-testid="column"] {
        padding: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# Keyboard handler - inject into parent
components.html("""
<script>
(function() {
    const parent = window.parent;
    
    function handleKey(e) {
        const keys = {
            'ArrowUp': '⬆', 'w': '⬆', 'W': '⬆',
            'ArrowDown': '⬇', 's': '⬇', 'S': '⬇',
            'ArrowLeft': '⬅', 'a': '⬅', 'A': '⬅',
            'ArrowRight': '➡', 'd': '➡', 'D': '➡'
        };
        
        if (keys[e.key]) {
            e.preventDefault();
            e.stopPropagation();
            
            const buttons = parent.document.querySelectorAll('button');
            buttons.forEach(btn => {
                if (btn.textContent.includes(keys[e.key])) {
                    btn.click();
                }
            });
            return false;
        }
    }
    
    parent.document.addEventListener('keydown', handleKey, true);
    parent.document.body.style.overflow = 'hidden';
    parent.document.addEventListener('wheel', e => e.preventDefault(), {passive: false});
})();
</script>
""", height=0)

# Session state
if 'board' not in st.session_state:
    st.session_state.board = gamelogic.initialize_board(4)
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.won = False

# Title
st.markdown('<div class="game-title">2048</div>', unsafe_allow_html=True)

# Scores
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="score-container">
        <div class="score-label">Score</div>
        <div class="score-value">{st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="score-container">
        <div class="score-label">Best</div>
        <div class="score-value">{st.session_state.high_score}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="score-container">
        <div class="score-label">Moves</div>
        <div class="score-value">{st.session_state.moves}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if st.button("🔄 New", key="new_game", use_container_width=True):
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.session_state.board = gamelogic.initialize_board(4)
        st.session_state.score = 0
        st.session_state.moves = 0
        st.session_state.game_over = False
        st.session_state.won = False
        st.rerun()

# Instructions
st.markdown("""
<div class="instructions">
    <span class="key-hint">↑</span> 
    <span class="key-hint">↓</span> 
    <span class="key-hint">←</span> 
    <span class="key-hint">→</span> 
    or <span class="key-hint">WASD</span>
</div>
""", unsafe_allow_html=True)

# Board
def get_tile_color(value):
    colors = {
        0: "#ffeaa7",      
        2: "#dfe6e9",      
        4: "#fab1a0",      
        8: "#ff7675",      
        16: "#fd79a8",     
        32: "#fdcb6e",     
        64: "#e17055",     
        128: "#74b9ff",    
        256: "#a29bfe",    
        512: "#6c5ce7",  
        1024: "#00b894",   
        2048: "#55efc4"    
    }
    return colors.get(value, "#ffeaa7")

def get_text_color(value):
    return "#776e65" if value <= 4 else "#f9f6f2"

def get_font_size(value):
    if value < 100:
        return "40px"
    elif value < 1000:
        return "34px"
    elif value < 10000:
        return "28px"
    else:
        return "22px"

st.markdown('<div class="game-container">', unsafe_allow_html=True)

for row in st.session_state.board:
    cols = st.columns(4)
    for idx, value in enumerate(row):
        with cols[idx]:
            bg_color = get_tile_color(value)
            text_color = get_text_color(value)
            font_size = get_font_size(value)
            display_value = str(value) if value != 0 else ""
            
            st.markdown(f"""
                <div style='
                    background: {bg_color};
                    color: {text_color};
                    height: 70px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: {font_size};
                    font-weight: bold;
                    font-family: "Clear Sans", Arial, sans-serif;
                    border-radius: 5px;
                    margin: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: all 0.15s ease-in-out;
                '>
                    {display_value}
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

def make_move(move_func, direction_name):
    if st.session_state.game_over:
        return False  # ← Add return False
    
    old_board = copy.deepcopy(st.session_state.board)
    new_board, points = move_func(st.session_state.board)
    
    if gamelogic.board_changed(old_board, new_board):
        # Valid move
        st.session_state.board = gamelogic.add_random_tile(new_board)
        st.session_state.score += points
        st.session_state.moves += 1
        
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        
        game_state = gamelogic.get_game_state(st.session_state.board)
        
        if game_state == "WON" and not st.session_state.won:
            st.session_state.won = True
            st.balloons()
        elif game_state == "LOST":
            st.session_state.game_over = True
        
        return True  # ← Add return True (valid move)
    else:
        # Invalid move
        st.toast(f"⚠️ Can't move {direction_name}!", icon="⚠️")
        return False  # ← Add return False (invalid move)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("⬆️", key="up", use_container_width=True):
        make_move(gamelogic.move_up, "UP")
        st.rerun()

with col3:
    st.write("")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️", key="left", use_container_width=True):
        make_move(gamelogic.move_left, "LEFT")
        st.rerun()

with col2:
    if st.button("⬇️", key="down", use_container_width=True):
        make_move(gamelogic.move_down, "DOWN")
        st.rerun()

with col3:
    if st.button("➡️", key="right", use_container_width=True):
        make_move(gamelogic.move_right, "RIGHT")
        st.rerun()

if st.session_state.game_over:
    st.error("🛑 Game Over! No more moves.")
elif st.session_state.won:
    st.success("🏆 You Won! Keep playing!")

# Footer
st.markdown("""
<div style='text-align: center; color: #776e65; font-size: 11px; 
     font-family: "Clear Sans", Arial, sans-serif; margin-top: 8px;'>
    2048 Game - Assignment for Exponent Energy
</div>
""", unsafe_allow_html=True)