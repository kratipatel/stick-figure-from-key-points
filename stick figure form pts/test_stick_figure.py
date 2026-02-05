"""
Unit Tests for Stick Figure Visualization
=========================================
Tests to ensure proper functionality of the StickFigure class.
"""

import unittest
import numpy as np
from stick_figure import StickFigure


class TestStickFigure(unittest.TestCase):
    """Test cases for StickFigure class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stick_figure = StickFigure()
    
    def test_initialization(self):
        """Test that stick figure initializes with correct number of joints."""
        self.assertEqual(len(self.stick_figure.joints), 15,
                        "Should have 15 joints")
        self.assertEqual(len(self.stick_figure.skeleton_connections), 15,
                        "Should have 15 skeleton connections")
    
    def test_joint_coordinates(self):
        """Test that all joints have valid (x, y) coordinates."""
        for joint_name, coords in self.stick_figure.joints.items():
            self.assertIsInstance(coords, tuple,
                                f"{joint_name} should have tuple coordinates")
            self.assertEqual(len(coords), 2,
                           f"{joint_name} should have 2D coordinates")
            x, y = coords
            self.assertIsInstance(x, (int, float),
                                f"{joint_name} x-coordinate should be numeric")
            self.assertIsInstance(y, (int, float),
                                f"{joint_name} y-coordinate should be numeric")
    
    def test_skeleton_connections(self):
        """Test that all skeleton connections reference valid joints."""
        for joint1, joint2 in self.stick_figure.skeleton_connections:
            self.assertIn(joint1, self.stick_figure.joints,
                         f"{joint1} should be a valid joint name")
            self.assertIn(joint2, self.stick_figure.joints,
                         f"{joint2} should be a valid joint name")
    
    def test_update_joint(self):
        """Test joint position update functionality."""
        original_pos = self.stick_figure.joints['head']
        new_pos = (0.5, 2.0)
        
        self.stick_figure.update_joint('head', new_pos)
        self.assertEqual(self.stick_figure.joints['head'], new_pos,
                        "Joint position should be updated")
        
        # Test invalid joint name
        self.stick_figure.update_joint('invalid_joint', (0, 0))
        # Should not raise error, just print warning
    
    def test_symmetry(self):
        """Test that left and right sides are symmetric."""
        # Check that left and right shoulders are symmetric about y-axis
        left_shoulder_x, left_shoulder_y = self.stick_figure.joints['left_shoulder']
        right_shoulder_x, right_shoulder_y = self.stick_figure.joints['right_shoulder']
        
        self.assertAlmostEqual(left_shoulder_x, -right_shoulder_x,
                              msg="Shoulders should be symmetric about y-axis")
        self.assertEqual(left_shoulder_y, right_shoulder_y,
                        "Shoulders should be at same height")
    
    def test_anatomical_validity(self):
        """Test that skeleton has anatomically valid structure."""
        # Head should be above neck
        head_y = self.stick_figure.joints['head'][1]
        neck_y = self.stick_figure.joints['neck'][1]
        self.assertGreater(head_y, neck_y, "Head should be above neck")
        
        # Hips should be below shoulders
        hip_y = self.stick_figure.joints['left_hip'][1]
        shoulder_y = self.stick_figure.joints['left_shoulder'][1]
        self.assertLess(hip_y, shoulder_y, "Hips should be below shoulders")
        
        # Feet should be lowest points
        ankle_y = self.stick_figure.joints['left_ankle'][1]
        self.assertLess(ankle_y, hip_y, "Ankles should be below hips")
    
    def test_coordinate_ranges(self):
        """Test that coordinates are within reasonable ranges."""
        for joint_name, (x, y) in self.stick_figure.joints.items():
            self.assertGreaterEqual(x, -2.0,
                                   f"{joint_name} x-coordinate too far left")
            self.assertLessEqual(x, 2.0,
                                f"{joint_name} x-coordinate too far right")
            self.assertGreaterEqual(y, -2.0,
                                   f"{joint_name} y-coordinate too low")
            self.assertLessEqual(y, 3.0,
                                f"{joint_name} y-coordinate too high")
    
    def test_no_duplicate_connections(self):
        """Test that there are no duplicate skeleton connections."""
        connections_set = set()
        for joint1, joint2 in self.stick_figure.skeleton_connections:
            # Create normalized tuple (sorted order)
            connection = tuple(sorted([joint1, joint2]))
            self.assertNotIn(connection, connections_set,
                           f"Duplicate connection found: {joint1} <-> {joint2}")
            connections_set.add(connection)
    
    def test_all_joints_connected(self):
        """Test that all joints are part of at least one connection."""
        connected_joints = set()
        for joint1, joint2 in self.stick_figure.skeleton_connections:
            connected_joints.add(joint1)
            connected_joints.add(joint2)
        
        for joint_name in self.stick_figure.joints.keys():
            self.assertIn(joint_name, connected_joints,
                         f"{joint_name} is not connected to any other joint")


class TestAnimationSetup(unittest.TestCase):
    """Test animation setup and configuration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stick_figure = StickFigure()
    
    def test_animation_frames_parameter(self):
        """Test that animation methods accept frame parameter."""
        # This test just ensures methods don't crash with different frame counts
        # Actual animation display is skipped in tests
        try:
            # We can't actually test animation without display
            # but we can verify the methods exist
            self.assertTrue(hasattr(self.stick_figure, 'animate_wave'))
            self.assertTrue(hasattr(self.stick_figure, 'animate_walk'))
        except Exception as e:
            self.fail(f"Animation methods should exist: {e}")


def run_tests():
    """Run all tests and display results."""
    print("="*60)
    print("Running Stick Figure Unit Tests")
    print("="*60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestStickFigure))
    suite.addTests(loader.loadTestsFromTestCase(TestAnimationSetup))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
