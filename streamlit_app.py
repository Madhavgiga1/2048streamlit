

import streamlit as st
import random
import copy


def init_board(size=4):
    """ empty board initialization and adding  two random tiles"""
    board = [[0] * size for _ in range(size)]
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board

def add_random_tile(board):
    """adding random tile (2 or 4) to an empty position"""
    empty = [(i, j) for i in range(len(board)) 
             for j in range(len(board)) if board[i][j] == 0]
    if not empty:
        return board
    
    i, j = random.choice(empty)
    new_board = copy.deepcopy(board)
    new_board[i][j] = 2 if random.random() < 0.9 else 4
    return new_board

def compress(row):
    """[0,2,0,0]->[2]"""
    return [x for x in row if x != 0]

def merge(row):
    """[[2,2,4]]->[[4,4]], we gt a new tuple containing new riw and score"""
    if len(row) < 2:
        return row, 0
    
    result = []
    score = 0
    i = 0
    
    while i < len(row):
        if i < len(row) - 1 and row[i] == row[i + 1]:
            value = row[i] * 2
            result.append(value)
            score += value
            i += 2
        else:
            result.append(row[i])
            i += 1
    
    return result, score

def move_row_left(row):
    """compress → merge → pad(add required zero to maintain matrix dimensions)"""
    compressed = compress(row)
    merged, score = merge(compressed)
    result = merged + [0] * (len(row) - len(merged))
    return result, score

def transpose(board):
    """simple matrix like transposition
        good way to think about it is like a 90-degree rotation before reversal
    """
    size = len(board)
    return [[board[j][i] for j in range(size)] for i in range(size)]

def reverse(board):
    """ each row reversal """
    return [row[::-1] for row in board]

def move_left(board):
    """Move all tiles left"""
    new_board = []
    total_score = 0
    
    for row in board:
        new_row, score = move_row_left(row)
        new_board.append(new_row)
        total_score += score
    
    return new_board, total_score

def move_right(board):
    """Move all tiles right"""
    board = reverse(board)
    board, score = move_left(board)
    return reverse(board), score

def move_up(board):
    """Move all tiles up"""
    board = transpose(board)
    board, score = move_left(board)
    return transpose(board), score

def move_down(board):
    """Move all tiles down"""
    board = transpose(board)
    board, score = move_right(board)
    return transpose(board), score

def board_changed(board1, board2):
    return board1 != board2
"""
    [[0,0,0,0],[0,0,0,0],[0,0,0,2],[8,2,0,4]]-> move down
     [[0,0,0,0],[0,0,0,0],[0,0,0,2],[8,2,0,4]] wont change so 

     new tile only spaws if board changes after move 
"""

def has_won(board, target=2048):
    """Check if target value reached"""
    return any(target in row for row in board)

def can_move(board):


    size = len(board)
    
    # empty cells check
    if any(0 in row for row in board):
        return True
    
    # horizontal merges check
    for row in board:
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                return True
    
    # vertical merges check
    for col in range(size):
        for row in range(size - 1):
            if board[row][col] == board[row + 1][col]:
                return True
    
    return False

def get_max_tile(board):
    """maximum tile value on board"""
    return max(max(row) for row in board)

def count_empty(board):
    """ empty cells counting """
    return sum(row.count(0) for row in board)

#  STREAMLIT UI

st.set_page_config(
    page_title="2048 Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #faf8ef;
    }
    
    .stButton>button {
        background-color: #8f7a66;
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #9f8a76;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    h1 {
        color: #776e65;
        text-align: center;
        font-size: 60px !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = init_board(4)
    st.session_state.score = 0
    st.session_state.size = 4
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.moves = 0
    st.session_state.best_score = 0

# Update best score
if st.session_state.score > st.session_state.best_score:
    st.session_state.best_score = st.session_state.score

# Main title
st.markdown("# 🎮 2048")

# Sidebar controls
with st.sidebar:
    st.markdown("## 🎛️ Controls")
    
    # New Game button
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.board = init_board(st.session_state.size)
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.won = False
        st.session_state.moves = 0
        st.rerun()
    
    # Board size selector
    st.markdown("### Board Size")
    new_size = st.selectbox(
        "Select size",
        options=[3, 4, 5, 6, 7, 8],
        index=[3, 4, 5, 6, 7, 8].index(st.session_state.size),
        label_visibility="collapsed"
    )
    
    if new_size != st.session_state.size:
        st.session_state.size = new_size
        st.session_state.board = init_board(new_size)
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.won = False
        st.session_state.moves = 0
        st.rerun()
    
    st.markdown("---")
    
    # Game stats
    st.markdown("### 📊 Statistics")
    st.metric("Current Score", st.session_state.score)
    st.metric("Best Score", st.session_state.best_score)
    st.metric("Moves", st.session_state.moves)
    st.metric("Max Tile", get_max_tile(st.session_state.board))
    st.metric("Empty Cells", count_empty(st.session_state.board))
    
    st.markdown("---")
    
    # How to play
    st.markdown("### 📖 How to Play")
    st.markdown("""
    1. Use the **arrow buttons** to move tiles
    2. Tiles with **same numbers** merge
    3. Reach **2048** to win!
    4. Game ends when no moves left
    """)
    
    st.markdown("---")
    
    # About
    st.markdown("### ℹ️ About")
    st.markdown("""
    **2048 Game**
    
    Built with Python & Streamlit
    
    Functional Programming Implementation
    """)

# Score display
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 Score", st.session_state.score)

with col2:
    st.metric("🏆 Best", st.session_state.best_score)

with col3:
    st.metric("🎲 Moves", st.session_state.moves)

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Color scheme
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

text_colors = {
    0: "#776e65",
    2: "#776e65",
    4: "#776e65"
}

for val in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]:
    text_colors[val] = "#f9f6f2"

