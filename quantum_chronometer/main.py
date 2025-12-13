import sys
import time
import math
import json
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer

from .model import QuantumModel, QuantumUnit, SUPERPOSITION_SYMBOLS
from .network import QuantumNetworkManager


class QuantumController:
    """
    Controller that connects the Model and View.
    Implements observation-based time: time only flows during observation.
    """
    
    def __init__(self):
        self.model = QuantumModel()
        
        # Observation state
        self.is_observing = False  # Continuous observation via button
        self.observation_intensity = 0.0  # 0-1, based on mouse proximity
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_observation_time = time.time()
        self.accumulated_time = 0.0  # Total "observed" time
        
        # Import View
        from .view import QuantumView, EmojiPickerDialog
        self.EmojiPickerDialog = EmojiPickerDialog
        
        self.view = QuantumView(self)
        
        # Connect Signals
        self.view.whiteboard.unit_dropped.connect(self.handle_new_unit_drop)
        self.view.whiteboard.unit_moved.connect(self.handle_unit_move)
        self.view.wave_collapse_triggered.connect(self.handle_wave_collapse)
        self.view.add_emoji_clicked.connect(self.open_emoji_picker)
        self.view.observe_toggled.connect(self.handle_observe_toggle)
        self.view.mouse_observation.connect(self.handle_mouse_observation)
        self.view.save_clicked.connect(self.handle_save)
        self.view.load_clicked.connect(self.handle_load)
        self.view.screenshot_clicked.connect(self.handle_screenshot)
        self.view.reset_clicked.connect(self.handle_reset)
        self.view.grid_changed.connect(self.handle_grid_change)
        
        # Network Manager (Phase 5.1)
        self.network = QuantumNetworkManager()
        self.network.remote_distortion_received.connect(self.handle_remote_distortion)
        self.network.start()
        
        # Timer for main update loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(50)  # 20 FPS

        self.view.show()

    def open_emoji_picker(self):
        """Open the emoji picker dialog."""
        dialog = self.EmojiPickerDialog(self.view)
        dialog.emoji_selected.connect(self.spawn_unit_at_center)
        dialog.exec()

    def spawn_unit_at_center(self, emoji_text):
        """Spawn a new unit at the center of the whiteboard."""
        center_x = self.view.whiteboard.width() // 2
        center_y = self.view.whiteboard.height() // 2
        
        unit = QuantumUnit(emoji_text, center_x, center_y)
        self.model.add_unit(unit)
        
        self.view.add_visual_unit(
            unit.id, emoji_text, center_x, center_y,
            unit.superposition_symbol, unit.display_width
        )

    def handle_new_unit_drop(self, text, position):
        """Handle a new unit being dropped."""
        unit = QuantumUnit(text, position.x(), position.y())
        self.model.add_unit(unit)
        self.view.add_visual_unit(
            unit.id, text, position.x(), position.y(),
            unit.superposition_symbol, unit.display_width
        )

    def handle_unit_move(self, unit_id, new_x, new_y):
        """Handle an existing unit being moved."""
        self.model.update_unit_position(unit_id, new_x, new_y)

    def handle_wave_collapse(self):
        """Mouse movement triggers observation (not collapse in this mode)."""
        # In observation mode, mouse movement IS observation
        pass

    def handle_observe_toggle(self, is_checked):
        """Toggle continuous observation mode."""
        self.is_observing = is_checked
        if is_checked:
            self.last_observation_time = time.time()

    def handle_mouse_observation(self, x, y):
        """Handle mouse position for proximity-based observation intensity."""
        self.mouse_x = x
        self.mouse_y = y
        
        # Calculate observation intensity based on proximity to any unit
        max_intensity = 0.0
        for unit in self.model.units:
            distance = math.sqrt((x - unit.x)**2 + (y - unit.y)**2)
            # Closer = higher intensity (max at 0, min at 200+)
            if distance < 200:
                intensity = 1.0 - (distance / 200.0)
                max_intensity = max(max_intensity, intensity)
        
        # Always some base observation from mouse movement
        self.observation_intensity = max(0.1, max_intensity)
        self.last_observation_time = time.time()

    def update_loop(self):
        """Main update loop - observation-based time mechanics."""
        current_real_time = time.time()
        
        # Determine if time should flow
        is_observing_time = False
        
        # 1. Continuous Observation
        if self.is_observing:
            is_observing_time = True
            
        # 2. Mouse Proximity Observation
        # If mouse moved recently (last 0.2s)
        if time.time() - self.last_observation_time < 0.2:
            is_observing_time = True
            
        # dt is the time step for the model update
        dt = 0.05 # Corresponds to the QTimer interval (50ms)
        
        # Update Model
        self.model.update_unit_times(
            dt, 
            is_observing=is_observing_time,
            mouse_pos=(self.mouse_x, self.mouse_y)
        )
        
        # Broadast local distortion (Phase 5.1)
        # Only broadcast if significant to reduce traffic
        if abs(self.model.time_distortion) > 0.0001:
            self.network.broadcast_distortion(self.model.time_distortion)
        
        # Update View
        if is_observing_time:
            self.accumulated_time += dt
            
        # Update Global Time Display
        magnified_time = self.accumulated_time + self.model.time_distortion
        distortion = self.model.time_distortion
        
        h = int(magnified_time // 3600)
        m = int((magnified_time % 3600) // 60)
        s = magnified_time % 60
        time_str = f"{h:02d}:{m:02d}:{s:06.3f}"
        
        # Superposition Marker
        if distortion > 0.5:
            marker = SUPERPOSITION_SYMBOLS[0]
        elif distortion < -0.5:
            marker = SUPERPOSITION_SYMBOLS[2]
        else:
            marker = SUPERPOSITION_SYMBOLS[1]
            
        self.view.update_time_display(time_str, marker)
        self.view.update_distortion_display(distortion)
        
        # Update Per-Unit Local Times
        for unit in self.model.units:
            observed_time = self.model.start_time + self.accumulated_time
            local_time = unit.get_local_magnified_time(observed_time)
            local_s = local_time % 60
            local_m = int((local_time % 3600) // 60)
            local_h = int(local_time // 3600)
            local_str = f"{local_h:02d}:{local_m:02d}:{local_s:05.2f}"
            self.view.update_unit_local_time(unit.id, local_str)
        
        # Update Proximity Lines
        proximity_pairs = self.model.get_proximity_pairs(threshold=100)
        line_coords = [((u1.x, u1.y), (u2.x, u2.y)) for u1, u2 in proximity_pairs]
        self.view.set_proximity_pairs(line_coords)

    def handle_save(self):
        """Save current state to a JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Save Quantum State",
            "quantum_state.json",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                state = self.model.save_state(self.accumulated_time)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self.view, "Saved", f"State saved to {file_path}")
            except Exception as e:
                QMessageBox.warning(self.view, "Error", f"Failed to save: {e}")

    def handle_load(self):
        """Load state from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Load Quantum State",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Clear current view
                self.view.whiteboard.unit_widgets.clear()
                # Clear whiteboard widgets
                for child in self.view.whiteboard.children():
                    if hasattr(child, 'unit_id'):
                        child.deleteLater()
                
                # Load state into model
                self.model.load_state(state)
                self.accumulated_time = state.get("accumulated_time", 0.0)
                
                # Recreate visual units
                for unit in self.model.units:
                    self.view.add_visual_unit(
                        unit.id, unit.text, unit.x, unit.y,
                        unit.superposition_symbol, unit.display_width
                    )
                
                QMessageBox.information(self.view, "Loaded", f"State loaded from {file_path}")
            except Exception as e:
                QMessageBox.warning(self.view, "Error", f"Failed to load: {e}")

    def handle_screenshot(self):
        """Save a screenshot of the whiteboard."""
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Save Screenshot",
            "quantum_screenshot.png",
            "PNG Images (*.png)"
        )
        if file_path:
            try:
                pixmap = self.view.whiteboard.grab()
                pixmap.save(file_path)
                QMessageBox.information(self.view, "Saved", f"Screenshot saved to {file_path}")
            except Exception as e:
                QMessageBox.warning(self.view, "Error", f"Failed to save screenshot: {e}")

    def handle_reset(self):
        """Reset the board state."""
        confirm = QMessageBox.question(
            self.view, 
            "Reset Spacetime", 
            "Are you sure you want to clear the whiteboard?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.model.units.clear()
            self.model.entangled_pairs.clear()
            self.model.time_distortion = 0.0
            self.accumulated_time = 0.0
            
            # Clear UI
            self.view.whiteboard.unit_widgets.clear()
            for child in self.view.whiteboard.children():
                if hasattr(child, 'unit_id'):
                    child.deleteLater()
            
            # Reset view labels
            self.view.update_time_display("00:00:00.000", SUPERPOSITION_SYMBOLS[1])
            self.view.update_distortion_display(0.0)

    def handle_grid_change(self, grid_type):
        """Update whiteboard grid type."""
        self.view.whiteboard.set_grid_type(grid_type)

    def handle_remote_distortion(self, remote_value):
        """
        Handle distortion received from network.
        For now, we just add it to the model's current distortion for display/effect.
        This is a simple additive interference.
        """
        # We need to inject this into the model.
        # Since model calculates distortion every frame, we might need a property 'external_distortion'
        # For phase 5.1 MVP, let's just modify the view's display to show it?
        # Or better, update model to accept external input.
        self.model.external_distortion = remote_value

def main():
    app = QApplication(sys.argv)
    controller = QuantumController()
    ret = app.exec()
    controller.network.stop()
    sys.exit(ret)


if __name__ == "__main__":
    main()
