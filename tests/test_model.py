import unittest
import time
import uuid
from quantum_chronometer.model import QuantumModel, QuantumUnit

class TestQuantumUnit(unittest.TestCase):
    """Tests for individual QuantumUnit behavior."""
    
    def test_unit_has_unique_id(self):
        """Each unit should have a unique identifier."""
        unit1 = QuantumUnit("🚀", 0, 0)
        unit2 = QuantumUnit("💡", 10, 10)
        self.assertIsNotNone(unit1.id)
        self.assertIsNotNone(unit2.id)
        self.assertNotEqual(unit1.id, unit2.id)

    def test_unit_local_time_calculation(self):
        """Unit should track its own local elapsed time."""
        unit = QuantumUnit("⚛️", 50, 50)
        
        unit.accumulate_time(0.5)
        
        self.assertAlmostEqual(unit.elapsed_time_sec, 0.5, places=2)

    def test_unit_get_local_magnified_time(self):
        """Unit should calculate its own magnified local time."""
        unit = QuantumUnit("🌌", 100, 100)
        
        unit.accumulate_time(2.0)
        
        local_time = unit.get_local_magnified_time(None) # current_time ignored now
        self.assertIsInstance(local_time, float)
        self.assertGreater(local_time, 1.5)
        self.assertLess(local_time, 3.0)

    # --- NEW: Multi-Emoji Unit Tests ---
    def test_unit_single_emoji(self):
        """Unit with single emoji should work normally."""
        unit = QuantumUnit("🚀", 0, 0)
        self.assertEqual(unit.text, "🚀")
        self.assertEqual(unit.emoji_count, 1)

    def test_unit_multiple_emojis(self):
        """Unit with multiple emojis should store all of them."""
        unit = QuantumUnit("🚀💡🌌", 0, 0)
        self.assertEqual(unit.text, "🚀💡🌌")
        self.assertEqual(unit.emoji_count, 3)

    def test_unit_display_width(self):
        """Unit should report appropriate display width based on emoji count."""
        unit1 = QuantumUnit("🚀", 0, 0)
        unit2 = QuantumUnit("🚀💡", 0, 0)
        
        self.assertEqual(unit1.display_width, 60)  # Base width for 1 emoji
        self.assertGreater(unit2.display_width, unit1.display_width)  # More emojis = wider


