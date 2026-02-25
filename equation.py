import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# App title
st.title("Ball Motion: x = 5t²")
st.write("This app visualizes the motion of a ball following the equation x = 5t²")

# User input for time range
col1, col2 = st.columns(2)
with col1:
    t_min = st.number_input("Minimum value of t", value=0.0, step=0.1)
with col2:
    t_max = st.number_input("Maximum value of t", value=5.0, step=0.1)

# Number of points
num_points = st.slider("Number of plot points", min_value=10, max_value=1000, value=100)

# Create t values
t = np.linspace(t_min, t_max, num_points)
x = 5 * t**2

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Position-Time Graph", "Ball Motion Animation", "Data Table"])

with tab1:
    st.subheader("Position-Time Graph")
    
    # Plot the curve
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, x, 'b-', linewidth=2, label='x = 5t²')
    ax.set_xlabel('Time (t)', fontsize=12)
    ax.set_ylabel('Position (x)', fontsize=12)
    ax.set_title('Position vs Time', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add a point that can be moved with slider
    t_point = st.slider("Select time to highlight", min_value=float(t_min), 
                        max_value=float(t_max), value=float(t_min), step=0.1)
    x_point = 5 * t_point**2
    ax.plot(t_point, x_point, 'ro', markersize=10, label=f't = {t_point:.1f}')
    ax.legend()
    
    st.pyplot(fig)

with tab2:
    st.subheader("Ball Motion Animation")
    
    # Animation speed control
    speed = st.slider("Animation speed", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    
    # Create two columns for animation and controls
    anim_col1, anim_col2 = st.columns([2, 1])
    
    with anim_col1:
        # Create figure for ball animation
        fig_anim, ax_anim = plt.subplots(figsize=(8, 4))
        
        # Set up the plot
        ax_anim.set_xlim(t_min, t_max)
        ax_anim.set_ylim(-2, max(x) * 1.1)
        ax_anim.set_xlabel('Position (x)', fontsize=12)
        ax_anim.set_ylabel('Height (y)', fontsize=12)
        ax_anim.set_title('Ball Motion Animation', fontsize=14)
        ax_anim.grid(True, alpha=0.3)
        
        # Create ground line
        ax_anim.axhline(y=0, color='gray', linestyle='-', linewidth=2)
        
        # Initialize ball position (will be updated in animation)
        ball = Circle((t_min, 0), 0.3, color='red', zorder=5)
        ax_anim.add_patch(ball)
        
        # Add trail
        trail_x = []
        trail_y = []
        trail, = ax_anim.plot([], [], 'b--', alpha=0.5, linewidth=1)
        
        st.pyplot(fig_anim)
    
    with anim_col2:
        st.write("### Animation Controls")
        
        # Manual control slider
        t_pos = st.slider("Ball position (t)", min_value=float(t_min), 
                          max_value=float(t_max), value=float(t_min), step=0.1)
        
        # Auto-play button
        if st.button("Play Animation"):
            placeholder = st.empty()
            for t_val in np.linspace(t_min, t_max, 50):
                x_val = 5 * t_val**2
                
                # Update ball position
                ball.center = (x_val, 0.5)
                
                # Update trail
                trail_x.append(x_val)
                trail_y.append(0.5)
                trail.set_data(trail_x, trail_y)
                
                # Redraw
                fig_anim.canvas.draw()
                placeholder.pyplot(fig_anim)
                time.sleep(0.05 / speed)
            
            st.success("Animation complete!")
        
        # Reset button
        if st.button("↺ Reset"):
            ball.center = (t_min, 0.5)
            trail.set_data([], [])
            fig_anim.canvas.draw()
            st.rerun()
    
    # Manual position update
    x_pos = 5 * t_pos**2
    ball.center = (x_pos, 0.5)
    
    # Update trail for manual position
    trail_x = [5 * ti**2 for ti in np.linspace(t_min, t_pos, 20)]
    trail_y = [0.5] * len(trail_x)
    trail.set_data(trail_x, trail_y)
    
    fig_anim.canvas.draw()
    st.pyplot(fig_anim)

with tab3:
    st.subheader("Calculated Values")
    
    # Create a comprehensive data table
    sample_t = np.linspace(t_min, t_max, 15)
    sample_x = 5 * sample_t**2
    sample_v = 10 * sample_t  # velocity (derivative: v = 10t)
    sample_a = np.ones_like(sample_t) * 10  # acceleration (constant = 10)
    
    data = {
        'Time (t)': sample_t,
        'Position (x = 5t²)': sample_x,
        'Velocity (v = 10t)': sample_v,
        'Acceleration (a = 10)': sample_a
    }
    
    st.dataframe(data, use_container_width=True)
    
    # Download button for data
    if st.button("Download Data as CSV"):
        import pandas as pd
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Click to download",
            data=csv,
            file_name="ball_motion_data.csv",
            mime="text/csv"
        )

# Sidebar information
st.sidebar.header("Information")
st.sidebar.info("""
    **Equation of Motion: x = 5t²**
    
    This represents motion with constant acceleration:
    - **x**: Position (displacement)
    - **t**: Time
    - **5**: Half the acceleration
    
    **Derived quantities:**
    - Velocity: v = dx/dt = 10t
    - Acceleration: a = dv/dt = 10 (constant)
    
    **This is like:**
    - A ball rolling down an inclined plane
    - An object in free fall (if we ignore gravity direction)
    - Constant acceleration motion
""")

# Add physics explanation
st.sidebar.markdown("---")
st.sidebar.subheader("Physics Concepts")
st.sidebar.write("""
    - **Initial velocity**: 0 m/s
    - **Acceleration**: 10 m/s²
    - **Motion type**: Uniformly accelerated motion
    - **Graph shape**: Parabola
""")

# Add some interactive physics calculations
st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Quick Calculations")

calc_time = st.sidebar.slider("Calculate at time t =", min_value=float(t_min), 
                               max_value=float(t_max), value=2.0, step=0.1)

calc_pos = 5 * calc_time**2
calc_vel = 10 * calc_time
calc_acc = 10

st.sidebar.write(f"At t = {calc_time:.1f}:")
st.sidebar.write(f" Position = {calc_pos:.2f}")
st.sidebar.write(f" Velocity = {calc_vel:.2f}")
st.sidebar.write(f" Acceleration = {calc_acc:.2f}")