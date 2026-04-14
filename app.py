import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_rolling_radius(rg, rh):
    return (2/3) * rg + (1/3) * rh

def main():
    st.set_page_config(page_title="Rolling Radius & Velocity", page_icon="🛞")
    
    st.title("🛞 Rolling Radius & Velocity Calc")
    st.markdown("Calculate effective radius and linear velocity $v = R_w \\cdot \\omega$")
    
    # Sidebar for inputs
    st.sidebar.header("1. Geometry Inputs")
    rg_input = st.sidebar.text_input("Geometric Radius (Rg) [mm]", value="315.0")
    rh_input = st.sidebar.text_input("Loaded Height (Rh) [mm]", value="300.0")

    st.sidebar.header("2. Motion Inputs")
    rpm_input = st.sidebar.text_input("Rotational Speed [RPM]", value="1000")

    try:
        # Convert string inputs to floats
        rg = float(rg_input)
        rh = float(rh_input)
        rpm = float(rpm_input)
        
        if rh > rg:
            st.error("⚠️ Loaded height (Rh) cannot be greater than Geometric radius (Rg).")
        elif rh <= 0 or rg <= 0:
            st.error("⚠️ Values must be greater than zero.")
        else:
            # 1. Calculate Rolling Radius
            rw = calculate_rolling_radius(rg, rh)

            # 2. Calculate Velocity (v = rw * omega)
            # Convert RPM to Rad/s: omega = (RPM * 2 * pi) / 60
            omega = (rpm * 2 * np.pi) / 60
            velocity_mms = rw * omega
            velocity_kmh = (velocity_mms * 3600) / 1_000_000 # mm/s to km/h conversion

            # Results Display
            st.subheader("Calculated Results")
            c1, c2, c3 = st.columns(3)
            c1.metric("Rolling Radius (Rw)", f"{rw:.2f} mm")
            c2.metric("Velocity (v)", f"{velocity_mms:.2f} mm/s")
            c3.metric("Velocity (km/h)", f"{velocity_kmh:.2f} km/h")

            # --- Graphical Representation ---
            theta = np.linspace(0, 2*np.pi, 100)
            fig = go.Figure()

            # Unloaded Tire Profile
            fig.add_trace(go.Scatter(x=rg*np.cos(theta), y=rg*np.sin(theta), 
                                     name='Geometric (Rg)', line=dict(color='gray', dash='dash')))

            # Effective Rolling Circle
            fig.add_trace(go.Scatter(x=rw*np.cos(theta), y=rw*np.sin(theta), 
                                     name='Rolling Radius (Rw)', line=dict(color='green', width=3)))

            # Ground and Axle
            fig.add_trace(go.Scatter(x=[0, 0], y=[0, -rh], mode='lines+markers', 
                                     name='Loaded Height (Rh)', line=dict(color='red')))
            fig.add_shape(type="line", x0=-rg*1.2, y0=-rh, x1=rg*1.2, y1=-rh, line=dict(color="black", width=3))

            # Velocity Vector Arrow (Visual aid)
            fig.add_annotation(x=0, y=rw+30, ax=velocity_mms/10, ay=rw+30, 
                               xref="x", yref="y", axref="x", ayref="y",
                               text="v", showarrow=True, arrowhead=2, arrowcolor="green")

            fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
                              height=500, margin=dict(l=10, r=10, t=10, b=10))

            st.plotly_chart(fig, use_container_width=True)

            with st.expander("View Calculation Details"):
                st.latex(f"R_w = \\frac{{2}}{{3}}({rg}) + \\frac{{1}}{{3}}({rh}) = {rw:.2f} \\text{{ mm}}")
                st.latex(f"\\omega = \\frac{{{rpm} \\cdot 2\\pi}}{{60}} = {omega:.2f} \\text{{ rad/s}}")
                st.latex(f"v = R_w \\cdot \\omega = {rw:.2f} \\cdot {omega:.2f} = {velocity_mms:.2f} \\text{{ mm/s}}")

    except ValueError:
        st.sidebar.error("Please enter numbers only.")

if __name__ == "__main__":
    main()
