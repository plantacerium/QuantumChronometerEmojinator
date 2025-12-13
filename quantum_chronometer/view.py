from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QApplication, QPushButton, QDialog, QGridLayout,
    QScrollArea, QTabWidget, QFrame, QComboBox
)
from PySide6.QtCore import Qt, QTimer, QPoint, Signal, QMimeData
from PySide6.QtGui import QDrag, QPixmap, QPainter, QFont, QColor, QPen

# --- Styling Constants ---
COLOR_BACKGROUND = "#0b0f19"
COLOR_GRID = "#1a233a"
COLOR_TEXT_MAIN = "#00f0ff"  # Cyan
COLOR_TEXT_DISTORTION = "#ff0055"  # Pink/Red
COLOR_TEXT_LOCAL_TIME = "#88ffaa"  # Green for per-unit time
COLOR_HEADER = "#00f0ff"
COLOR_BUTTON = "#1e3a5f"
COLOR_BUTTON_HOVER = "#2a5a8f"
FONT_FAMILY = "Consolas"

# Superposition symbol colors
SUPERPOSITION_COLORS = {
    '+': QColor(0, 255, 200, 60),   # Cyan/Green glow
    '*': QColor(180, 100, 255, 60), # Purple glow
    '~': QColor(255, 50, 100, 60),  # Red/Pink glow
}

# Categorized emoji collection for the browser
EMOJI_CATEGORIES = {
    "Quantum": ["⚛️", "🔮", "✨", "💫", "🌌", "🕳️", "⏰", "🔬", "🧬", "🧲", "⚡", "🌀",
                "🧠", "👁️", "🎲", "🌐", "🕰️", "🌟"],
    "Space": ["🚀", "🛸", "🌍", "🌙", "☀️", "⭐", "🌟", "💫", "🪐", "🌠", "☄️", "🔭",
             "🌕", "🌑", "🌔", "🌖", "🛠️", "🧑‍🚀"],
    "Symbols": ["➕", "✖️", "➖", "🔴", "🟢", "🔵", "🟡", "⚪", "⚫", "🟣", "🟠", "💠",
              "❤️", "💜", "💛", "💚", "♾️", "☢️"],
    "Objects": ["💡", "🖤", "🎯", "🔑", "💎", "🧊", "🔥", "💧", "🌊", "🍀", "🎲", "🎮",
              "💣", "🪄", "📿", "🧩", "🎁", "🔧"],
    "Animals": ["🐱", "🐶", "🦊", "🐻", "🐼", "🦁", "🐯", "🐸", "🦋", "🐝", "🐙", "🦑",
              "🦉", "🐲", "🦄", "🐳", "🦀", "🐍"],
    "Faces": ["😀", "😎", "🤔", "😱", "🥳", "😈", "👽", "🤖", "👻", "💀", "🎃", "😺",
            "🥸", "🙃", "🧐", "🙄", "🫣", "👋"],
    "Nature": ["🌸", "🌻", "🌿", "🌵", "🌲", "❄️", "🌈", "☁️", "⛈️", "🌪️", "🌫️", "🌞",
              "🌝", "⛅", "🌧️", "⚡", "🌋", "🏝️"],
    "Tech": ["💻", "📱", "🖥️", "💾", "💿", "📡", "🔌", "🪭", "📊", "📈", "⚙️", "🔗",
           "🧪", "🧱", "📦", "💬", "🔒", "🔓"],
}

