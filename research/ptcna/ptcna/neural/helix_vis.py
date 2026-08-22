# ratios: loc_comments=42:40 imports_exports=3:2 calls_definitions=31:3
"""
core/helix_vis.py
Visualizes the spectral state of a 7-seed Meta Router.
Plots the complex descriptor Z = Σ E · e^(iθ)
"""

# === MODULE_BUILD ===
# id: pcna_helix_vis
#   module_name: helix_vis
#   module_kind: instrument
#   summary: Visualizes the spectral state of a 7-seed Meta Router by plotting the complex descriptor Z over a simulated trajectory and saving an animation.
#   owner: Erin Spencer
#   public_surface: generate_helix_data, visualize
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove import and call sites
#   requires: none
#   since: 2026-06-02
#   unresolved: saves to hardcoded pcna_helix.gif with no config (Known Issues)
# === END MODULE_BUILD ===

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generate_helix_data(ticks=100):
    """Simulate a meta-router evolving over time."""
    # 7 seeds, random initial phases
    phases = np.random.uniform(-np.pi, np.pi, 7)
    # Masses vary slightly
    masses = np.random.uniform(0.8, 1.2, 7)
    
    # 7:3 coupling induces phase rotation
    # Delta theta approx 2π * 3/7 per tick (idealized)
    omega = (2 * np.pi * 3 / 7) * 0.1 
    
    trajectory = []
    
    for t in range(ticks):
        # Update phases (rotate)
        phases += omega + np.random.normal(0, 0.05, 7)
        
        # Calculate complex Z (The Spectral Descriptor)
        # Z = Sum(mass * e^(i * theta))
        Z = np.sum(masses * np.exp(1j * phases))
        
        trajectory.append(Z)
        
    return np.array(trajectory)

def visualize():
    data = generate_helix_data(ticks=200)
    
    fig = plt.figure(figsize=(10, 5))
    
    # 1. 2D Phase Plot (Unit Circle View)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title("Spectral Phase (Arg Z)")
    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)
    ax1.grid(True)
    ax1.axhline(y=0, color='k', linewidth=0.5)
    ax1.axvline(x=0, color='k', linewidth=0.5)
    
    # Plot history
    ax1.plot(data.real, data.imag, 'b-', alpha=0.5, label='Trajectory')
    # Plot current
    point, = ax1.plot([], [], 'ro', label='Current Z')
    
    # 2. Time Series (Radius/Stability)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title("Spectral Radius (|Z|) - Conservation Check")
    ax2.set_ylim(0, 15)
    ax2.set_xlim(0, 200)
    line_r, = ax2.plot([], [], 'g-', label='Radius')
    
    def update(frame):
        # Update Phase Plot
        current_Z = data[frame]
        point.set_data([current_Z.real], [current_Z.imag])
        
        # Update Radius Plot
        radii = np.abs(data[:frame])
        line_r.set_data(range(frame), radii)
        
        return point, line_r

    ani = FuncAnimation(fig, update, frames=len(data), interval=50, blit=True)
    
    print("Generating Helix visualization...")
    # In Termux, we save to file rather than show window
    ani.save('pcna_helix.gif', writer='pillow', fps=20)
    print("Saved to pcna_helix.gif")

if __name__ == "__main__":
    visualize()
# ratios: loc_comments=42:40 imports_exports=3:2 calls_definitions=31:3
