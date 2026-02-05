"""
Stick Figure Skeleton Visualization from 2D Joint Coordinates
=============================================================
This program demonstrates pose-based animation by visualizing a human stick figure
using predefined joint coordinates. It showcases core concepts used in computer vision
systems for motion tracking and human pose estimation.

Author: Generated for pose estimation visualization
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class StickFigure:
    """
    A class to represent and visualize a human stick figure skeleton.
    """
    
    def __init__(self):
        """Initialize the stick figure with default joint positions."""
        # Define body joint coordinates (x, y) in normalized space
        # Coordinate system: (0, 0) is at center, y increases upward
        self.joints = {
            # Head
            'head': (0, 1.7),
            'neck': (0, 1.4),
            
            # Torso
            'left_shoulder': (-0.3, 1.3),
            'right_shoulder': (0.3, 1.3),
            'left_hip': (-0.2, 0.5),
            'right_hip': (0.2, 0.5),
            'spine_mid': (0, 0.9),
            
            # Left arm
            'left_elbow': (-0.5, 0.9),
            'left_wrist': (-0.6, 0.5),
            
            # Right arm
            'right_elbow': (0.5, 0.9),
            'right_wrist': (0.6, 0.5),
            
            # Left leg
            'left_knee': (-0.2, 0.0),
            'left_ankle': (-0.2, -0.5),
            
            # Right leg
            'right_knee': (0.2, 0.0),
            'right_ankle': (0.2, -0.5),
        }
        
        # Define skeleton connections (bone structure)
        # Each tuple represents a connection between two joints
        self.skeleton_connections = [
            # Head to torso
            ('head', 'neck'),
            ('neck', 'spine_mid'),
            
            # Shoulders
            ('neck', 'left_shoulder'),
            ('neck', 'right_shoulder'),
            
            # Spine to hips
            ('spine_mid', 'left_hip'),
            ('spine_mid', 'right_hip'),
            ('left_hip', 'right_hip'),
            
            # Left arm
            ('left_shoulder', 'left_elbow'),
            ('left_elbow', 'left_wrist'),
            
            # Right arm
            ('right_shoulder', 'right_elbow'),
            ('right_elbow', 'right_wrist'),
            
            # Left leg
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            
            # Right leg
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
        ]
    
    def plot_skeleton(self, ax=None, title="Stick Figure Skeleton"):
        """
        Plot the stick figure skeleton.
        
        Parameters:
        -----------
        ax : matplotlib.axes.Axes, optional
            The axes to plot on. If None, creates new figure.
        title : str
            Title for the plot
        
        Returns:
        --------
        fig, ax : matplotlib figure and axes objects
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 10))
        else:
            fig = ax.get_figure()
        
        # Clear the axes
        ax.clear()
        
        # Draw skeleton connections (bones)
        for joint1, joint2 in self.skeleton_connections:
            x1, y1 = self.joints[joint1]
            x2, y2 = self.joints[joint2]
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=3, zorder=1)
        
        # Draw joints as points
        x_coords = [coord[0] for coord in self.joints.values()]
        y_coords = [coord[1] for coord in self.joints.values()]
        ax.scatter(x_coords, y_coords, c='red', s=100, zorder=2, 
                  edgecolors='darkred', linewidths=2)
        
        # Format the plot
        ax.set_aspect('equal')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 2)
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('X Position', fontsize=12)
        ax.set_ylabel('Y Position', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        
        return fig, ax
    
    def update_joint(self, joint_name, new_position):
        """
        Update the position of a specific joint.
        
        Parameters:
        -----------
        joint_name : str
            Name of the joint to update
        new_position : tuple
            New (x, y) coordinates for the joint
        """
        if joint_name in self.joints:
            self.joints[joint_name] = new_position
        else:
            print(f"Warning: Joint '{joint_name}' not found.")
    
    def animate_wave(self, frames=60, save_path=None):
        """
        Create an animation of the stick figure waving.
        
        Parameters:
        -----------
        frames : int
            Number of frames in the animation
        save_path : str, optional
            Path to save the animation as GIF
        """
        fig, ax = plt.subplots(figsize=(8, 10))
        
        # Store original positions
        original_right_elbow = self.joints['right_elbow']
        original_right_wrist = self.joints['right_wrist']
        
        def update(frame):
            """Update function for animation."""
            # Create wave motion using sine wave
            angle = (frame / frames) * 4 * np.pi  # Two complete waves
            
            # Animate right arm waving
            elbow_y = original_right_elbow[1] + 0.2 * np.sin(angle)
            wrist_y = original_right_wrist[1] + 0.4 * np.sin(angle)
            wrist_x = original_right_wrist[0] + 0.1 * np.cos(angle)
            
            self.update_joint('right_elbow', (original_right_elbow[0], elbow_y))
            self.update_joint('right_wrist', (wrist_x, wrist_y))
            
            # Redraw the skeleton
            self.plot_skeleton(ax, title=f"Stick Figure Animation - Frame {frame+1}/{frames}")
        
        anim = FuncAnimation(fig, update, frames=frames, interval=50, repeat=True)
        
        plt.tight_layout()
        
        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer='pillow', fps=20)
            print("Animation saved!")
        
        plt.show()
        
        # Restore original positions
        self.joints['right_elbow'] = original_right_elbow
        self.joints['right_wrist'] = original_right_wrist
    
    def animate_walk(self, frames=60):
        """
        Create a walking animation.
        
        Parameters:
        -----------
        frames : int
            Number of frames in the animation
        """
        fig, ax = plt.subplots(figsize=(8, 10))
        
        # Store original positions
        original_positions = {
            'left_knee': self.joints['left_knee'],
            'left_ankle': self.joints['left_ankle'],
            'right_knee': self.joints['right_knee'],
            'right_ankle': self.joints['right_ankle'],
            'left_elbow': self.joints['left_elbow'],
            'left_wrist': self.joints['left_wrist'],
            'right_elbow': self.joints['right_elbow'],
            'right_wrist': self.joints['right_wrist'],
        }
        
        def update(frame):
            """Update function for walking animation."""
            # Create walking motion using sine waves with phase offset
            angle = (frame / frames) * 4 * np.pi
            
            # Leg motion (opposite phase for left and right)
            left_leg_angle = angle
            right_leg_angle = angle + np.pi
            
            # Left leg
            left_knee_y = original_positions['left_knee'][1] + 0.1 * np.sin(left_leg_angle)
            left_ankle_y = original_positions['left_ankle'][1] + 0.15 * np.sin(left_leg_angle)
            left_ankle_x = original_positions['left_ankle'][0] + 0.05 * np.sin(left_leg_angle)
            
            # Right leg
            right_knee_y = original_positions['right_knee'][1] + 0.1 * np.sin(right_leg_angle)
            right_ankle_y = original_positions['right_ankle'][1] + 0.15 * np.sin(right_leg_angle)
            right_ankle_x = original_positions['right_ankle'][0] + 0.05 * np.sin(right_leg_angle)
            
            # Arm swing (opposite to legs for natural walking)
            left_arm_angle = right_leg_angle
            right_arm_angle = left_leg_angle
            
            left_wrist_y = original_positions['left_wrist'][1] + 0.1 * np.sin(left_arm_angle)
            right_wrist_y = original_positions['right_wrist'][1] + 0.1 * np.sin(right_arm_angle)
            
            # Update joint positions
            self.update_joint('left_knee', (original_positions['left_knee'][0], left_knee_y))
            self.update_joint('left_ankle', (left_ankle_x, left_ankle_y))
            self.update_joint('right_knee', (original_positions['right_knee'][0], right_knee_y))
            self.update_joint('right_ankle', (right_ankle_x, right_ankle_y))
            self.update_joint('left_wrist', (original_positions['left_wrist'][0], left_wrist_y))
            self.update_joint('right_wrist', (original_positions['right_wrist'][0], right_wrist_y))
            
            # Redraw the skeleton
            self.plot_skeleton(ax, title=f"Walking Animation - Frame {frame+1}/{frames}")
        
        anim = FuncAnimation(fig, update, frames=frames, interval=50, repeat=True)
        plt.tight_layout()
        plt.show()
        
        # Restore original positions
        for joint, pos in original_positions.items():
            self.joints[joint] = pos


