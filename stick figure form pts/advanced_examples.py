"""
Advanced Examples: Stick Figure Extensions
==========================================
This file demonstrates advanced usage patterns and extensions.
"""

from stick_figure import StickFigure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import json


# ============================================================================
# EXAMPLE 1: Pose Sequence System
# ============================================================================

class PoseSequence:
    """Manage and animate sequences of poses."""
    
    def __init__(self):
        self.poses = []
        self.timings = []
    
    def add_pose(self, joints_dict, duration=1.0):
        """Add a pose to the sequence."""
        self.poses.append(joints_dict.copy())
        self.timings.append(duration)
    
    def interpolate(self, pose1, pose2, t):
        """Linear interpolation between two poses."""
        interpolated = {}
        for joint_name in pose1.keys():
            x1, y1 = pose1[joint_name]
            x2, y2 = pose2[joint_name]
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            interpolated[joint_name] = (x, y)
        return interpolated
    
    def play(self, fps=30):
        """Play the pose sequence as an animation."""
        sf = StickFigure()
        fig, ax = plt.subplots(figsize=(8, 10))
        
        # Calculate total frames
        total_time = sum(self.timings)
        total_frames = int(total_time * fps)
        
        def update(frame):
            # Determine which poses to interpolate between
            elapsed = frame / fps
            cumulative = 0
            
            for i, duration in enumerate(self.timings):
                if elapsed <= cumulative + duration:
                    # Interpolate between pose i and pose i+1
                    if i + 1 < len(self.poses):
                        t = (elapsed - cumulative) / duration
                        interpolated = self.interpolate(
                            self.poses[i], self.poses[i + 1], t
                        )
                        sf.joints = interpolated
                    break
                cumulative += duration
            
            sf.plot_skeleton(ax, f"Pose Sequence - Frame {frame+1}")
        
        anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
        plt.show()


def demo_pose_sequence():
    """Demonstrate pose sequence animation."""
    print("\n" + "="*60)
    print("ADVANCED EXAMPLE 1: Pose Sequence System")
    print("="*60)
    
    # Create poses
    sf = StickFigure()
    
    # Pose 1: Standing
    pose1 = sf.joints.copy()
    
    # Pose 2: Arms raised
    pose2 = sf.joints.copy()
    pose2['left_wrist'] = (-0.4, 1.6)
    pose2['left_elbow'] = (-0.4, 1.3)
    pose2['right_wrist'] = (0.4, 1.6)
    pose2['right_elbow'] = (0.4, 1.3)
    
    # Pose 3: Squat
    pose3 = sf.joints.copy()
    pose3['left_hip'] = (-0.2, 0.3)
    pose3['right_hip'] = (0.2, 0.3)
    pose3['spine_mid'] = (0, 0.6)
    pose3['left_knee'] = (-0.3, -0.1)
    pose3['right_knee'] = (0.3, -0.1)
    
    # Create sequence
    sequence = PoseSequence()
    sequence.add_pose(pose1, duration=1.0)
    sequence.add_pose(pose2, duration=1.5)
    sequence.add_pose(pose3, duration=1.5)
    sequence.add_pose(pose1, duration=1.0)
    
    print("Created 4-pose sequence with smooth transitions")
    print("Close window to continue...")
    sequence.play(fps=20)


# ============================================================================
# EXAMPLE 2: Pose Data Export/Import
# ============================================================================

