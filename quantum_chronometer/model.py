import time
import math
import uuid
import re
from random import choice, uniform

PLANCK_TIME_MAGNIFIER = 1.0  # Seconds per "magnified Planck Time unit"
DISTANCE_GRAVITY_FACTOR = 0.05  # How much distance affects time (5% per unit distance)
CLOSE_GRAVITY_FACTOR = 0.10     # Additional effect when units are close (10%)
BLACK_HOLE_FACTOR = 0.50        # Extra distortion multiplier for black hole units
SUPERPOSITION_SYMBOLS = ['+', '*', '~']
BLACK_HOLE_EMOJIS = ['🕳️', '🕳']  # Black hole emoji variants

# Regex pattern to count emojis (handles most common emoji patterns)
EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001F9FF]"  # Miscellaneous Symbols and Pictographs, Emoticons, etc.
    "|[\U00002600-\U000027BF]"  # Misc symbols
    "|[\U0001F600-\U0001F64F]"  # Emoticons
    "|[\U0001F680-\U0001F6FF]"  # Transport and Map
    "|[\U0001F1E0-\U0001F1FF]"  # Flags
    "|[\U00002702-\U000027B0]"  # Dingbats
    "|[\U0001FA00-\U0001FAFF]"  # Chess, symbols
    "|."  # Fallback for single characters
)


class QuantumUnit:
    """
    Represents a quantum unit (an abstracted particle).
    Can contain one or multiple emojis.
    Its position and proximity to others affect time measurement.
    Each unit has its own local chronometer.
    """
    BASE_WIDTH = 60   # Base display width for single emoji
    EXTRA_WIDTH = 30  # Additional width per extra emoji
    
    def __init__(self, text, x, y):
        self.id = str(uuid.uuid4())
        self.text = text
        self.x = x
        self.y = y
        self.superposition_symbol = choice(SUPERPOSITION_SYMBOLS)
        self.start_time = time.time()
        self.elapsed_time_sec = 0.0
        self.local_distortion = 0.0

    @property
    def emoji_count(self):
        """Count the number of emoji/characters in this unit."""
        # Simple approach: count grapheme clusters
        # For emojis, this is a reasonable approximation
        emojis = re.findall(EMOJI_PATTERN, self.text)
        # Filter out empty matches
        count = len([e for e in emojis if e.strip()])
        return max(1, count)  # At least 1

    @property
    def display_width(self):
        """Calculate display width based on emoji count."""
        return self.BASE_WIDTH + (self.emoji_count - 1) * self.EXTRA_WIDTH

    @property
    def is_black_hole(self):
        """Check if this unit contains a black hole emoji."""
        return any(bh in self.text for bh in BLACK_HOLE_EMOJIS)

    def accumulate_time(self, delta_seconds):
        """Accumulate time delta."""
        self.elapsed_time_sec += delta_seconds

    def update_time(self, current_time):
        """Calculates and updates the elapsed time for this unit. (Legacy)"""
        # Kept for backward compatibility if needed, but logic is shifting to accumulate
        pass

    def get_local_magnified_time(self, current_time):
        """
        Calculates this unit's local magnified time.
        Formula: (elapsed + local_distortion) * PLANCK_TIME_MAGNIFIER
        """
        return (self.elapsed_time_sec + self.local_distortion) * PLANCK_TIME_MAGNIFIER


