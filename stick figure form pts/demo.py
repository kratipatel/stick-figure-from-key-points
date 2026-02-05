"""
Demo Script: Showcasing All Animation Features
==============================================
This script demonstrates all capabilities of the stick figure visualization system.
"""

from stick_figure import StickFigure
import matplotlib.pyplot as plt


def demo_static_poses():
    """Demonstrate different static poses."""
    print("\n" + "="*60)
    print("DEMO 1: Static Pose Variations")
    print("="*60)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    # Pose 1: Standing (default)
    sf1 = StickFigure()
    sf1.plot_skeleton(axes[0], "Standing Pose")
    
    # Pose 2: Arms raised
    sf2 = StickFigure()
    sf2.update_joint('left_wrist', (-0.4, 1.5))
    sf2.update_joint('left_elbow', (-0.4, 1.2))
    sf2.update_joint('right_wrist', (0.4, 1.5))
    sf2.update_joint('right_elbow', (0.4, 1.2))
    sf2.plot_skeleton(axes[1], "Arms Raised")
    
    # Pose 3: Squatting
    sf3 = StickFigure()
    sf3.update_joint('left_hip', (-0.2, 0.3))
    sf3.update_joint('right_hip', (0.2, 0.3))
    sf3.update_joint('spine_mid', (0, 0.6))
    sf3.update_joint('left_knee', (-0.3, -0.1))
    sf3.update_joint('right_knee', (0.3, -0.1))
    sf3.update_joint('neck', (0, 1.0))
    sf3.update_joint('left_shoulder', (-0.3, 0.9))
    sf3.update_joint('right_shoulder', (0.3, 0.9))
    sf3.plot_skeleton(axes[2], "Squatting Pose")
    
    plt.tight_layout()
    plt.savefig('demo_static_poses.png', dpi=150)
    print("✓ Saved demo_static_poses.png")
    plt.show()


def demo_joint_tracking():
    """Demonstrate individual joint tracking."""
    print("\n" + "="*60)
    print("DEMO 2: Joint Position Tracking")
    print("="*60)
    
    sf = StickFigure()
    
    print("\nJoint Coordinates:")
    print("-" * 40)
    for joint_name, (x, y) in sf.joints.items():
        print(f"{joint_name:20s}: ({x:6.2f}, {y:6.2f})")
    
    print("\nSkeleton Connections:")
    print("-" * 40)
    for i, (joint1, joint2) in enumerate(sf.skeleton_connections, 1):
        print(f"{i:2d}. {joint1:20s} <-> {joint2}")


def demo_coordinate_system():
    """Demonstrate the coordinate system used."""
    print("\n" + "="*60)
    print("DEMO 3: Understanding the Coordinate System")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    sf = StickFigure()
    sf.plot_skeleton(ax, "Coordinate System Reference")
    
    # Add annotations for key joints
    annotations = {
        'head': 'Head (0, 1.7)',
        'left_shoulder': 'L.Shoulder (-0.3, 1.3)',
        'right_shoulder': 'R.Shoulder (0.3, 1.3)',
        'left_wrist': 'L.Wrist',
        'right_wrist': 'R.Wrist',
        'left_ankle': 'L.Ankle',
        'right_ankle': 'R.Ankle',
    }
    
    for joint_name, label in annotations.items():
        x, y = sf.joints[joint_name]
        ax.annotate(label, xy=(x, y), xytext=(10, 10),
                   textcoords='offset points', fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.savefig('demo_coordinate_system.png', dpi=150)
    print("✓ Saved demo_coordinate_system.png")
    plt.show()


def main():
    """Run all demonstrations."""
    print("="*60)
    print("STICK FIGURE VISUALIZATION - COMPLETE DEMO")
    print("="*60)
    print("\nThis demo will showcase:")
    print("  1. Static pose variations")
    print("  2. Joint position tracking")
    print("  3. Coordinate system visualization")
    print("\nPress Enter to continue...")
    input()
    
    # Run demos
    demo_joint_tracking()
    
    print("\n\nPress Enter to view static poses...")
    input()
    demo_static_poses()
    
    print("\n\nPress Enter to view coordinate system...")
    input()
    demo_coordinate_system()
    
    print("\n" + "="*60)
    print("All demonstrations complete!")
    print("="*60)
    print("\nGenerated files:")
    print("  - demo_static_poses.png")
    print("  - demo_coordinate_system.png")
    print("\nTo see animations, run: python stick_figure.py")


if __name__ == "__main__":
    main()
