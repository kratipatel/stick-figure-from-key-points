# Usage Guide: Stick Figure Skeleton Visualization

## Table of Contents
1. [Quick Start](#quick-start)
2. [Understanding the Code](#understanding-the-code)
3. [Customizing Poses](#customizing-poses)
4. [Creating Animations](#creating-animations)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Program
```bash
python stick_figure.py
```

### Your First Visualization
The program will prompt you with three options:
- **Option 1**: Static pose (saves output.png)
- **Option 2**: Waving animation
- **Option 3**: Walking animation

Press Enter or type `1` for a static pose.

---

## Understanding the Code

### Core Components

#### 1. The StickFigure Class
```python
from stick_figure import StickFigure

# Create an instance
sf = StickFigure()
```

#### 2. Joint Dictionary
Each joint has an (x, y) coordinate:
```python
sf.joints = {
    'head': (0, 1.7),
    'neck': (0, 1.4),
    # ... more joints
}
```

#### 3. Skeleton Connections
Defines which joints are connected:
```python
sf.skeleton_connections = [
    ('head', 'neck'),
    ('neck', 'left_shoulder'),
    # ... more connections
]
```

### Coordinate System
- **Origin**: (0, 0) at center
- **X-axis**: Negative = left, Positive = right
- **Y-axis**: Negative = down, Positive = up
- **Units**: Normalized (-1 to 1 for body width)

---

## Customizing Poses

### Modifying Individual Joints

```python
from stick_figure import StickFigure

sf = StickFigure()

# Raise right arm
sf.update_joint('right_wrist', (0.5, 1.6))
sf.update_joint('right_elbow', (0.5, 1.3))

# Display the modified pose
sf.plot_skeleton()
```

### Creating Custom Poses

#### Example: T-Pose
```python
sf = StickFigure()

# Extend arms horizontally
sf.update_joint('left_elbow', (-0.6, 1.3))
sf.update_joint('left_wrist', (-0.9, 1.3))
sf.update_joint('right_elbow', (0.6, 1.3))
sf.update_joint('right_wrist', (0.9, 1.3))

sf.plot_skeleton(title="T-Pose")
```

#### Example: Sitting Pose
```python
sf = StickFigure()

# Lower the body
sf.update_joint('left_hip', (-0.2, 0.2))
sf.update_joint('right_hip', (0.2, 0.2))
sf.update_joint('spine_mid', (0, 0.5))
sf.update_joint('neck', (0, 1.0))
sf.update_joint('head', (0, 1.3))

# Bend knees forward
sf.update_joint('left_knee', (-0.3, -0.2))
sf.update_joint('right_knee', (0.3, -0.2))
sf.update_joint('left_ankle', (-0.3, -0.5))
sf.update_joint('right_ankle', (0.3, -0.5))

# Adjust shoulders
sf.update_joint('left_shoulder', (-0.3, 0.9))
sf.update_joint('right_shoulder', (0.3, 0.9))

sf.plot_skeleton(title="Sitting Pose")
```

---

## Creating Animations

### Basic Animation Structure

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

sf = StickFigure()
fig, ax = plt.subplots(figsize=(8, 10))

# Store original positions
original_wrist = sf.joints['right_wrist']

def update(frame):
    # Calculate new position
    angle = (frame / 60) * 2 * np.pi
    new_y = original_wrist[1] + 0.3 * np.sin(angle)
    
    # Update joint
    sf.update_joint('right_wrist', (original_wrist[0], new_y))
    
    # Redraw
    sf.plot_skeleton(ax)

anim = FuncAnimation(fig, update, frames=60, interval=50)
plt.show()
```

### Custom Animation: Jumping

```python
def animate_jump(self, frames=60):
    fig, ax = plt.subplots(figsize=(8, 10))
    
    # Store all original positions
    original_joints = self.joints.copy()
    
    def update(frame):
        # Jump arc using parabola
        progress = frame / frames
        height = 4 * progress * (1 - progress)  # Parabolic arc
        
        # Move entire body up
        for joint_name, (x, y) in original_joints.items():
            self.update_joint(joint_name, (x, y + height * 0.5))
        
        self.plot_skeleton(ax, f"Jumping - Frame {frame+1}")
    
    anim = FuncAnimation(fig, update, frames=frames, interval=50)
    plt.show()
```

---

## Advanced Usage

### Multi-Figure Comparison

```python
import matplotlib.pyplot as plt

# Create multiple poses
poses = []
for i in range(4):
    sf = StickFigure()
    # Modify joints for each pose
    angle = i * np.pi / 6
    sf.update_joint('right_wrist', 
                   (0.6 * np.cos(angle), 0.5 + 0.5 * np.sin(angle)))
    poses.append(sf)

# Display in grid
fig, axes = plt.subplots(1, 4, figsize=(16, 5))
for i, (sf, ax) in enumerate(zip(poses, axes)):
    sf.plot_skeleton(ax, f"Pose {i+1}")
plt.tight_layout()
plt.show()
```

### Exporting Animation as GIF

First, install Pillow:
```bash
pip install pillow
```

Then use the built-in method:
```python
sf = StickFigure()
sf.animate_wave(frames=80, save_path='wave_animation.gif')
```

### Custom Skeleton Structure

```python
class CustomStickFigure(StickFigure):
    def __init__(self):
        super().__init__()
        
        # Add extra joints
        self.joints['spine_upper'] = (0, 1.1)
        
        # Add extra connections
        self.skeleton_connections.append(('neck', 'spine_upper'))
        self.skeleton_connections.append(('spine_upper', 'spine_mid'))
```

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution**: Install dependencies
```bash
pip install matplotlib numpy
```

#### Issue: Animation window not showing
**Solution**: Ensure you're not running in a headless environment. For servers:
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

#### Issue: Joint positions look incorrect
**Solution**: Check coordinate ranges. Typical ranges:
- X: -1.0 to 1.0
- Y: -0.5 (feet) to 1.7 (head)

#### Issue: Animation is too fast/slow
**Solution**: Adjust the `interval` parameter in FuncAnimation:
```python
anim = FuncAnimation(fig, update, frames=60, interval=100)  # Slower
```

### Best Practices

1. **Always store original positions** before animating
2. **Use normalized coordinates** for consistency
3. **Maintain anatomical constraints** (e.g., elbow between shoulder and wrist)
4. **Test with static poses** before creating animations
5. **Use version control** to track pose variations

---

## Examples Gallery

### Running All Examples
```bash
python demo.py
```

This will generate:
- `demo_static_poses.png`: Three different poses
- `demo_coordinate_system.png`: Annotated coordinate system

### Testing
```bash
python test_stick_figure.py
```

Tests verify:
- Joint initialization
- Coordinate validity
- Anatomical structure
- Connection integrity

---

## Next Steps

### Beginner
1. Modify existing joint positions
2. Create 3-5 custom static poses
3. Animate a single joint

### Intermediate
1. Create smooth multi-joint animations
2. Implement physics-based motion
3. Add multiple figures to one scene

### Advanced
1. Integrate with MediaPipe for real-time pose detection
2. Create a pose sequence recorder
3. Build a full motion capture system
4. Extend to 3D visualization

---

## Resources

### Related Technologies
- **MediaPipe Pose**: Real-time pose detection
- **OpenPose**: Multi-person pose estimation
- **PyTorch3D**: 3D computer vision
- **Blender Python API**: Professional 3D animation

### Further Reading
- Human pose estimation papers (COCO dataset)
- Skeletal animation in game engines
- Inverse kinematics algorithms

---

**Happy Animating! 🎨**
