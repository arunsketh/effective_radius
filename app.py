import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_rolling_radius(rg, rh):
    return (2/3) * rg + (1/3) * rh

def main():
    st.set_page_config(page_title="Rolling Radius Visualizer", page_icon="🛞")
    
    st.title("🛞 Rolling Radius Visualizer")
    st.markdown("""
    Based on the **AutoMotorGarage** formula, the effective rolling radius is a weighted average 
    of the physical tire dimensions.
    """)

    # Sidebar Inputs
    st.sidebar.header("Tire Parameters")
    rg = st.sidebar.slider("Geometric Radius (Rg) [mm]", 200, 500, 315)
    deflection_pct = st.sidebar.slider("Vertical Deflection (%)", 0, 20, 5)
    
    # Calculate values
    rh = rg * (1 - (deflection_pct / 100))
    rw = calculate_rolling_radius(rg, rh)

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Geometric (Rg)", f"{rg} mm")
    col2.metric("Loaded (Rh)", f"{rh:.1f} mm")
    col3.metric("Rolling (Rw)", f"{rw:.1f} mm", delta=f"{rw-rg:.1f} mm")

    # --- Graphical Representation ---
    st.subheader("Geometry Visualization")
    
    # Create a circle for the tire
    theta = np.linspace(0, 2*np.pi, 100)
    x_unloaded = rg * np.cos(theta)
    y_unloaded = rg * np.sin(theta)

    fig = go.Figure()

    # Unloaded Tire (Geometric)
    fig.add_trace(go.Scatter(x=x_unloaded, y=y_unloaded, name='Unloaded Tire (Rg)', 
                             line=dict(color='gray', dash='dash')))

    # Ground Line
    fig.add_shape(type="line", x0=-rg, y0=-rh, x1=rg, y1=-rh, 
                  line=dict(color="Black", width=3))

    # Radii Markers
    # Rg line
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, rg], mode='lines+markers', name='Rg (Geometric)', line=dict(color='blue')))
    # Rh line
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -rh], mode='lines+markers', name='Rh (Loaded Height)', line=dict(color='red')))
    # Rw indicator (The effective rolling circle)
    fig.add_trace(go.Scatter(x=rw * np.cos(theta), y=rw * np.sin(theta), 
                             name='Effective Rolling Radius (Rw)', line=dict(color='green', width=3)))

    fig.update_layout(
        xaxis=dict(range=[-rg-20, rg+20], constrain='domain'),
        yaxis=dict(range=[-rg-20, rg+20], scaleanchor="x", scaleratio=1),
        width=600, height=600,
        showlegend=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Observation:** Notice that the green circle (Effective Rolling Radius $R_w$) is larger than 
    the loaded height (red line) but smaller than the geometric radius (blue line). 
    This is because the tire tread compresses but doesn't act like a perfectly rigid point.
    """)

if __name__ == "__main__":
    main()
