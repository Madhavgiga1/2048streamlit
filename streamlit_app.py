import streamlit as st
import random
import copy

# ============================================
# FUNCTIONAL GAME LOGIC (Pure Functions)
# ============================================

def initialize_board(size=4):
    """Create empty board and add 2 random tiles"""
    board = [[0] * size for _ in range(size)]
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board

def add_random_tile(board):
    """Add a random 2 or 4 to an empty cell"""
    empty_cells = [(i, j) for i in range(len(board)) 
                   for j in range(len(board[0])) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board

def slide_row(row):
    """Slide and merge a single row to the left"""
    # Remove zeros
    non_zero = [num for num in row if num != 0]
    
    # Merge adjacent equal numbers
    merged = []
    score = 0
    i = 0
    while i < len(non_zero):
        if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
            merged.append(non_zero[i] * 2)
            score += non_zero[i] * 2
            i += 2
        else:
            merged.append(non_zero[i])
            i += 1
    
    # Pad with zeros
    merged += [0] * (len(row) - len(merged))
    return merged, score

def move_left(board):
    """Move all tiles left"""
    new_board = []
    total_score = 0
    for row in board:
        new_row, score = slide_row(row)
        new_board.append(new_row)
        total_score += score
    return new_board, total_score

def move_right(board):
    """Move all tiles right"""
    new_board = []
    total_score = 0
    for row in board:
        reversed_row = row[::-1]
        new_row, score = slide_row(reversed_row)
        new_board.append(new_row[::-1])
        total_score += score
    return new_board, total_score

def transpose(board):
    """Transpose the board"""
    return [list(row) for row in zip(*board)]

def move_up(board):
    """Move all tiles up"""
    transposed = transpose(board)
    moved, score = move_left(transposed)
    return transpose(moved), score

def move_down(board):
    """Move all tiles down"""
    transposed = transpose(board)
    moved, score = move_right(transposed)
    return transpose(moved), score

def board_changed(old_board, new_board):
    """Check if board changed after move"""
    return old_board != new_board

def can_move(board):
    """Check if any move is possible"""
    size = len(board)
    
    # Check for empty cells
    for row in board:
        if 0 in row:
            return True
    
    # Check for adjacent equal numbers horizontally
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] == board[i][j + 1]:
                return True
    
    # Check for adjacent equal numbers vertically
    for i in range(size - 1):
        for j in range(size):
            if board[i][j] == board[i + 1][j]:
                return True
    
    return False

def has_won(board):
    """Check if 2048 tile exists"""
    for row in board:
        if 2048 in row:
            return True
    return False

# ============================================
# STREAMLIT UI SETUP
# ============================================

st.set_page_config(page_title="2048 Game", page_icon="🎮", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'board' not in st.session_state:
    st.session_state.board = initialize_board(4)
    st.session_state.score = 0
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.won = False

# ============================================
# HEADER
# ============================================

st.title("🎮 2048 Game")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    st.metric("Moves", st.session_state.moves)
with col3:
    if st.button("🔄 New Game"):
        st.session_state.board = initialize_board(4)
        st.session_state.score = 0
        st.session_state.moves = 0
        st.session_state.game_over = False
        st.session_state.won = False
        st.rerun()

st.markdown("---")

# ============================================
# GAME BOARD DISPLAY
# ============================================

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
        2048: "#edc22e"
    }
    return colors.get(value, "#3c3a32")

def get_text_color(value):
    """Get text color based on tile value"""
    return "#776e65" if value in [2, 4] else "#f9f6f2"

# Display board using columns
st.markdown("### Game Board")
for row in st.session_state.board:
    cols = st.columns(4)
    for idx, value in enumerate(row):
        with cols[idx]:
            bg_color = get_tile_color(value)
            text_color = get_text_color(value)
            display_value = str(value) if value != 0 else ""
            
            st.markdown(f"""
                <div style='
                    background-color: {bg_color};
                    color: {text_color};
                    height: 100px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 32px;
                    font-weight: bold;
                    border-radius: 8px;
                    margin: 4px;
                '>
                    {display_value}
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# MOVE FUNCTION
# ============================================

def make_move(move_func, direction):
    """Execute a move and update game state"""
    if st.session_state.game_over:
        st.warning("Game Over! Click 'New Game' to start again.")
        return
    
    old_board = copy.deepcopy(st.session_state.board)
    new_board, points = move_func(st.session_state.board)
    
    if board_changed(old_board, new_board):
        # Valid move - board actually changed
        st.session_state.board = add_random_tile(new_board)
        st.session_state.score += points
        st.session_state.moves += 1
        
        # Check win condition
        if not st.session_state.won and has_won(st.session_state.board):
            st.session_state.won = True
            st.balloons()
            st.success(f"🎉 **You Won!** Reached 2048! Score: {st.session_state.score}")
        
        # Check lose condition
        elif not can_move(st.session_state.board):
            st.session_state.game_over = True
            st.error(f"😢 **Game Over!** No more moves. Final Score: {st.session_state.score}")
        
        # Move feedback
        elif points > 0:
            st.info(f"✨ Great! **+{points}** points")
        
        st.rerun()
    else:
        # Invalid move - board didn't change
        st.warning(f"⚠️ Can't move **{direction}**! Try another direction.")

# ============================================
# CONTROLS
# ============================================

st.markdown("### 🎮 Controls")
st.markdown("*Use arrow keys ↑↓←→ or click buttons*")

# Control buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("⬆️ UP", key="up", use_container_width=True):
        make_move(move_up, "UP")

with col3:
    st.write("")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️ LEFT", key="left", use_container_width=True):
        make_move(move_left, "LEFT")

with col2:
    if st.button("⬇️ DOWN", key="down", use_container_width=True):
        make_move(move_down, "DOWN")

with col3:
    if st.button("➡️ RIGHT", key="right", use_container_width=True):
        make_move(move_right, "RIGHT")

# ============================================
# GAME STATUS
# ============================================

st.markdown("---")

if st.session_state.game_over:
    st.error("🛑 **Game Over!** No more moves possible.")
elif st.session_state.won:
    st.success("🏆 **You Won!** Keep playing for higher scores!")
else:
    st.info("💡 **Tip:** Keep your highest tile in a corner!")


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #776e65; font-size: 14px;'>
    <p><strong>2048 Game</strong> - Built with Python & Streamlit</p>
    <p>Functional Programming Implementation</p>
</div>
""", unsafe_allow_html=True)