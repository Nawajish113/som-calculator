import streamlit as st
import math

st.set_page_config(
    page_title="Strength of Materials Calculator",
    page_icon="🔩",
    layout="centered"
)

st.markdown("""
<style>
    .main-title { font-size: 2rem; font-weight: 600; margin-bottom: 0.2rem; }
    .sub-title  { color: #666; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .formula-box {
        background: #f0f4ff;
        border-left: 4px solid #1a4f8a;
        padding: 10px 16px;
        font-family: monospace;
        font-size: 0.9rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
    .result-safe {
        background: #e8f5ee; color: #1a6b3a;
        padding: 10px 14px; border-radius: 8px;
        font-size: 0.9rem; margin-top: 0.5rem;
    }
    .result-unsafe {
        background: #fde8e8; color: #8a1a1a;
        padding: 10px 14px; border-radius: 8px;
        font-size: 0.9rem; margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔩 Strength of Materials Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Stress · Strain · Beam Bending · Torsion · Column Buckling · Combined Loading</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Normal Stress & Strain",
    "Shear Stress",
    "Beam Bending",
    "Torsion",
    "Column Buckling",
    "Combined Loading"
])


# ── TAB 1: NORMAL STRESS ──────────────────────────────────────────────────────
with tab1:
    st.subheader("Normal Stress & Axial Deformation")
    st.markdown('<div class="formula-box">σ = P / A &nbsp;|&nbsp; ε = σ / E &nbsp;|&nbsp; δ = PL / AE</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — Steel rod, P=50 kN, d=20 mm, L=1.5 m, E=200 GPa"):
        if st.button("Fill example values", key="ex_stress"):
            st.session_state.s_P  = 50000.0
            st.session_state.s_A  = round(math.pi * 20**2 / 4, 2)
            st.session_state.s_L  = 1500.0
            st.session_state.s_E  = 200000.0
            st.session_state.s_sa = 250.0

    col1, col2 = st.columns(2)
    with col1:
        s_P  = st.number_input("Axial Force P (N)",            min_value=0.0, value=st.session_state.get("s_P",  0.0), key="s_P")
        s_A  = st.number_input("Cross-section Area A (mm²)",   min_value=0.0, value=st.session_state.get("s_A",  0.0), key="s_A")
        s_L  = st.number_input("Length L (mm)",                min_value=0.0, value=st.session_state.get("s_L",  0.0), key="s_L")
    with col2:
        s_E  = st.number_input("Elastic Modulus E (MPa)",      min_value=0.0, value=st.session_state.get("s_E",  0.0), key="s_E")
        s_sa = st.number_input("Allowable Stress σ_allow (MPa)", min_value=0.0, value=st.session_state.get("s_sa", 0.0), key="s_sa")

    if st.button("⚙️ Calculate", key="calc_stress"):
        if s_P and s_A and s_L and s_E:
            sig   = s_P / s_A
            eps   = sig / s_E
            delta = s_P * s_L / (s_A * s_E)
            sf    = s_sa / sig if s_sa else None

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Normal Stress σ",  f"{sig:.2f} MPa")
            c2.metric("Axial Strain ε",   f"{eps*1000:.4f} ×10⁻³")
            c3.metric("Deformation δ",    f"{delta:.4f} mm")
            c4.metric("Safety Factor",    f"{sf:.2f}" if sf else "N/A")

            if s_sa:
                if sig <= s_sa:
                    st.markdown(f'<div class="result-safe">✓ SAFE — σ = {sig:.1f} MPa ≤ σ_allow = {s_sa} MPa. Safety factor: {sf:.2f}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-unsafe">✗ UNSAFE — σ = {sig:.1f} MPa exceeds σ_allow = {s_sa} MPa. Increase cross-section area.</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all required fields.")


# ── TAB 2: SHEAR STRESS ───────────────────────────────────────────────────────
with tab2:
    st.subheader("Direct Shear & Bearing Stress")
    st.markdown('<div class="formula-box">τ = V / (n · A_bolt) &nbsp;|&nbsp; σ_b = P / (t · d)</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — Single-shear bolt, V=30 kN, d=16 mm, t=10 mm"):
        if st.button("Fill example values", key="ex_shear"):
            st.session_state.sh_V  = 30000.0
            st.session_state.sh_d  = 16.0
            st.session_state.sh_n  = 1
            st.session_state.sh_t  = 10.0
            st.session_state.sh_ta = 100.0

    col1, col2 = st.columns(2)
    with col1:
        sh_V  = st.number_input("Shear Force V (N)",            min_value=0.0, value=st.session_state.get("sh_V",  0.0), key="sh_V")
        sh_d  = st.number_input("Bolt / Pin Diameter d (mm)",   min_value=0.0, value=st.session_state.get("sh_d",  0.0), key="sh_d")
        sh_n  = st.number_input("Number of Shear Planes",       min_value=1,   value=st.session_state.get("sh_n",  1),   key="sh_n", step=1)
    with col2:
        sh_t  = st.number_input("Plate Thickness t (mm)",       min_value=0.0, value=st.session_state.get("sh_t",  0.0), key="sh_t")
        sh_ta = st.number_input("Allowable Shear Stress (MPa)", min_value=0.0, value=st.session_state.get("sh_ta", 0.0), key="sh_ta")

    if st.button("⚙️ Calculate", key="calc_shear"):
        if sh_V and sh_d:
            A_sh  = sh_n * math.pi * sh_d**2 / 4
            tau   = sh_V / A_sh
            sig_b = sh_V / (sh_t * sh_d) if sh_t else 0
            sf    = sh_ta / tau if sh_ta else None

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Shear Stress τ",   f"{tau:.2f} MPa")
            c2.metric("Bearing Stress σ_b", f"{sig_b:.2f} MPa")
            c3.metric("Shear Area",       f"{A_sh:.2f} mm²")
            c4.metric("Safety Factor",    f"{sf:.2f}" if sf else "N/A")

            if sh_ta:
                if tau <= sh_ta:
                    st.markdown(f'<div class="result-safe">✓ SAFE — τ = {tau:.1f} MPa ≤ τ_allow = {sh_ta} MPa. Safety factor: {sf:.2f}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-unsafe">✗ UNSAFE — τ = {tau:.1f} MPa exceeds τ_allow = {sh_ta} MPa. Use larger bolt or add shear planes.</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all required fields.")


# ── TAB 3: BEAM BENDING ───────────────────────────────────────────────────────
with tab3:
    st.subheader("Beam Bending Stress — Flexure Formula")
    st.markdown('<div class="formula-box">σ_max = M·c / I &nbsp;|&nbsp; I_rect = bh³/12 &nbsp;|&nbsp; I_circ = πd⁴/64</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — SS beam, UDL 12 kN/m, 80×120 mm, L=3 m, E=70 GPa"):
        if st.button("Fill example values", key="ex_beam"):
            st.session_state.b_L    = 3000.0
            st.session_state.b_w    = 12.0
            st.session_state.b_b    = 80.0
            st.session_state.b_h    = 120.0
            st.session_state.b_E    = 70000.0

    col1, col2 = st.columns(2)
    with col1:
        b_L    = st.number_input("Beam Length L (mm)",    min_value=0.0, value=st.session_state.get("b_L", 0.0), key="b_L")
        b_load = st.selectbox("Load Configuration", [
            "UDL — Simply Supported",
            "Point Load at Midspan (SS)",
            "Point Load at Free End (Cantilever)",
            "UDL — Cantilever"
        ])
        b_w    = st.number_input("Load Magnitude (kN/m or kN)", min_value=0.0, value=st.session_state.get("b_w", 0.0), key="b_w")
    with col2:
        b_sec  = st.selectbox("Section Type", ["Rectangular (b × h)", "Circular (diameter d)"])
        b_E    = st.number_input("Elastic Modulus E (MPa)", min_value=0.0, value=st.session_state.get("b_E", 0.0), key="b_E")
        if "Rectangular" in b_sec:
            b_b = st.number_input("Width b (mm)",  min_value=0.0, value=st.session_state.get("b_b", 0.0), key="b_b")
            b_h = st.number_input("Height h (mm)", min_value=0.0, value=st.session_state.get("b_h", 0.0), key="b_h")
        else:
            b_d = st.number_input("Diameter d (mm)", min_value=0.0, value=0.0, key="b_d")

    if st.button("⚙️ Calculate", key="calc_beam"):
        if b_L and b_w:
            wN = b_w * 1000
            if "Rectangular" in b_sec:
                I = b_b * b_h**3 / 12; c = b_h / 2
            else:
                I = math.pi * b_d**4 / 64; c = b_d / 2

            if "UDL — Simply"    in b_load: M = wN * b_L**2 / 8 / 1e6;       defl = 5*wN*b_L**4/(384*b_E*I)
            elif "Midspan"       in b_load: M = wN*1000*b_L / 4 / 1e6;        defl = wN*1000*b_L**3/(48*b_E*I)
            elif "Free End"      in b_load: M = wN*1000*b_L / 1e6;            defl = wN*1000*b_L**3/(3*b_E*I)
            else:                           M = wN * b_L**2 / 2 / 1e6;        defl = wN*b_L**4/(8*b_E*I)

            sig = M * 1e6 * c / I

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Max Moment M",    f"{M:.3f} kN·m")
            c2.metric("Second Moment I", f"{I/1e6:.4f} ×10⁶ mm⁴")
            c3.metric("Bending Stress σ", f"{sig:.2f} MPa")
            c4.metric("Max Deflection δ", f"{defl:.4f} mm")
        else:
            st.warning("Please fill in all required fields.")


# ── TAB 4: TORSION ────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Torsion in Circular Shafts")
    st.markdown('<div class="formula-box">τ_max = T·r / J &nbsp;|&nbsp; φ = TL / GJ &nbsp;|&nbsp; J_solid = πd⁴/32</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — Solid steel shaft, T=800 N·m, d=40 mm, L=1.2 m, G=80 GPa, n=1200 rpm"):
        if st.button("Fill example values", key="ex_torsion"):
            st.session_state.t_T  = 800.0
            st.session_state.t_do = 40.0
            st.session_state.t_L  = 1200.0
            st.session_state.t_G  = 80000.0
            st.session_state.t_n  = 1200.0

    col1, col2 = st.columns(2)
    with col1:
        t_T    = st.number_input("Torque T (N·m)",          min_value=0.0, value=st.session_state.get("t_T",  0.0), key="t_T")
        t_type = st.selectbox("Shaft Type", ["Solid", "Hollow"])
        t_do   = st.number_input("Outer Diameter d_o (mm)", min_value=0.0, value=st.session_state.get("t_do", 0.0), key="t_do")
        if t_type == "Hollow":
            t_di = st.number_input("Inner Diameter d_i (mm)", min_value=0.0, value=0.0, key="t_di")
    with col2:
        t_L    = st.number_input("Length L (mm)",           min_value=0.0, value=st.session_state.get("t_L",  0.0), key="t_L")
        t_G    = st.number_input("Shear Modulus G (MPa)",   min_value=0.0, value=st.session_state.get("t_G",  0.0), key="t_G")
        t_n    = st.number_input("Speed n (rpm)",           min_value=0.0, value=st.session_state.get("t_n",  0.0), key="t_n")

    if st.button("⚙️ Calculate", key="calc_torsion"):
        if t_T and t_do and t_L and t_G:
            T_Nmm = t_T * 1000
            if t_type == "Solid":
                J = math.pi * t_do**4 / 32
            else:
                J = math.pi * (t_do**4 - t_di**4) / 32

            tau  = T_Nmm * (t_do / 2) / J
            phi  = T_Nmm * t_L / (t_G * J) * 180 / math.pi
            omega = 2 * math.pi * t_n / 60
            power = T_Nmm / 1000 * omega / 1000

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Polar Moment J",     f"{J/1000:.2f} ×10³ mm⁴")
            c2.metric("Shear Stress τ_max", f"{tau:.2f} MPa")
            c3.metric("Angle of Twist φ",   f"{phi:.4f}°")
            c4.metric("Power Transmitted",  f"{power:.2f} kW")
        else:
            st.warning("Please fill in all required fields.")


# ── TAB 5: COLUMN BUCKLING ────────────────────────────────────────────────────
with tab5:
    st.subheader("Euler Column Buckling")
    st.markdown('<div class="formula-box">P_cr = π²EI / (KL)² &nbsp;|&nbsp; λ = KL / r &nbsp;|&nbsp; r = √(I/A)</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — Pin–pin steel column, P=200 kN, L=3 m, 80×80 mm, E=200 GPa"):
        if st.button("Fill example values", key="ex_buckling"):
            st.session_state.k_P = 200000.0
            st.session_state.k_L = 3000.0
            st.session_state.k_b = 80.0
            st.session_state.k_h = 80.0
            st.session_state.k_E = 200000.0

    col1, col2 = st.columns(2)
    with col1:
        k_P  = st.number_input("Applied Load P (N)",    min_value=0.0, value=st.session_state.get("k_P", 0.0), key="k_P")
        k_L  = st.number_input("Column Length L (mm)",  min_value=0.0, value=st.session_state.get("k_L", 0.0), key="k_L")
        k_ec = st.selectbox("End Conditions", [
            "Pin – Pin (K = 1.0)",
            "Fixed – Fixed (K = 0.5)",
            "Fixed – Free (K = 2.0)",
            "Fixed – Pin (K = 0.7)"
        ])
    with col2:
        k_b  = st.number_input("Section Width b (mm)",  min_value=0.0, value=st.session_state.get("k_b", 0.0), key="k_b")
        k_h  = st.number_input("Section Height h (mm)", min_value=0.0, value=st.session_state.get("k_h", 0.0), key="k_h")
        k_E  = st.number_input("Elastic Modulus E (MPa)", min_value=0.0, value=st.session_state.get("k_E", 0.0), key="k_E")

    K_map = {"Pin – Pin (K = 1.0)": 1.0, "Fixed – Fixed (K = 0.5)": 0.5, "Fixed – Free (K = 2.0)": 2.0, "Fixed – Pin (K = 0.7)": 0.7}

    if st.button("⚙️ Calculate", key="calc_buckling"):
        if k_P and k_L and k_b and k_h and k_E:
            K   = K_map[k_ec]
            I   = k_b * k_h**3 / 12
            A   = k_b * k_h
            r   = math.sqrt(I / A)
            KL  = K * k_L
            Pcr = math.pi**2 * k_E * I / KL**2
            lam = KL / r
            sf  = Pcr / k_P

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Critical Load P_cr",  f"{Pcr/1000:.2f} kN")
            c2.metric("Slenderness Ratio λ", f"{lam:.1f}")
            c3.metric("Effective Length KL", f"{KL:.0f} mm")
            c4.metric("Safety Factor",       f"{sf:.2f}")

            if k_P < Pcr:
                st.markdown(f'<div class="result-safe">✓ SAFE against buckling — P = {k_P/1000:.1f} kN &lt; P_cr = {Pcr/1000:.1f} kN. Safety factor: {sf:.2f}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-unsafe">✗ BUCKLES — Applied load exceeds P_cr = {Pcr/1000:.1f} kN. Increase section size, reduce length, or improve end conditions.</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all required fields.")


# ── TAB 6: COMBINED LOADING ───────────────────────────────────────────────────
with tab6:
    st.subheader("Combined Bending & Torsion — von Mises Criterion")
    st.markdown('<div class="formula-box">σ_b = 32M / πd³ &nbsp;|&nbsp; τ = 16T / πd³ &nbsp;|&nbsp; σ_vm = √(σ_b² + 3τ²)</div>', unsafe_allow_html=True)

    with st.expander("📌 Load Example — Steel shaft d=50 mm, M=500 N·m, T=700 N·m, σ_y=300 MPa"):
        if st.button("Fill example values", key="ex_combined"):
            st.session_state.c_M  = 500.0
            st.session_state.c_T  = 700.0
            st.session_state.c_d  = 50.0
            st.session_state.c_sy = 300.0

    col1, col2 = st.columns(2)
    with col1:
        c_M  = st.number_input("Bending Moment M (N·m)", min_value=0.0, value=st.session_state.get("c_M",  0.0), key="c_M")
        c_T  = st.number_input("Torque T (N·m)",         min_value=0.0, value=st.session_state.get("c_T",  0.0), key="c_T")
    with col2:
        c_d  = st.number_input("Shaft Diameter d (mm)",  min_value=0.0, value=st.session_state.get("c_d",  0.0), key="c_d")
        c_sy = st.number_input("Yield Strength σ_y (MPa)", min_value=0.0, value=st.session_state.get("c_sy", 0.0), key="c_sy")

    if st.button("⚙️ Calculate", key="calc_combined"):
        if c_M and c_T and c_d and c_sy:
            M_Nmm  = c_M * 1000
            T_Nmm  = c_T * 1000
            sig_b  = 32 * M_Nmm / (math.pi * c_d**3)
            tau    = 16 * T_Nmm / (math.pi * c_d**3)
            vm     = math.sqrt(sig_b**2 + 3 * tau**2)
            sf     = c_sy / vm

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Bending Stress σ_b", f"{sig_b:.2f} MPa")
            c2.metric("Torsional Stress τ", f"{tau:.2f} MPa")
            c3.metric("von Mises σ_vm",     f"{vm:.2f} MPa")
            c4.metric("Safety Factor",      f"{sf:.2f}")

            if vm <= c_sy:
                st.markdown(f'<div class="result-safe">✓ SAFE — von Mises stress ({vm:.1f} MPa) ≤ yield strength ({c_sy} MPa). Safety factor: {sf:.2f}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-unsafe">✗ YIELDS — von Mises stress ({vm:.1f} MPa) exceeds yield strength. Increase shaft diameter or reduce loads.</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in all required fields.")


st.divider()
st.caption("Strength of Materials Calculator · All calculations are for educational purposes. Always verify critical designs with a licensed engineer.")