class PoseSerializer:
    """Save and load poses to/from JSON."""
    
    @staticmethod
    def save_pose(stick_figure, filename):
        """Save a pose to JSON file."""
        data = {
            'joints': {
                name: {'x': pos[0], 'y': pos[1]}
                for name, pos in stick_figure.joints.items()
            },
            'connections': stick_figure.skeleton_connections
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved pose to {filename}")
    
    @staticmethod
    def load_pose(filename):
        """Load a pose from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        sf = StickFigure()
        
        # Update joints from loaded data
        for name, coords in data['joints'].items():
            sf.joints[name] = (coords['x'], coords['y'])
        
        print(f"✓ Loaded pose from {filename}")
        return sf


def demo_pose_serialization():
    """Demonstrate saving and loading poses."""
    print("\n" + "="*60)
    print("ADVANCED EXAMPLE 2: Pose Data Export/Import")
    print("="*60)
    
    # Create custom pose
    sf = StickFigure()
    sf.update_joint('left_wrist', (-0.5, 1.5))
    sf.update_joint('right_wrist', (0.5, 1.5))
    
    # Save pose
    PoseSerializer.save_pose(sf, 'custom_pose.json')
    
    # Load pose
    loaded_sf = PoseSerializer.load_pose('custom_pose.json')
    
    # Display
    loaded_sf.plot_skeleton(title="Loaded Custom Pose")
    plt.savefig('loaded_pose.png', dpi=150)
    print("✓ Saved visualization to loaded_pose.png")
    plt.show()


# ============================================================================
# EXAMPLE 3: Physics-Based Motion
# ============================================================================

class PhysicsSimulator:
    """Simple physics simulation for stick figure motion."""
    
    def __init__(self, stick_figure):
        self.sf = stick_figure
        self.gravity = -0.02
        self.velocities = {name: (0, 0) for name in stick_figure.joints.keys()}
        self.constraints = self._build_constraints()
    
    def _build_constraints(self):
        """Define joint constraints (min/max positions)."""
        return {
            'left_ankle': {'y_min': -0.8, 'y_max': 0.5},
            'right_ankle': {'y_min': -0.8, 'y_max': 0.5},
            'head': {'y_min': 0.5, 'y_max': 2.5},
        }
    
    def apply_gravity(self):
        """Apply gravity to all joints."""
        for joint_name in self.sf.joints.keys():
            vx, vy = self.velocities[joint_name]
            self.velocities[joint_name] = (vx, vy + self.gravity)
    
    def apply_constraints(self):
        """Apply position constraints."""
        for joint_name, constraint in self.constraints.items():
            x, y = self.sf.joints[joint_name]
            
            # Apply y constraints
            if 'y_min' in constraint and y < constraint['y_min']:
                y = constraint['y_min']
                vx, vy = self.velocities[joint_name]
                self.velocities[joint_name] = (vx, -vy * 0.7)  # Bounce
            
            if 'y_max' in constraint and y > constraint['y_max']:
                y = constraint['y_max']
            
            self.sf.joints[joint_name] = (x, y)
    
    def update(self):
        """Update physics simulation by one step."""
        self.apply_gravity()
        
        # Update positions
        for joint_name, (x, y) in self.sf.joints.items():
            vx, vy = self.velocities[joint_name]
            self.sf.joints[joint_name] = (x + vx, y + vy)
        
        self.apply_constraints()
    
    def drop_animation(self, frames=100):
        """Animate figure falling with physics."""
        fig, ax = plt.subplots(figsize=(8, 10))
        
        # Lift the figure
        for joint_name, (x, y) in self.sf.joints.items():
            self.sf.joints[joint_name] = (x, y + 1.0)
        
        def update(frame):
            self.update()
            self.sf.plot_skeleton(ax, f"Physics Simulation - Frame {frame+1}")
        
        anim = FuncAnimation(fig, update, frames=frames, interval=50)
        plt.show()


def demo_physics_simulation():
    """Demonstrate physics-based animation."""
    print("\n" + "="*60)
    print("ADVANCED EXAMPLE 3: Physics-Based Motion")
    print("="*60)
    
    sf = StickFigure()
    physics = PhysicsSimulator(sf)
    
    print("Starting physics simulation...")
    print("Figure will fall and bounce")
    print("Close window to continue...")
    physics.drop_animation(frames=120)


# ============================================================================
# EXAMPLE 4: Multiple Figures in Scene
# ============================================================================

def demo_multiple_figures():
    """Demonstrate multiple stick figures in one scene."""
    print("\n" + "="*60)
    print("ADVANCED EXAMPLE 4: Multiple Figures in Scene")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create three figures at different positions
    figures = []
    x_positions = [-0.8, 0, 0.8]
    
    for i, x_offset in enumerate(x_positions):
        sf = StickFigure()
        
        # Offset all joints
        for joint_name, (x, y) in sf.joints.items():
            sf.joints[joint_name] = (x + x_offset, y)
        
        # Give each a different pose
        if i == 0:  # Left figure - arms down
            pass
        elif i == 1:  # Middle figure - arms raised
            sf.update_joint('left_wrist', (-0.3 + x_offset, 1.6))
            sf.update_joint('right_wrist', (0.3 + x_offset, 1.6))
            sf.update_joint('left_elbow', (-0.3 + x_offset, 1.3))
            sf.update_joint('right_elbow', (0.3 + x_offset, 1.3))
        else:  # Right figure - T-pose
            sf.update_joint('left_wrist', (-0.7 + x_offset, 1.3))
            sf.update_joint('left_elbow', (-0.5 + x_offset, 1.3))
            sf.update_joint('right_wrist', (0.7 + x_offset, 1.3))
            sf.update_joint('right_elbow', (0.5 + x_offset, 1.3))
        
        figures.append(sf)
    
    # Draw all figures
    for sf in figures:
        for joint1, joint2 in sf.skeleton_connections:
            x1, y1 = sf.joints[joint1]
            x2, y2 = sf.joints[joint2]
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
        
        x_coords = [coord[0] for coord in sf.joints.values()]
        y_coords = [coord[1] for coord in sf.joints.values()]
        ax.scatter(x_coords, y_coords, c='red', s=60, zorder=2)
    
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 2)
    ax.set_title("Multiple Stick Figures", fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('multiple_figures.png', dpi=150)
    print("✓ Saved multiple_figures.png")
    plt.show()


# ============================================================================
# Main Demo Runner
# ============================================================================

def main():
    """Run all advanced examples."""
    print("="*60)
    print("ADVANCED EXAMPLES FOR STICK FIGURE VISUALIZATION")
    print("="*60)
    print("\nThese examples demonstrate:")
    print("  1. Pose sequence system with interpolation")
    print("  2. Pose data export/import (JSON)")
    print("  3. Physics-based motion simulation")
    print("  4. Multiple figures in one scene")
    print("\n" + "="*60)
    
    while True:
        print("\nSelect example to run:")
        print("  1 - Pose Sequence Animation")
        print("  2 - Pose Serialization")
        print("  3 - Physics Simulation")
        print("  4 - Multiple Figures")
        print("  5 - Run All")
        print("  Q - Quit")
        
        choice = input("\nYour choice: ").strip().upper()
        
        if choice == '1':
            demo_pose_sequence()
        elif choice == '2':
            demo_pose_serialization()
        elif choice == '3':
            demo_physics_simulation()
        elif choice == '4':
            demo_multiple_figures()
        elif choice == '5':
            demo_pose_sequence()
            demo_pose_serialization()
            demo_physics_simulation()
            demo_multiple_figures()
            break
        elif choice == 'Q':
            break
        else:
            print("Invalid choice. Please try again.")
    
    print("\n" + "="*60)
    print("Advanced examples complete!")
    print("="*60)


if __name__ == "__main__":
    main()