class QuantumModel:
    """
    Manages the state of the Quantum Chronometer:
    - Time tracking
    - List of units
    - Calculation of time distortion (Quantum Gravity Effects)
    """
    def __init__(self):
        self.units = []
        self.start_time = time.time()
        self.time_distortion = 0.0
        self.entangled_pairs = []  # List of (unit_id1, unit_id2) tuples
        self.external_distortion = 0.0 # From network (Phase 5.1)
        
    def add_unit(self, unit):
        self.units.append(unit)

    def entangle_units(self, unit_id1, unit_id2):
        """Create an entanglement between two units."""
        unit1 = self.get_unit_by_id(unit_id1)
        unit2 = self.get_unit_by_id(unit_id2)
        if unit1 and unit2 and unit_id1 != unit_id2:
            self.entangled_pairs.append((unit_id1, unit_id2))
            return True
        return False

    def get_entangled_pairs(self):
        """Return list of entangled unit pairs as (unit1, unit2) tuples."""
        pairs = []
        for id1, id2 in self.entangled_pairs:
            unit1 = self.get_unit_by_id(id1)
            unit2 = self.get_unit_by_id(id2)
            if unit1 and unit2:
                pairs.append((unit1, unit2))
        return pairs

    def get_unit_by_id(self, unit_id):
        """Retrieve a unit by its unique ID."""
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        return None

    def update_unit_position(self, unit_id, new_x, new_y):
        """Update a unit's position by ID. Returns True if successful."""
        unit = self.get_unit_by_id(unit_id)
        if unit:
            unit.x = new_x
            unit.y = new_y
            return True
        return False
        
    def move_unit(self, unit, new_x, new_y):
        """Direct move (deprecated, use update_unit_position for ID-based)."""
        unit.x = new_x
        unit.y = new_y
        
    def collapse_wave_function(self):
        """Resets the time distortion to zero (Observation Effect)."""
        self.time_distortion = 0.0

    def get_proximity_pairs(self, threshold=100):
        """
        Returns list of (unit1, unit2) tuples for units within threshold distance.
        Used for drawing proximity lines in the view.
        """
        pairs = []
        for i, unit1 in enumerate(self.units):
            for unit2 in self.units[i+1:]:
                distance = math.sqrt(
                    (unit1.x - unit2.x)**2 + 
                    (unit1.y - unit2.y)**2
                )
                if distance < threshold:
                    pairs.append((unit1, unit2))
        return pairs
        
    def calculate_magnified_time(self, current_time):
        """
        Calculates the total time, magnified from Planck Time.
        Returns total_time_seconds.
        """
        elapsed_sec = current_time - self.start_time
        distorted_time = elapsed_sec + self.time_distortion
        return distorted_time * PLANCK_TIME_MAGNIFIER

    def update_unit_times(self, dt, is_observing=False, mouse_pos=None):
        """
        Applies 'Quantum Gravity Effects' to time measurement.
        dt: time step (e.g., 0.05s)
        is_observing: if True, time moves forward
        mouse_pos: (x, y) tuple for proximity intensity calculation
        """
        total_delta = 0.0
        
        # Calculate Mouse Proximity Intensity
        proximity_intensity = 0.0
        if mouse_pos:
            mx, my = mouse_pos
            # Find closest unit
            min_dist = float('inf')
            for unit in self.units:
                dist = math.sqrt((unit.x - mx)**2 + (unit.y - my)**2)
                if dist < min_dist:
                    min_dist = dist
            
            # Closer = Higher Intensity (Max 1.0 at 0 dist, 0.0 at >300px)
            if min_dist < 300:
                proximity_intensity = (300 - min_dist) / 300.0

        # Apply time flow to units
        for unit in self.units:
            # Time only increments if observing
            if is_observing:
                # Flow rate depends on proximity intensity (base 0.1 + 0.9 * intensity)
                # If continuous observe button is on, we might assume max intensity or standard flow
                flow_factor = 0.5 + 0.5 * proximity_intensity
                unit.accumulate_time(dt * flow_factor)
            
            # 1. Movement Effect (simulated by random flux for now as we don't track velocity explicitly)
            movement_fuzz_delta = math.sin(time.time()) * 0.001
            
            # 2. Proximity/Gravity Effect
            proximity_delta = 0.0
            for other_unit in self.units:
                if unit is not other_unit:
                    distance = math.sqrt(
                        (unit.x - other_unit.x)**2 + 
                        (unit.y - other_unit.y)**2
                    )
                    if distance < 100:
                        safe_dist = max(distance, 1.0)
                        proximity_delta += CLOSE_GRAVITY_FACTOR / (safe_dist / 50.0)
            
            # 3. Superposition Effect
            if unit.superposition_symbol == '+':
                superposition_delta = uniform(0.001, 0.005)
            elif unit.superposition_symbol == '*':
                superposition_delta = uniform(-0.002, 0.002)
            else:  # '~'
                superposition_delta = uniform(-0.005, -0.001)
            
            # 4. Black Hole Effect
            black_hole_delta = 0.0
            if unit.is_black_hole:
                black_hole_delta = BLACK_HOLE_FACTOR
                
            local_delta = movement_fuzz_delta + proximity_delta + superposition_delta + black_hole_delta
            unit.local_distortion = local_delta
            total_delta += local_delta
        
        # 5. Entanglement: share distortion between entangled pairs
        for unit1, unit2 in self.get_entangled_pairs():
            avg_distortion = (unit1.local_distortion + unit2.local_distortion) / 2
            unit1.local_distortion = avg_distortion
            unit2.local_distortion = avg_distortion
            
        self.time_distortion = total_delta + self.external_distortion


    def save_state(self, accumulated_time=0.0):
        """
        Serialize the current model state to a dictionary.
        Can be saved to JSON for persistence.
        """
        units_data = []
        for unit in self.units:
            units_data.append({
                "id": unit.id,
                "text": unit.text,
                "x": unit.x,
                "y": unit.y,
                "superposition_symbol": unit.superposition_symbol,
            })
        
        return {
            "units": units_data,
            "accumulated_time": accumulated_time,
            "entangled_pairs": list(self.entangled_pairs),
            "time_distortion": self.time_distortion,
        }

    def load_state(self, state):
        """
        Restore model state from a dictionary (e.g., loaded from JSON).
        """
        self.units = []
        self.entangled_pairs = []
        
        for unit_data in state.get("units", []):
            unit = QuantumUnit(
                unit_data["text"],
                unit_data["x"],
                unit_data["y"]
            )
            # Restore ID and superposition if provided
            if "id" in unit_data:
                unit.id = unit_data["id"]
            if "superposition_symbol" in unit_data:
                unit.superposition_symbol = unit_data["superposition_symbol"]
            self.units.append(unit)
        
        self.entangled_pairs = [tuple(pair) for pair in state.get("entangled_pairs", [])]
        self.time_distortion = state.get("time_distortion", 0.0)

