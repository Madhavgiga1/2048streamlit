import streamlit as st
import streamlit.components.v1 as components
import copy
import gamelogic


st.set_page_config(
    page_title="2048 Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    
    html, body {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    .main {
        overflow-y: hidden !important;
        padding-bottom: 0 !important;
    }
    
    .stApp {
        background: #eadaf0; 
        overflow: hidden !important;
    }
    
    .block-container {
        padding: 0.5rem 1rem 0.2rem 1rem !important;
        max-width: 450px !important;
    }
    
    
    .game-title {
        font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 38px;
        font-weight: bold;
        color: #776e65;
        text-align: center;
        margin: 5px 0 8px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    
    .score-container {
        background: #bbada0;  /* Brown - CHANGE THIS */
        border-radius: 5px;
        padding: 6px 10px;
        color: white;
    }
    
    .score-label {
        font-size: 9px;
        text-transform: uppercase;
        font-weight: bold;
        opacity: 0.8;
    }
    
    .score-value {
        font-size: 18px;
        font-weight: bold;
        margin-top: 2px;
    }
    
    
    .stButton > button {
        background-color: #8f7a66; 
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 6px;
        width: 100%;
        height: 42px;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background-color: #d35400;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
   
    .game-container {
        background: #fab1a0;
        border-radius: 6px;
        padding: 6px;
        margin: 6px auto;
        max-width: 100%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    
    .instructions {
        text-align: center;
        color: #776e65;
        font-size: 11px;
        margin: 6px 0;
        font-family: 'Clear Sans', Arial, sans-serif;
    }
    
    .key-hint {
        display: inline-block;
        background: #e17055;
        color: white;
        padding: 3px 6px;
        border-radius: 3px;
        margin: 0 2px;
        font-weight: bold;
        font-size: 10px;
    }
    
   
    .stAlert {
        border-radius: 5px;
        font-family: 'Clear Sans', Arial, sans-serif;
        padding: 6px;
        font-size: 12px;
        margin: 4px 0;
    }
    
    
    .stException {
        display: none !important;
    }
    
    
    [data-testid="column"] {
        padding: 2px !important;
    }
    
    .stSelectbox {
        margin: 0 !important;
    }
    
    .stSelectbox > div > div {
        font-size: 12px !important;
        padding: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

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

if 'board' not in st.session_state:
    st.session_state.board_size = 4
    st.session_state.board = gamelogic.initialize_board(4)
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.won = False


st.markdown('<div class="game-title">2048</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.2])

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
    # Board size selector
    new_size = st.selectbox(
        "Size",
        options=[3, 4, 5, 6],
        index=[3, 4, 5, 6].index(st.session_state.board_size),
        key="size_select",
        label_visibility="collapsed"
    )
    
    if new_size != st.session_state.board_size:
        st.session_state.board_size = new_size
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.session_state.board = gamelogic.initialize_board(new_size)
        st.session_state.score = 0
        st.session_state.moves = 0
        st.session_state.game_over = False
        st.session_state.won = False
        st.rerun()

with col5:
    if st.button("🔄 New Game", key="new_game", use_container_width=True):
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.session_state.board = gamelogic.initialize_board(st.session_state.board_size)
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

def get_tile_color(value):
    colors = {
        0: "#b9aa9a",      # Empty tile - beige
        2: "#41724F99",     
        4: "#ede0c8",     
        8: "#f2b179",      
        16: "#f59563",     
        32: "#f67c5f",    
        64: "#f65e3b",     
        128: "#edcf72",    
        256: "#edcc61",    
        512: "#edc850",    # Yellow
        1024: "#edc53f",   # Bright yellow
        2048: "#edc22e"    
    }
    return colors.get(value, "#4a52c0")


def get_text_color(value):
    return "#776e65" if value <= 4 else "#f9f6f2"

def get_font_size(value, board_size):
    if board_size == 3:
        if value < 100: return "42px"
        elif value < 1000: return "36px"
        elif value < 10000: return "30px"
        else: return "24px"
    elif board_size == 4:
        if value < 100: return "36px"
        elif value < 1000: return "30px"
        elif value < 10000: return "24px"
        else: return "20px"
    elif board_size == 5:
        if value < 100: return "28px"
        elif value < 1000: return "24px"
        elif value < 10000: return "20px"
        else: return "16px"
    else:  # 6
        if value < 100: return "24px"
        elif value < 1000: return "20px"
        elif value < 10000: return "16px"
        else: return "14px"

def get_tile_height(board_size):
    heights = {3: 85, 4: 65, 5: 52, 6: 43}
    return heights.get(board_size, 65)

st.markdown('<div class="game-container">', unsafe_allow_html=True)

tile_height = get_tile_height(st.session_state.board_size)

for row in st.session_state.board:
    cols = st.columns(st.session_state.board_size)
    for idx, value in enumerate(row):
        with cols[idx]:
            bg_color = get_tile_color(value)
            text_color = get_text_color(value)
            font_size = get_font_size(value, st.session_state.board_size)
            display_value = str(value) if value != 0 else ""
            
            st.markdown(f"""
                <div style='
                    background: {bg_color};
                    color: {text_color};
                    height: {tile_height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: {font_size};
                    font-weight: bold;
                    font-family: "Clear Sans", Arial, sans-serif;
                    border-radius: 4px;
                    margin: 3px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: all 0.15s ease-in-out;
                '>
                    {display_value}
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

def make_move(move_func, direction_name):
    if st.session_state.game_over:
        return False
    
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
        
        return True
    else:
        
        st.toast(f"⚠️ Can't move {direction_name}!", icon="⚠️")
        return False


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("⬆️", key="up", use_container_width=True):
        if make_move(gamelogic.move_up, "UP"):
            st.rerun()

with col3:
    st.write("")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️", key="left", use_container_width=True):
        if make_move(gamelogic.move_left, "LEFT"):
            st.rerun()

with col2:
    if st.button("⬇️", key="down", use_container_width=True):
        if make_move(gamelogic.move_down, "DOWN"):
            st.rerun()

with col3:
    if st.button("➡️", key="right", use_container_width=True):
        if make_move(gamelogic.move_right, "RIGHT"):
            st.rerun()


if st.session_state.game_over:
    st.error("🛑 Game Over! No more moves.")
elif st.session_state.won:
    st.success("🏆 You Won! Keep playing!")

st.markdown("""
<div style='text-align: center; color: #776e65; font-size: 20px; 
     font-family: "Clear Sans", Arial, sans-serif; margin-top: 6px;'>
    2048 Game - Exponent Energy Assignment
</div>
""", unsafe_allow_html=True)