# Calculate responsive tile size
tile_size = max(60, min(100, 400 // st.session_state.size))
font_size = max(18, min(48, 200 // st.session_state.size))

# Game board display - FIXED VERSION
st.markdown("### 🎮 Game Board")

# Create container for board
board_container = st.container()

with board_container:
    # Display each row
    for row_idx, row in enumerate(st.session_state.board):
        cols = st.columns(st.session_state.size)
        
        for col_idx, cell in enumerate(row):
            with cols[col_idx]:
                # Get colors
                bg_color = colors.get(cell, "#3c3a32")
                fg_color = text_colors.get(cell, "#f9f6f2")
                cell_text = str(cell) if cell != 0 else ""
                
                # Adjust font size
                if cell >= 1024:
                    display_font = int(font_size * 0.7)
                elif cell >= 128:
                    display_font = int(font_size * 0.85)
                else:
                    display_font = font_size
                
                # Display cell
                st.markdown(f"""
                    <div style='
                        background: {bg_color};
                        color: {fg_color};
                        width: {tile_size}px;
                        height: {tile_size}px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 8px;
                        font-size: {display_font}px;
                        font-weight: bold;
                        margin: 2px auto;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    '>
                        {cell_text}
                    </div>
                """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Move function
def make_move(move_func, direction):
    """Execute a move and update game state"""
    if st.session_state.game_over:
        st.warning("⚠️ Game Over! Click 'New Game' to play again.")
        return
    
    old_board = copy.deepcopy(st.session_state.board)
    new_board, points = move_func(st.session_state.board)
    
    if board_changed(old_board, new_board):
        # Valid move
        st.session_state.board = add_random_tile(new_board)
        st.session_state.score += points
        st.session_state.moves += 1
        
        # Check win
        if not st.session_state.won and has_won(st.session_state.board):
            st.session_state.won = True
            st.balloons()
            st.success(f"🎉 **You Won!** Reached 2048! Score: {st.session_state.score}")
        
        # Check lose
        elif not can_move(st.session_state.board):
            st.session_state.game_over = True
            st.error(f"😢 **Game Over!** No more moves. Final Score: {st.session_state.score}")
        
        # Move feedback
        elif points > 0:
            st.info(f"✨ Great! **+{points}** points")
        
        st.rerun()
    else:
        # Invalid move
        st.warning(f"⚠️ Can't move **{direction}**! Try another direction.")

# Control buttons
st.markdown("### 🎮 Controls")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("⬆️", key="up", use_container_width=True, help="Move Up"):
        make_move(move_up, "UP")

with col3:
    st.write("")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️", key="left", use_container_width=True, help="Move Left"):
        make_move(move_left, "LEFT")

with col2:
    if st.button("⬇️", key="down", use_container_width=True, help="Move Down"):
        make_move(move_down, "DOWN")

with col3:
    if st.button("➡️", key="right", use_container_width=True, help="Move Right"):
        make_move(move_right, "RIGHT")

# Game status
if st.session_state.game_over:
    st.error("🛑 **Game Over!** No more moves possible.")
elif st.session_state.won:
    st.success("🏆 **You Won!** Keep playing for higher scores!")
else:
    st.info("💡 **Tip:** Keep your highest tile in a corner!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #776e65; font-size: 12px;'>
    <p><strong>2048 Game</strong> - Built with Python & Streamlit</p>
    <p>Functional Programming Implementation</p>
</div>
""", unsafe_allow_html=True)