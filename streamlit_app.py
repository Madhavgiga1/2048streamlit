import streamlit as st
import streamlit.components.v1 as components
import copy
import gamelogic  # Import our game logic module

# Page config
st.set_page_config(
    page_title="2048 Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #faf8ef 0%, #f0e4d7 100%);
    }
    
    /* Title styling */
    .game-title {
        font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 80px;
        font-weight: bold;
        color: #776e65;
        text-align: center;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Score container */
    .score-container {
        background: #bbada0;
        border-radius: 10px;
        padding: 15px 25px;
        color: white;
        font-family: 'Clear Sans', Arial, sans-serif;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .score-label {
        font-size: 13px;
        text-transform: uppercase;
        font-weight: bold;
        opacity: 0.8;
    }
    
    .score-value {
        font-size: 28px;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #8f7a66;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 15px;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background-color: #9f8a76;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Game container */
    .game-container {
        background: #bbada0;
        border-radius: 10px;
        padding: 15px;
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Instructions */
    .instructions {
        text-align: center;
        color: #776e65;
        font-size: 16px;
        margin: 20px 0;
        font-family: 'Clear Sans', Arial, sans-serif;
    }
    
    .key-hint {
        display: inline-block;
        background: #8f7a66;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        margin: 0 5px;
        font-weight: bold;
    }
    
    /* Info messages */
    .stAlert {
        border-radius: 8px;
        font-family: 'Clear Sans', Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Keyboard event handler with scroll prevention
components.html("""
<script>
// Focus on the document to capture keyboard events
window.focus();

// Prevent arrow key scrolling
document.addEventListener('keydown', function(e) {
    // Arrow keys
    if(['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'w', 'a', 's', 'd'].includes(e.key)) {
        e.preventDefault();  // Prevent page scroll
        
        const streamlitDoc = window.parent.document;
        const buttons = streamlitDoc.querySelectorAll('button');
        
        buttons.forEach(button => {
            const text = button.innerText || button.textContent;
            
            // Arrow keys
            if ((e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') && text.includes('⬆')) {
                button.click();
            }
            if ((e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') && text.includes('⬇')) {
                button.click();
            }
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && text.includes('⬅')) {
                button.click();
            }
            if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && text.includes('➡')) {
                button.click();
            }
        });
    }
}, true);  // Use capture phase

// Also prevent space bar from scrolling
document.addEventListener('keydown', function(e) {
    if(e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
    }
});
</script>
""", height=0)

# Session state initialization
if 'board' not in st.session_state:
    st.session_state.board = gamelogic.initialize_board(4)
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.won = False

st.markdown('<div class="game-title">2048</div>', unsafe_allow_html=True)

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
    if st.button("🔄 New Game", use_container_width=True):
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
    Use <span class="key-hint">↑</span> 
    <span class="key-hint">↓</span> 
    <span class="key-hint">←</span> 
    <span class="key-hint">→</span> 
    or <span class="key-hint">WASD</span> to move tiles
</div>
""", unsafe_allow_html=True)

# Game board
def get_tile_color(value):
    """Get color for tile based on value"""
    colors = {
        0: "#cdc1b4",
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e",
        4096: "#3c3a32",
        8192: "#3c3a32"
    }
    return colors.get(value, "#3c3a32")

def get_text_color(value):
    """Get text color based on tile value"""
    return "#776e65" if value <= 4 else "#f9f6f2"

def get_font_size(value):
    """Get font size based on tile value"""
    if value < 100:
        return "55px"
    elif value < 1000:
        return "45px"
    elif value < 10000:
        return "35px"
    else:
        return "30px"

# Display board
st.markdown('<div class="game-container">', unsafe_allow_html=True)

for row_idx, row in enumerate(st.session_state.board):
    cols = st.columns(4)
    for col_idx, value in enumerate(row):
        with cols[col_idx]:
            bg_color = get_tile_color(value)
            text_color = get_text_color(value)
            font_size = get_font_size(value)
            display_value = str(value) if value != 0 else ""
            
            st.markdown(f"""
                <div style='
                    background: {bg_color};
                    color: {text_color};
                    height: 106px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: {font_size};
                    font-weight: bold;
                    font-family: "Clear Sans", Arial, sans-serif;
                    border-radius: 6px;
                    margin: 7px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: all 0.15s ease-in-out;
                '>
                    {display_value}
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Move function
def make_move(move_func, direction):
    """Execute move and update game state"""
    if st.session_state.game_over:
        return
    
    old_board = copy.deepcopy(st.session_state.board)
    new_board, points = move_func(st.session_state.board)
    
    if gamelogic.board_changed(old_board, new_board):
        # Valid move
        st.session_state.board = gamelogic.add_random_tile(new_board)
        st.session_state.score += points
        st.session_state.moves += 1
        
        # Update high score
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        
        # Check win/lose
        game_state = gamelogic.get_game_state(st.session_state.board)
        
        if game_state == "WON" and not st.session_state.won:
            st.session_state.won = True
            st.balloons()
            st.success(f"🎉 **You Won!** Reached 2048! Score: {st.session_state.score}")
        elif game_state == "LOST":
            st.session_state.game_over = True
            st.error(f"😢 **Game Over!** No more moves. Final Score: {st.session_state.score}")
        
        st.rerun()

# Control buttons
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("⬆️", key="up", use_container_width=True):
        make_move(gamelogic.move_up, "UP")

with col3:
    st.write("")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️", key="left", use_container_width=True):
        make_move(gamelogic.move_left, "LEFT")

with col2:
    if st.button("⬇️", key="down", use_container_width=True):
        make_move(gamelogic.move_down, "DOWN")

with col3:
    if st.button("➡️", key="right", use_container_width=True):
        make_move(gamelogic.move_right, "RIGHT")

# Game status
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.game_over:
    st.error("🛑 **Game Over!** No more moves possible.")
elif st.session_state.won:
    st.success("🏆 **You Won!** Keep playing for higher scores!")
else:
    st.info("💡 **Tip:** Keep your highest tile in a corner!")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #776e65; font-size: 14px; font-family: "Clear Sans", Arial, sans-serif;'>
    <p><strong>2048 Game</strong> - Functional Programming Implementation</p>
    <p>Built with Python & Streamlit | Deployed on AWS EC2</p>
</div>
""", unsafe_allow_html=True)