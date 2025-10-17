# 2048 Game

Web-based 2048 puzzle game built with Python and Streamlit.

## Quick Start
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Features

- Multiple board sizes (3×3 to 6×6)
- Keyboard controls (Arrow keys / WASD)
- Score tracking and move counter
- Clean UI matching original 2048

## Architecture

**streamlit_app.py** - UI layer (presentation, user input, styling)

**gamelogic.py** - Pure functional game logic (no side effects)

Complete separation of concerns - game logic works with any UI framework.

## Core Algorithm

One `slide_row()` function handles all four directions through matrix transformations:

- **Left**: `slide_row()`
- **Right**: Reverse → `slide_row()` → Reverse  
- **Up**: Transpose → `slide_row()` → Transpose
- **Down**: Transpose → Right → Transpose

Matrix operations eliminate code duplication.

## Tech Stack

Python • Streamlit • Functional Programming

## License

MIT