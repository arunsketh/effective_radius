import streamlit as st

def calculate_rolling_radius(rg, rh):
    """Calculates rolling radius based on geometric radius and loaded height."""
    return (2/3) * rg + (1/3) * rh

def main():
    st.set_page_config(page_title="Rolling Radius Calculator", page_icon="🛞")
    
    st.title("🛞 Tire Rolling Radius Calculator")
    st.markdown("""
    This app calculates the **Effective Rolling Radius ($R_w$)** of a tire based on the formula:
    $$R_w = \\frac{2}{3}R_g + \\frac{1}{3}R_h$$
    """)

    st.sidebar.header("Input Parameters")
    
    # Input Method Selection
    input_method = st.sidebar.radio("Input Method", ["Direct Radius Input", "Tire Specification (ISO)"])

    if input_method == "Direct Radius Input":
        rg = st.number_input("Geometric Radius ($R_g$) [mm]", min_value=100.0, value=315.0, step=0.1)
        rh = st.number_input("Loaded Height ($R_h$) [mm]", min_value=100.0, value=300.0, step=0.1)
        
    else:
        st.subheader("ISO Tire Specification")
        col1, col2, col3 = st.columns(3)
        width = col1.number_input("Width (e.g. 225)", value=225)
        aspect = col2.number_input("Aspect Ratio (e.g. 45)", value=45)
        rim = col3.number_input("Rim Diameter (e.g. 17)", value=17)
        
        # Calculate Geometric Radius (Rg)
        # Rg = (Rim / 2 * 25.4) + (Width * Aspect / 100)
        rg = ((rim * 25.4) / 2) + (width * (aspect / 100))
        
        st.info(f"Calculated Geometric Radius ($R_g$): {rg:.2 Sebastian} mm")
        deflection = st.slider("Vertical Deflection (%)", 0, 20, 5)
        rh = rg * (1 - (deflection / 100))
        st.info(f"Estimated Loaded Height ($R_h$): {rh:.2f} mm")

    # Calculation
    if rh > rg:
        st.error("Error: Loaded height (Rh) cannot be greater than Geometric radius (Rg).")
    else:
        rw = calculate_rolling_radius(rg, rh)
        
        st.divider()
        st.header("Results")
        k1, k2 = st.columns(2)
        k1.metric("Effective Rolling Radius ($R_w$)", f"{rw:.2f} mm")
        k2.metric("Total Deflection", f"{rg - rh:.2f} mm")
        
        st.success(f"The effective rolling radius is approximately **{rw:.2f} mm**.")

if __name__ == "__main__":
    main()
