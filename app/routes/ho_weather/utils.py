import matplotlib.pyplot as plt
import numpy as np
import os

"""
Utility Functions:
- Logging setup
- Wind compass visualization generation
- Admin access decorators
"""

def get_wind_direction_label(deg):
    directions = [
        'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
    ]
    idx = int((deg % 360) / 22.5)
    return directions[idx % 16]

def generate_wind_compass_image(angle_deg, image_path):
    compass_radius = 1
    angle_rad = np.deg2rad(90 - angle_deg)  # Compass logic (0° = North)
    x = compass_radius * np.cos(angle_rad)
    y = compass_radius * np.sin(angle_rad)
    wind_label = get_wind_direction_label(angle_deg)

    fig, ax = plt.subplots()
    ax.plot(np.cos(np.linspace(0, 2 * np.pi, 360)),
            np.sin(np.linspace(0, 2 * np.pi, 360)))

    for deg in range(0, 360, 45):
        label = {
            0: 'N', 45: 'NE', 90: 'E', 135: 'SE',
            180: 'S', 225: 'SW', 270: 'W', 315: 'NW'
        }.get(deg, f'{deg}°')
        rad = np.deg2rad(90 - deg)
        mx = compass_radius * np.cos(rad)
        my = compass_radius * np.sin(rad)
        ax.plot([0, mx], [0, my], color='gray', linestyle='--', linewidth=0.5)
        ax.text(1.15 * mx, 1.15 * my, label, ha='center', va='center', fontsize=8, fontweight='bold')

    ax.plot([0, x], [0, y], color='blue', linewidth=2)
    ax.text(x * 1.2, y * 1.2, f'{angle_deg}°\n{wind_label}', color='blue', ha='center', fontsize=9)

    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis('off')
    plt.tight_layout()

    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    plt.savefig(image_path, dpi=100)
    plt.close(fig)

    return wind_label
