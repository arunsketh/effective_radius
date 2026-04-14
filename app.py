import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_rolling_radius(rg, rh):
    return (2/3) * rg + (1/3) * rh

def main():
    st.set_page_config(page_title="Rolling Radius Calc", page_icon="🛞")
    
    st.title("🛞 Rolling Radius Visualizer")
    
    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    
    # Text Box entries
    rg_input = st.sidebar.text_input("Geometric Radius (Rg) [mm]", value="315.0")
    rh_input = st.sidebar.text_input("Loaded Height (Rh) [mm]", value="300.0")

    try:
        # Convert string inputs to floats
        rg = float(rg_input)
        rh = float(rh_input)
        
        if rh > rg:
            st.error("⚠️ Loaded height (Rh) cannot be greater than Geometric radius (Rg).")
        elif rh <= 0 or rg <= 0:
            st.error("⚠️ Values must be greater than zero.")
        else:
            # Calculation
            rw = calculate_rolling_radius(rg, rh)

            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Geometric (Rg)", f"{rg} mm")
            c2.metric("Loaded (Rh)", f"{rh} mm")
            c3.metric("Rolling (Rw)", f"{rw:.2f} mm")

            # --- Plotting ---
            theta = np.linspace(0, 2*np.pi, 100)
            
            fig = go.Figure()

            # 1. Unloaded Tire (Geometric)
            fig.add_trace(go.Scatter(
                x=rg * np.cos(theta), y=rg * np.sin(theta),
                name='Geometric Profile (Rg)',
                line=dict(color='rgba(100, 100, 100, 0.5)', dash='dash')
            ))

            # 2. Effective Rolling Circle (Rw)
            fig.add_trace(go.Scatter(
                x=rw * np.cos(theta), y=rw * np.sin(theta),
                name='Effective Rolling Circle (Rw)',
                line=dict(color='green', width=4)
            ))

            # 3. Axle to Ground (Rh)
            fig.add_trace(go.Scatter(
                x=[0, 0], y=[0, -rh],
                mode='lines+markers',
                name='Loaded Height (Rh)',
                line=dict(color='red', width=3)
            ))

            # 4. Ground Line
            fig.add_shape(type="line", x0=-rg*1.2, y0=-rh, x1=rg*1.2, y1=-rh,
                          line=dict(color="Black", width=4))

            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
                height=500,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"**Result:** For every rotation, the wheel travels **{2 * np.pi * rw:.2f} mm**.")

    except ValueError:
        st.sidebar.error("Please enter valid numerical values.")

if __name__ == "__main__":
    main()
