import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_rolling_radius(rg, rh):
    return (2/3) * rg + (1/3) * rh

def main():
    st.set_page_config(page_title="Rolling Radius & RPM Calc", page_icon="🛞")
    
    st.title("🛞 Wheel Speed Calculator")
    st.markdown("Input your target linear velocity ($v$) to find the required angular velocity ($\\omega$) and RPM.")
    
    # Sidebar for inputs
    st.sidebar.header("1. Geometry Inputs")
    rg_input = st.sidebar.text_input("Geometric Radius (Rg) [mm]", value="315.0")
    rh_input = st.sidebar.text_input("Loaded Height (Rh) [mm]", value="300.0")

    st.sidebar.header("2. Motion Input")
    v_input = st.sidebar.text_input("Linear Velocity (v) [mm/s]", value="10000")

    try:
        # Convert string inputs to floats
        rg = float(rg_input)
        rh = float(rh_input)
        v = float(v_input)
        
        if rh > rg:
            st.error("⚠️ Loaded height (Rh) cannot be greater than Geometric radius (Rg).")
        elif rh <= 0 or rg <= 0:
            st.error("⚠️ Geometry values must be greater than zero.")
        else:
            # 1. Calculate Rolling Radius
            rw = calculate_rolling_radius(rg, rh)

            # 2. Calculate Angular Velocity (omega = v / rw)
            omega = v / rw
            
            # 3. Calculate RPM (RPM = omega * 60 / (2 * pi))
            rpm = (omega * 60) / (2 * np.pi)
            
            # Bonus: km/h conversion just for real-world context
            v_kmh = (v * 3600) / 1_000_000

            # Results Display
            st.subheader("Calculated Results")
            c1, c2, c3 = st.columns(3)
            c1.metric("Rolling Radius (Rw)", f"{rw:.2f} mm")
            c2.metric("Angular Vel (ω)", f"{omega:.2f} rad/s")
            c3.metric("Required RPM", f"{rpm:.1f} RPM")

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

            # Rotation Curve Arrow (Visual aid for omega)
            # This draws a small curved arrow to represent the spin
            fig.add_annotation(x=rw*0.7, y=rw*0.7, ax=0, ay=rw, 
                               xref="x", yref="y", axref="x", ayref="y",
                               text="ω", showarrow=True, arrowhead=2, arrowcolor="blue")

            fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
                              height=500, margin=dict(l=10, r=10, t=10, b=10))

            st.plotly_chart(fig, use_container_width=True)

            with st.expander("View Calculation Details"):
                st.latex(f"R_w = \\frac{{2}}{{3}}({rg}) + \\frac{{1}}{{3}}({rh}) = {rw:.2f} \\text{{ mm}}")
                st.latex(f"v = {v:.2f} \\text{{ mm/s}} \\quad (\\approx {v_kmh:.2f} \\text{{ km/h}})")
                st.latex(f"\\omega = \\frac{{v}}{{R_w}} = \\frac{{{v}}}{{{rw:.2f}}} = {omega:.2f} \\text{{ rad/s}}")
                st.latex(f"RPM = \\frac{{\\omega \\cdot 60}}{{2\\pi}} = {rpm:.2f} \\text{{ RPM}}")

    except ValueError:
        st.sidebar.error("Please enter valid numbers only.")

if __name__ == "__main__":
    main()