# Emoji names for search (emoji -> list of keywords)
EMOJI_NAMES = {
    "⚛️": ["atom", "quantum", "physics", "science"],
    "🔮": ["crystal", "ball", "magic", "fortune"],
    "✨": ["sparkles", "stars", "magic", "shine"],
    "💫": ["dizzy", "star", "sparkle"],
    "🌌": ["milky", "way", "galaxy", "space"],
    "🕳️": ["hole", "black", "blackhole", "void"],
    "⏰": ["clock", "alarm", "time"],
    "🔬": ["microscope", "science", "lab"],
    "🧬": ["dna", "genetics", "biology"],
    "🧲": ["magnet", "magnetic"],
    "⚡": ["lightning", "bolt", "electric", "energy"],
    "🌀": ["cyclone", "spiral", "spin"],
    "🧠": ["brain", "mind", "think"],
    "👁️": ["eye", "see", "observe", "watch"],
    "🎲": ["dice", "game", "random", "chance"],
    "🌐": ["globe", "world", "earth", "meridian"],
    "🕰️": ["clock", "mantle", "time", "antique"],
    "🌟": ["star", "glow", "shine"],
    "🚀": ["rocket", "space", "launch"],
    "🛸": ["ufo", "alien", "spaceship"],
    "🌍": ["earth", "globe", "world", "planet"],
    "🌙": ["moon", "crescent", "night"],
    "☀️": ["sun", "sunny", "bright"],
    "⭐": ["star", "yellow"],
    "🪐": ["saturn", "planet", "ringed"],
    "🌠": ["shooting", "star", "meteor"],
    "☄️": ["comet", "meteor"],
    "🔭": ["telescope", "astronomy"],
    "🌕": ["moon", "full"],
    "🌑": ["moon", "new", "dark"],
    "💡": ["light", "bulb", "idea"],
    "🖤": ["heart", "black"],
    "🎯": ["target", "aim", "dart"],
    "🔑": ["key", "lock"],
    "💎": ["gem", "diamond", "jewel"],
    "🧊": ["ice", "cube", "cold"],
    "🔥": ["fire", "flame", "hot"],
    "💧": ["water", "drop", "droplet"],
    "🌊": ["wave", "ocean", "water"],
    "🐱": ["cat", "kitty", "feline"],
    "🐶": ["dog", "puppy", "canine"],
    "🦊": ["fox"],
    "🐻": ["bear"],
    "🐼": ["panda"],
    "🦁": ["lion"],
    "🐯": ["tiger"],
    "🐸": ["frog"],
    "🦋": ["butterfly"],
    "😀": ["smile", "happy", "face"],
    "😎": ["cool", "sunglasses"],
    "🤔": ["think", "thinking", "hmm"],
    "😱": ["scream", "fear", "scared"],
    "👽": ["alien", "et", "ufo"],
    "🤖": ["robot", "bot"],
    "👻": ["ghost", "boo"],
    "💀": ["skull", "death", "dead"],
    "🎃": ["pumpkin", "halloween", "jack"],
    "🌸": ["flower", "cherry", "blossom"],
    "🌈": ["rainbow"],
    "❄️": ["snow", "snowflake", "cold", "winter"],
    "💻": ["computer", "laptop", "pc"],
    "📱": ["phone", "mobile", "cell"],
    "⚙️": ["gear", "settings", "cog"],
    "🧪": ["test", "tube", "lab", "science"],
}

# Flattened list for search
ALL_EMOJIS = [e for cat in EMOJI_CATEGORIES.values() for e in cat]