class TestQuantumModel(unittest.TestCase):
    """Tests for the QuantumModel (system-level behavior)."""
    
    def setUp(self):
        self.model = QuantumModel()

    def test_initial_state(self):
        self.assertEqual(self.model.time_distortion, 0.0)
        self.assertEqual(len(self.model.units), 0)

    def test_add_unit(self):
        unit = QuantumUnit("🚀", 0, 0)
        self.model.add_unit(unit)
        self.assertEqual(len(self.model.units), 1)
        self.assertEqual(self.model.units[0].text, "🚀")

    def test_get_unit_by_id(self):
        """Model should be able to retrieve a unit by its ID."""
        unit = QuantumUnit("🔮", 25, 25)
        self.model.add_unit(unit)
        
        retrieved = self.model.get_unit_by_id(unit.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.text, "🔮")
        
        fake_id = str(uuid.uuid4())
        self.assertIsNone(self.model.get_unit_by_id(fake_id))

    def test_update_unit_position(self):
        """Model should update a unit's position by ID."""
        unit = QuantumUnit("🎯", 10, 10)
        self.model.add_unit(unit)
        
        success = self.model.update_unit_position(unit.id, 200, 300)
        self.assertTrue(success)
        self.assertEqual(unit.x, 200)
        self.assertEqual(unit.y, 300)
        
        fake_id = str(uuid.uuid4())
        self.assertFalse(self.model.update_unit_position(fake_id, 0, 0))

    def test_distortion_calculation_single_unit(self):
        unit = QuantumUnit("A", 10, 10)
        self.model.add_unit(unit)
        
        self.model.update_unit_times(dt=0.1, is_observing=True)
        self.assertIsInstance(self.model.time_distortion, float)

    def test_proximity_affects_distortion(self):
        """Two units close together should create more distortion than apart."""
        unit1 = QuantumUnit("A", 50, 50)
        unit2 = QuantumUnit("B", 55, 55)
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        
        self.model.update_unit_times(dt=0.1, is_observing=True)
        close_distortion = abs(self.model.time_distortion)
        
        self.model = QuantumModel()
        unit3 = QuantumUnit("C", 50, 50)
        unit4 = QuantumUnit("D", 500, 500)
        self.model.add_unit(unit3)
        self.model.add_unit(unit4)
        
        self.model.update_unit_times(dt=0.1, is_observing=True)
        far_distortion = abs(self.model.time_distortion)
        
        self.assertGreater(close_distortion, far_distortion)

    # --- NEW: Proximity Pairs for Visual Lines ---
    def test_get_proximity_pairs(self):
        """Model should return pairs of units that are close together."""
        unit1 = QuantumUnit("A", 50, 50)
        unit2 = QuantumUnit("B", 60, 60)   # Close to unit1 (~14px)
        unit3 = QuantumUnit("C", 500, 500) # Far from both
        
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        self.model.add_unit(unit3)
        
        pairs = self.model.get_proximity_pairs(threshold=100)
        
        # Should have one pair: (unit1, unit2)
        self.assertEqual(len(pairs), 1)
        pair_ids = {pairs[0][0].id, pairs[0][1].id}
        self.assertIn(unit1.id, pair_ids)
        self.assertIn(unit2.id, pair_ids)

    def test_get_proximity_pairs_empty(self):
        """No pairs if units are far apart."""
        unit1 = QuantumUnit("A", 0, 0)
        unit2 = QuantumUnit("B", 500, 500)
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        
        pairs = self.model.get_proximity_pairs(threshold=100)
        self.assertEqual(len(pairs), 0)

    # --- Phase 3: Entanglement Tests ---
    def test_entangle_units(self):
        """Two units can be entangled."""
        unit1 = QuantumUnit("A", 0, 0)
        unit2 = QuantumUnit("B", 100, 100)
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        
        success = self.model.entangle_units(unit1.id, unit2.id)
        self.assertTrue(success)
        self.assertIn((unit1.id, unit2.id), self.model.entangled_pairs)

    def test_entangled_units_share_distortion(self):
        """Entangled units should share their local distortion."""
        unit1 = QuantumUnit("A", 0, 0)
        unit2 = QuantumUnit("B", 500, 500)
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        self.model.entangle_units(unit1.id, unit2.id)
        
        # Update times to calculate distortion
        self.model.update_unit_times(dt=1.0, is_observing=True)
        
        # Entangled units should have similar local_distortion
        diff = abs(unit1.local_distortion - unit2.local_distortion)
        self.assertLess(diff, 0.1)  # Allow small variance

    def test_get_entangled_pairs(self):
        """Model should return list of entangled unit pairs."""
        unit1 = QuantumUnit("A", 0, 0)
        unit2 = QuantumUnit("B", 100, 100)
        self.model.add_unit(unit1)
        self.model.add_unit(unit2)
        self.model.entangle_units(unit1.id, unit2.id)
        
        pairs = self.model.get_entangled_pairs()
        self.assertEqual(len(pairs), 1)

    # --- Phase 3: Black Hole Unit Tests ---
    def test_black_hole_unit_detection(self):
        """🕳️ emoji should be detected as black hole unit."""
        unit = QuantumUnit("🕳️", 100, 100)
        self.assertTrue(unit.is_black_hole)
        
        normal_unit = QuantumUnit("🚀", 100, 100)
        self.assertFalse(normal_unit.is_black_hole)

    def test_black_hole_increases_distortion(self):
        """Black hole unit should create extra time distortion."""
        # Without black hole
        unit1 = QuantumUnit("🚀", 100, 100)
        self.model.add_unit(unit1)
        self.model.update_unit_times(dt=0.5, is_observing=True)
        normal_dist = abs(self.model.time_distortion)
        
        # With black hole
        self.model = QuantumModel()
        unit2 = QuantumUnit("🕳️", 100, 100)
        self.model.add_unit(unit2)
        self.model.update_unit_times(dt=0.5, is_observing=True)
        black_hole_dist = abs(self.model.time_distortion)
        
        self.assertGreater(black_hole_dist, normal_dist)

    def test_distortion_reset(self):
        self.model.time_distortion = 5.0
        self.model.collapse_wave_function()
        self.assertEqual(self.model.time_distortion, 0.0)

    def test_magnified_time(self):
        start_time = self.model.start_time
        current_time = start_time + 1.0
        
        magnified = self.model.calculate_magnified_time(current_time)
        self.assertAlmostEqual(magnified, 1.0, places=1)
        
        self.model.time_distortion = 1.0
        magnified = self.model.calculate_magnified_time(current_time)
        self.assertAlmostEqual(magnified, 2.0, places=1)

    # --- Phase 4.2: Save/Load State Tests ---
    def test_save_state_returns_dict(self):
        """Model should serialize state to a dictionary."""
        unit = QuantumUnit("🚀", 100, 150)
        self.model.add_unit(unit)
        
        state = self.model.save_state()
        
        self.assertIsInstance(state, dict)
        self.assertIn("units", state)
        self.assertIn("accumulated_time", state)
        self.assertEqual(len(state["units"]), 1)

    def test_save_state_unit_data(self):
        """Saved unit should contain all necessary fields."""
        unit = QuantumUnit("⚛️🔮", 50, 75)
        self.model.add_unit(unit)
        
        state = self.model.save_state()
        saved_unit = state["units"][0]
        
        self.assertEqual(saved_unit["text"], "⚛️🔮")
        self.assertEqual(saved_unit["x"], 50)
        self.assertEqual(saved_unit["y"], 75)
        self.assertIn("id", saved_unit)
        self.assertIn("superposition_symbol", saved_unit)

    def test_load_state_restores_units(self):
        """Model should restore units from saved state."""
        state = {
            "units": [
                {"id": "test-id-1", "text": "🌌", "x": 200, "y": 300, "superposition_symbol": "+"},
                {"id": "test-id-2", "text": "💡", "x": 100, "y": 100, "superposition_symbol": "*"},
            ],
            "accumulated_time": 10.5,
            "entangled_pairs": []
        }
        
        self.model.load_state(state)
        
        self.assertEqual(len(self.model.units), 2)
        self.assertEqual(self.model.units[0].text, "🌌")
        self.assertEqual(self.model.units[1].x, 100)


if __name__ == '__main__':
    unittest.main()