def main():
    """
    Main function to demonstrate stick figure visualization and animation.
    """
    print("=" * 60)
    print("Stick Figure Skeleton Visualization")
    print("=" * 60)
    print()
    
    # Create stick figure instance
    stick_figure = StickFigure()
    
    print("Creating stick figure skeleton...")
    print(f"Total joints: {len(stick_figure.joints)}")
    print(f"Total connections: {len(stick_figure.skeleton_connections)}")
    print()
    
    # Display menu
    print("Animation Options:")
    print("1. Static pose (saves as output.png)")
    print("2. Waving animation")
    print("3. Walking animation")
    print()
    
    choice = input("Enter your choice (1/2/3) or press Enter for static pose: ").strip()
    
    if choice == '2':
        print("\nStarting waving animation...")
        print("Close the window to exit.")
        stick_figure.animate_wave(frames=80)
    elif choice == '3':
        print("\nStarting walking animation...")
        print("Close the window to exit.")
        stick_figure.animate_walk(frames=80)
    else:
        print("\nDisplaying static pose...")
        fig, ax = stick_figure.plot_skeleton()
        plt.tight_layout()
        
        # Save the static image
        output_path = 'output.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved static pose to {output_path}")
        
        plt.show()
    
    print("\n" + "=" * 60)
    print("Visualization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