class EmojiPickerDialog(QDialog):
    """Enhanced emoji picker with categories, search, and multi-emoji support."""
    
    emoji_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Quantum Unit")
        self.setModal(True)
        self.setMinimumSize(520, 550)  # Wider to fit all tabs
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLOR_BACKGROUND};
                border: 2px solid {COLOR_TEXT_MAIN};
                border-radius: 10px;
            }}
            QLabel {{
                color: white;
            }}
            QLineEdit {{
                color: white;
                background-color: {COLOR_GRID};
                border: 1px solid {COLOR_TEXT_MAIN};
                padding: 8px;
                font-size: 18px;
            }}
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                padding: 8px;
                font-size: 18px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
                border: 1px solid {COLOR_TEXT_MAIN};
            }}
            QTabWidget::pane {{
                border: 1px solid {COLOR_GRID};
                background-color: {COLOR_BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: {COLOR_BUTTON};
                color: white;
                padding: 8px 12px;
                border-radius: 5px 5px 0 0;
            }}
            QTabBar::tab:selected {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Input field with current selection
        input_label = QLabel("Your selection (click emojis to add):")
        self.emoji_input = QLineEdit()
        self.emoji_input.setPlaceholderText("Type or click emojis below...")
        self.emoji_input.setMinimumHeight(40)
        layout.addWidget(input_label)
        layout.addWidget(self.emoji_input)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 18px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search emojis...")
        self.search_input.textChanged.connect(self._filter_emojis)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Tab widget for categories
        self.tab_widget = QTabWidget()
        self._build_category_tabs()
        layout.addWidget(self.tab_widget, 1)
        
        # Button row
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(lambda: self.emoji_input.clear())
        button_layout.addWidget(clear_btn)
        
        confirm_btn = QPushButton("Add Unit")
        confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_TEXT_MAIN};
                color: {COLOR_BACKGROUND};
                font-weight: bold;
            }}
        """)
        confirm_btn.clicked.connect(self._confirm)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)

    def _build_category_tabs(self):
        """Build tabs for each emoji category."""
        for category, emojis in EMOJI_CATEGORIES.items():
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            container = QWidget()
            grid = QGridLayout(container)
            grid.setSpacing(5)
            
            row, col = 0, 0
            for emoji in emojis:
                btn = self._create_emoji_button(emoji)
                grid.addWidget(btn, row, col)
                col += 1
                if col >= 6:
                    col = 0
                    row += 1
            
            scroll.setWidget(container)
            self.tab_widget.addTab(scroll, category)

    def _create_emoji_button(self, emoji):
        """Create a button for an emoji."""
        btn = QPushButton(emoji)
        btn.setFixedSize(55, 55)
        btn.setFont(QFont("Segoe UI Emoji", 22))
        btn.clicked.connect(lambda checked, e=emoji: self._append_emoji(e))
        return btn

    def _append_emoji(self, emoji):
        """Append an emoji to the current selection."""
        current = self.emoji_input.text()
        self.emoji_input.setText(current + emoji)
        
    def _filter_emojis(self, search_text):
        """Filter emojis based on search using keyword matching."""
        if not search_text:
            self._rebuild_tabs()
            return
        
        search_lower = search_text.lower().strip()
        matches = []
        
        # Search by keyword in EMOJI_NAMES
        for emoji, keywords in EMOJI_NAMES.items():
            if any(search_lower in kw for kw in keywords):
                if emoji not in matches:
                    matches.append(emoji)
        
        # Also search category names
        for cat_name, cat_emojis in EMOJI_CATEGORIES.items():
            if search_lower in cat_name.lower():
                for e in cat_emojis:
                    if e not in matches:
                        matches.append(e)
        
        if not matches:
            # No matches found, show message
            self.tab_widget.clear()
            no_results = QLabel(f"No emojis found for '{search_text}'")
            no_results.setStyleSheet("color: white; padding: 20px;")
            no_results.setAlignment(Qt.AlignCenter)
            self.tab_widget.addTab(no_results, "No Results")
            return
        
        # Show matches
        self.tab_widget.clear()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(5)
        
        row, col = 0, 0
        for emoji in matches:
            btn = self._create_emoji_button(emoji)
            grid.addWidget(btn, row, col)
            col += 1
            if col >= 6:
                col = 0
                row += 1
        
        scroll.setWidget(container)
        self.tab_widget.addTab(scroll, f"Found ({len(matches)})")

    def _rebuild_tabs(self):
        """Rebuild original category tabs."""
        self.tab_widget.clear()
        self._build_category_tabs()
        
    def _confirm(self):
        text = self.emoji_input.text().strip()
        if text:
            self.emoji_selected.emit(text)
            self.accept()




class DraggableUnitWidget(QWidget):
    """
    Visual representation of a quantum unit with its own local time display.
    Supports multi-emoji text and colored glow based on superposition.
    """
    unit_moved = Signal(str, int, int)  # unit_id, new_x, new_y
    
    def __init__(self, unit_id, text, superposition_symbol='+', display_width=60, parent=None):
        super().__init__(parent)
        self.unit_id = unit_id
        self.emoji_text = text
        self.superposition_symbol = superposition_symbol
        self.local_time_str = "00:00:00"
        
        # Dynamic sizing based on emoji count
        self.orb_width = max(60, display_width)
        self.widget_width = max(110, self.orb_width) # Ensure at least 110px for time text
        self.setFixedSize(self.widget_width, 80)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setToolTip(f"Superposition: {superposition_symbol}")
        
        self.drag_start_position = None
        self.show_symbol = True

    def set_show_symbol(self, show):
        self.show_symbol = show
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get glow color based on superposition symbol
        glow_color = SUPERPOSITION_COLORS.get(self.superposition_symbol, QColor(0, 240, 255, 30))
        
        # Draw glow/background ellipse
        painter.setBrush(glow_color)
        painter.setPen(Qt.NoPen)
        
        # Center the orb in the widget
        orb_x = (self.width() - self.orb_width) // 2
        painter.drawEllipse(orb_x, 5, self.orb_width, 50)
        
        # Draw emoji
        painter.setFont(QFont("Segoe UI Emoji", 20))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect().adjusted(0, 5, 0, -20), Qt.AlignCenter, self.emoji_text)
        
        # Draw local time below
        painter.setFont(QFont(FONT_FAMILY, 8))
        painter.setPen(QColor(COLOR_TEXT_LOCAL_TIME))
        painter.drawText(self.rect().adjusted(0, 55, 0, 0), Qt.AlignHCenter | Qt.AlignTop, self.local_time_str)
        
        # Draw Superposition Symbol (Top Right)
        if self.show_symbol:
            # Color logic
            symbol_color = QColor(255, 255, 255, 180) # Default
            if self.superposition_symbol == '+':
                symbol_color = QColor(0, 255, 255) # Cyan
            elif self.superposition_symbol == '*':
                symbol_color = QColor(200, 100, 255) # Purple
            elif self.superposition_symbol == '~':
                symbol_color = QColor(255, 70, 70) # Red

            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.setPen(symbol_color)
            painter.drawText(self.rect().adjusted(0, 5, -8, 0), Qt.AlignRight | Qt.AlignTop, self.superposition_symbol)
        
    def update_local_time(self, time_str):
        self.local_time_str = time_str
        self.setToolTip(f"Superposition: {self.superposition_symbol}\nLocal Time: {time_str}")
        self.update()  # Trigger repaint

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_position is None:
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        # Include ID in mime data for move operations
        mime_data.setText(f"MOVE:{self.unit_id}:{self.emoji_text}")
        drag.setMimeData(mime_data)
        
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(30, 40))
        
        drag.exec(Qt.MoveAction)


class QuantumWhiteboardWidget(QWidget):
    """The main display area with the grid and proximity lines."""
    
    unit_dropped = Signal(str, QPoint)  # For new units (text, position)
    unit_moved = Signal(str, int, int)  # For existing units (unit_id, x, y)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {COLOR_BACKGROUND}; border: 1px solid {COLOR_GRID}; border-radius: 10px;")
        self.unit_widgets = {}  # unit_id -> DraggableUnitWidget
        self.proximity_pairs = []  # List of ((x1,y1), (x2,y2)) for drawing lines
        self.grid_type = "Square"  # Square, Circle, Hexagon
        self.show_symbols = True

    def toggle_symbols(self, show):
        self.show_symbols = show
        for widget in self.unit_widgets.values():
            widget.set_show_symbol(show)

    def set_grid_type(self, grid_type):
        self.grid_type = grid_type
        self.update()

    def set_proximity_pairs(self, pairs):
        """Set the pairs of units to draw lines between."""
        self.proximity_pairs = pairs
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(COLOR_BACKGROUND))
        
        # Draw Grid
        pen = QPen(QColor(COLOR_GRID))
        pen.setWidth(1)
        painter.setPen(pen)
        
        grid_size = 40
        
        if self.grid_type == "Square":
            for x in range(0, self.width(), grid_size):
                painter.drawLine(x, 0, x, self.height())
            for y in range(0, self.height(), grid_size):
                painter.drawLine(0, y, self.width(), y)
                
        elif self.grid_type == "Circle":
            # Draw lines connecting centers first
            pen_lines = QPen(QColor(COLOR_GRID))
            pen_lines.setWidth(1)
            pen_lines.setStyle(Qt.DotLine)
            painter.setPen(pen_lines)
            
            for x in range(0, self.width(), grid_size):
                painter.drawLine(x, 0, x, self.height())
            for y in range(0, self.height(), grid_size):
                painter.drawLine(0, y, self.width(), y)
                
            # Draw dots at intersections
            painter.setBrush(QColor(COLOR_GRID))
            painter.setPen(Qt.NoPen)
            for x in range(0, self.width(), grid_size):
                for y in range(0, self.height(), grid_size):
                    painter.drawEllipse(x-2, y-2, 4, 4)
                    
        elif self.grid_type == "Hexagon":
            # Proper honeycomb grid
            import math
            size = 30  # Radius of hexagon
            w = math.sqrt(3) * size
            h = 2 * size
            horiz_dist = w
            vert_dist = 3/4 * h
            
            rows = int(self.height() / vert_dist) + 2
            cols = int(self.width() / horiz_dist) + 2
            
            hex_pen = QPen(QColor(COLOR_GRID))
            hex_pen.setWidth(1)
            painter.setPen(hex_pen)
            
            for r in range(rows):
                for c in range(cols):
                    x_offset = (r % 2) * (w / 2)
                    cx = c * horiz_dist + x_offset
                    cy = r * vert_dist
                    
                    # Draw bottom half of hex to avoid double drawing
                    # Points: (0, size), (w/2, size/2), (w/2, -size/2), (0, -size), (-w/2, -size/2), (-w/2, size/2)
                    # We just need to draw 3 lines to tile the plane if we do it for every center:
                    # Center to bottom-right, center to bottom, center to bottom-left?
                    # Simpler to just draw the simplified pattern:
                    #   / \
                    #  |   |
                    #   \ /
                    
                    # Calculate vertices
                    x0 = cx
                    y0 = cy - size
                    x1 = cx + w/2
                    y1 = cy - size/2
                    x2 = cx + w/2
                    y2 = cy + size/2
                    x3 = cx
                    y3 = cy + size
                    x4 = cx - w/2
                    y4 = cy + size/2
                    x5 = cx - w/2
                    y5 = cy - size/2
                    
                    # Draw hexagon
                    points = [QPoint(int(x0), int(y0)), QPoint(int(x1), int(y1)), 
                              QPoint(int(x2), int(y2)), QPoint(int(x3), int(y3)), 
                              QPoint(int(x4), int(y4)), QPoint(int(x5), int(y5))]
                    
                    for i in range(6):
                        p1 = points[i]
                        p2 = points[(i + 1) % 6]
                        painter.drawLine(p1, p2)
        
        # Draw Proximity Lines
        if self.proximity_pairs:
            line_pen = QPen(QColor(100, 200, 255, 80))
            line_pen.setWidth(2)
            line_pen.setStyle(Qt.DashLine)
            painter.setPen(line_pen)
            
            for (x1, y1), (x2, y2) in self.proximity_pairs:
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        text = event.mimeData().text()
        position = event.position().toPoint()
        
        if text.startswith("MOVE:"):
            parts = text.split(":")
            unit_id = parts[1]
            self.unit_moved.emit(unit_id, position.x(), position.y())
            
            if unit_id in self.unit_widgets:
                widget = self.unit_widgets[unit_id]
                widget.move(position.x() - widget.width()//2, position.y() - 40)
        else:
            self.unit_dropped.emit(text, position)
        
        event.accept()

    def add_unit_widget(self, unit_id, text, x, y, superposition_symbol='+', display_width=60):
        widget = DraggableUnitWidget(unit_id, text, superposition_symbol, display_width, self)
        widget.move(x - widget.width()//2, y - 40)
        widget.set_show_symbol(self.show_symbols)
        widget.show()
        self.unit_widgets[unit_id] = widget
        return widget

    def update_unit_time(self, unit_id, time_str):
        if unit_id in self.unit_widgets:
            self.unit_widgets[unit_id].update_local_time(time_str)


class QuantumView(QMainWindow):
    """Main Application Window."""
    
    wave_collapse_triggered = Signal()  # Mouse moved = observation
    add_emoji_clicked = Signal()
    observe_toggled = Signal(bool)  # Continuous observation mode
    mouse_observation = Signal(int, int)  # Mouse position for proximity
    save_clicked = Signal()
    load_clicked = Signal()
    screenshot_clicked = Signal()
    reset_clicked = Signal()
    grid_changed = Signal(str)
    symbols_toggled = Signal(bool)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Quantum Chronometer")
        self.resize(1000, 800)
        
        # Ensure main window background is dark
        self.setStyleSheet(f"background-color: {COLOR_BACKGROUND};")
        
        # Central Widget
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {COLOR_BACKGROUND};")
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 1. Time Display
        self.time_label = QLabel("00:00:00.000")
        self.time_label.setFont(QFont(FONT_FAMILY, 60, QFont.Bold))
        self.time_label.setStyleSheet(f"color: {COLOR_TEXT_MAIN};")
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # 2. Distortion Status
        self.status_label = QLabel("Quantum Distortion: 0.0000 Magnified t_P")
        self.status_label.setFont(QFont(FONT_FAMILY, 12))
        self.status_label.setStyleSheet(f"color: {COLOR_TEXT_DISTORTION};")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 3. Header
        header = QLabel("Quantum Whiteboard")
        header.setFont(QFont(FONT_FAMILY, 14))
        header.setStyleSheet(f"color: {COLOR_HEADER}; margin-top: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # 4. Whiteboard
        self.whiteboard = QuantumWhiteboardWidget()
        layout.addWidget(self.whiteboard, 1)

        # 5. Bottom Bar: Add Button + Observe Button
        bottom_bar = QWidget()
        bottom_bar.setStyleSheet(f"background-color: #151a25; border-radius: 5px; padding: 5px;")
        bottom_layout = QHBoxLayout(bottom_bar)
        
        # Add Emoji Button
        self.add_button = QPushButton("➕")
        self.add_button.setFont(QFont("Segoe UI Emoji", 16))
        self.add_button.setFixedSize(50, 40)
        self.add_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: {COLOR_TEXT_MAIN};
                border: 1px solid {COLOR_TEXT_MAIN};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.add_button.setToolTip("Add new quantum unit")
        self.add_button.clicked.connect(self.add_emoji_clicked.emit)
        bottom_layout.addWidget(self.add_button)

        # Network Status
        self.net_label = QLabel("📡 Network: ON")
        self.net_label.setFont(QFont(FONT_FAMILY, 9))
        self.net_label.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; margin-left: 10px;")
        self.net_label.setToolTip("Broadcasting on UDP Port 50055")
        bottom_layout.addWidget(self.net_label)
        
        # Spacer
        bottom_layout.addStretch(1)
        
        # Observe Toggle Button
        self.observe_button = QPushButton("Observe")
        self.observe_button.setFont(QFont(FONT_FAMILY, 12))
        self.observe_button.setCheckable(True)
        self.observe_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                padding: 8px 15px;
                border-radius: 5px;
            }}
            QPushButton:checked {{
                background-color: {COLOR_TEXT_MAIN};
                color: {COLOR_BACKGROUND};
                border: 1px solid {COLOR_TEXT_MAIN};
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.observe_button.setToolTip("Toggle continuous observation (time flows)")
        self.observe_button.toggled.connect(self.observe_toggled.emit)
        bottom_layout.addWidget(self.observe_button)
        
        # Save Button
        self.save_button = QPushButton("💾")
        self.save_button.setFont(QFont("Segoe UI Emoji", 14))
        self.save_button.setFixedSize(40, 40)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.save_button.setToolTip("Save state to file")
        self.save_button.clicked.connect(self.save_clicked.emit)
        bottom_layout.addWidget(self.save_button)
        
        # Load Button
        self.load_button = QPushButton("📂")
        self.load_button.setFont(QFont("Segoe UI Emoji", 14))
        self.load_button.setFixedSize(40, 40)
        self.load_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.load_button.setToolTip("Load state from file")
        self.load_button.clicked.connect(self.load_clicked.emit)
        bottom_layout.addWidget(self.load_button)
        
        # Screenshot Button
        self.screenshot_button = QPushButton("📷")
        self.screenshot_button.setFont(QFont("Segoe UI Emoji", 14))
        self.screenshot_button.setFixedSize(40, 40)
        self.screenshot_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.screenshot_button.setToolTip("Save screenshot")
        self.screenshot_button.clicked.connect(self.screenshot_clicked.emit)
        bottom_layout.addWidget(self.screenshot_button)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {COLOR_GRID};")
        bottom_layout.addWidget(line)
        
        # Grid Selector
        self.grid_combo = QComboBox()
        self.grid_combo.addItems(["Square", "Circle", "Hexagon"])
        self.grid_combo.setFont(QFont(FONT_FAMILY, 10))
        self.grid_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
        """)
        self.grid_combo.setToolTip("Change spacetime grid topology")
        self.grid_combo.currentTextChanged.connect(self.grid_changed.emit)
        bottom_layout.addWidget(self.grid_combo)

        # Symbols Toggle
        self.symbols_button = QPushButton("Symbols: ON")
        self.symbols_button.setFont(QFont(FONT_FAMILY, 10))
        self.symbols_button.setCheckable(True)
        self.symbols_button.setChecked(True)
        self.symbols_button.setFixedWidth(100)
        self.symbols_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:checked {{
                background-color: {COLOR_TEXT_MAIN};
                color: {COLOR_BACKGROUND};
            }}
        """)
        self.symbols_button.toggled.connect(self.handle_symbols_toggled)
        bottom_layout.addWidget(self.symbols_button)
        
        # Reset Button
        self.reset_button = QPushButton("↻")
        self.reset_button.setFont(QFont("Segoe UI Emoji", 14))
        self.reset_button.setFixedSize(40, 40)
        self.reset_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON};
                color: {COLOR_TEXT_DISTORTION};
                border: 1px solid {COLOR_GRID};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_HOVER};
            }}
        """)
        self.reset_button.setToolTip("Reset Spacetime")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        bottom_layout.addWidget(self.reset_button)
        
        layout.addWidget(bottom_bar)
        
        # Set global stylesheet for standard dialogs to fix dark mode text visibility
        self.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLOR_BACKGROUND};
                color: white;
            }}
            QMessageBox QLabel {{
                color: white;
            }}
            QMessageBox QPushButton {{
                background-color: {COLOR_BUTTON};
                color: white;
                border: 1px solid {COLOR_TEXT_MAIN};
                padding: 5px 15px;
                border-radius: 3px;
            }}
        """)
        self.setCentralWidget(central_widget)
        
        # Track mouse for proximity observation
        self.setMouseTracking(True)
        central_widget.setMouseTracking(True)
        self.whiteboard.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        # Emit mouse position for proximity-based observation
        global_pos = event.globalPosition().toPoint()
        whiteboard_pos = self.whiteboard.mapFromGlobal(global_pos)
        self.mouse_observation.emit(whiteboard_pos.x(), whiteboard_pos.y())
        self.wave_collapse_triggered.emit()
        super().mouseMoveEvent(event)

    def update_time_display(self, time_str, super_marker):
        self.time_label.setText(f"{time_str} {super_marker}")

    def update_distortion_display(self, distortion):
        self.status_label.setText(f"Quantum Distortion: {distortion:+.4f} Magnified t_P")

    def add_visual_unit(self, unit_id, text, x, y, superposition_symbol='+', display_width=60):
        return self.whiteboard.add_unit_widget(unit_id, text, x, y, superposition_symbol, display_width)

    def update_unit_local_time(self, unit_id, time_str):
        self.whiteboard.update_unit_time(unit_id, time_str)

    def set_proximity_pairs(self, pairs):
        """Update the proximity line data on the whiteboard."""
        self.whiteboard.set_proximity_pairs(pairs)

    def handle_symbols_toggled(self, checked):
        self.symbols_button.setText(f"Symbols: {'ON' if checked else 'OFF'}")
        self.whiteboard.toggle_symbols(checked)

