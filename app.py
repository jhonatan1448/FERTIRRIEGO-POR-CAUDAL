import streamlit as st

st.set_page_config(page_title="Fertirriego Pro - Óxidos", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego Avanzado (PPM en Forma Oxidada)")
st.write("Introduce directamente los requerimientos en óxidos (P₂O₅, K₂O, CaO, MgO) según tus recetas de campo.")

# Fórmula maestra directa de tus apuntes
def calcular_gramos(ppm_oxido, grado_fertilizante, volumen):
    if grado_fertilizante <= 0:
        return 0.0
    return (ppm_oxido * volumen * 0.1) / grado_fertilizante

# ==========================================
# BARRA LATERAL: CONFIGURACIÓN DEL VOLUMEN
# ==========================================
st.sidebar.header("💧 Control de Caudal / Volumen")
metodo_agua = st.sidebar.radio("Método de entrada:", ["Volumen Fijo (Tanque/Ha)", "Caudal Continuo"])

if metodo_agua == "Volumen Fijo (Tanque/Ha)":
    volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=16000, step=1000)
else:
    caudal = st.sidebar.number_input("Caudal del emisor / sistema (L/hora):", min_value=1, value=5000)
    tiempo = st.sidebar.number_input("Tiempo de riego (Horas):", min_value=0.1, value=3.2, step=0.1)
    volumen_agua = caudal * tiempo
    st.sidebar.success(f"Volumen calculado: {volumen_agua:,.0f} Litros")

# ==========================================
# SELECCIÓN DE FERTILIZANTES EN BODEGA (MENÚS)
# ==========================================
st.sidebar.header("📦 Fertilizantes Disponibles")

opcion_k = st.sidebar.selectbox(
    "Fuente de Potasio (K₂O):",
    ["Sulfato de Potasio (Solupotasse)", "Nitrato Potásico (Master 15-5-30)", "Fosfato Dipotásico (Haifa)"]
)

opcion_mg = st.sidebar.selectbox(
    "Fuente de Magnesio (MgO):",
    ["Sulfato de Magnesio", "Nitrato de Magnesio"]
)

# ==========================================
# PANEL PRINCIPAL: ENTRADA EN FORMA OXIDADA
# ==========================================
st.header("🧪 Requerimientos Nutricionales del Cultivo (PPM de Óxidos)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ppm_cao = st.number_input("PPM Óxido de Calcio (CaO) deseadas:", value=241.2, step=1.0, help="Ejemplo: 172.3 Ca × 1.4 = 241.2 CaO")
    ppm_mgo = st.number_input("PPM Óxido de Magnesio (MgO) deseadas:", value=72.0, step=1.0, help="Ejemplo: 45.0 Mg × 1.6 = 72.0 MgO")

with col2:
    ppm_p2o5 = st.number_input("PPM Pentóxido de Fósforo (P₂O₅) deseadas:", value=97.0, step=1.0, help="Ejemplo: 43.0 P × 2.25 = 97.0 P₂O₅")
    ppm_k2o = st.number_input("PPM Óxido de Potasio (K₂O) deseadas:", value=278.7, step=1.0, help="Ejemplo: 232.3 K × 1.2 = 278.7 K₂O")

with col3:
    st.markdown("**Micronutrientes (PPM):**")
    ppm_b = st.number_input("PPM Boro (B):", value=0.92, format="%.2f")
    ppm_zn = st.number_input("PPM Zinc (Zn):", value=0.33, format="%.2f")

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    ppm_mn = st.number_input("PPM Manganeso (Mn):", value=2.47, format="%.2f")
    ppm_mo = st.number_input("PPM Molibdeno (Mo):", value=0.19, format="%.2f")

# ==========================================
# DESPLIEGUE VISUAL POR TANQUES COMPATIBLES
# ==========================================
st.markdown("---")
st.header("📋 Receta Dinámica Distribuida por Tanques")

tab1, tab2 = st.tabs(["🛢️ TANQUE A (Calcio y Nitratos)", "🛢️ TANQUE B (Fósforo, Sulfatos y Micros)"])

with tab1:
    st.subheader("Nutrientes Concentrados")
    
    # Calcinit usa las PPM de CaO directamente
    g_calcinit = calcular_gramos(ppm_cao, 26.5, volumen_agua)
    st.write(f"• **Nitrato Cálcico (Calcinit):** `{g_calcinit / 1000:.2f} Kg` *(Aporta tus {ppm_cao} PPM de CaO)*")
    
    # Lógica si eliges Master 15-5-30 para aportar el K2O en el Tanque A
    if opcion_k == "Nitrato Potásico (Master 15-5-30)":
        g_master = calcular_gramos(ppm_k2o, 30.0, volumen_agua)
        st.write(f"• **Nitrato Potásico (Master 15-5-30):** `{g_master / 1000:.2f} Kg` *(Aporta tus {ppm_k2o} PPM de K₂O)*")
        st.info("💡 El Nitrato de Potasio se ha asignado al Tanque A para mantener la solubilidad.")

with tab2:
    st.subheader("Nutrientes de Fondo y Microelementos")
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("**Macronutrientes Seleccionados:**")
        
        # Fósforo se calcula directo con el P2O5 ingresado
        g_fosfato_mono = calcular_gramos(ppm_p2o5, 41.0, volumen_agua)
        st.write(f"• **Fosfato Monopotásico (41% P₂O₅):** `{g_fosfato_mono / 1000:.2f} Kg` *(Aporta tus {ppm_p2o5} PPM de P₂O₅)*")
        
        # Fuentes alternas de Potasio (calculadas directo con K2O)
        if opcion_k == "Sulfato de Potasio (Solupotasse)":
            g_solu_k = calcular_gramos(ppm_k2o, 50.0, volumen_agua)
            st.write(f"• **Sulfato Potásico (Solupotasse 50% K₂O):** `{g_solu_k / 1000:.2f} Kg` *(Aporta tus {ppm_k2o} PPM de K₂O)*")
        elif opcion_k == "Fosfato Dipotásico (Haifa)":
            g_haifa_k = calcular_gramos(ppm_k2o, 54.0, volumen_agua)
            st.write(f"• **Fosfato Dipotásico (Haifa 54% K₂O):** `{g_haifa_k / 1000:.2f} Kg` *(Aporta tus {ppm_k2o} PPM de K₂O)*")

        # Fuentes de Magnesio (calculadas directo con MgO)
        if opcion_mg == "Sulfato de Magnesio":
            g_sulf_mg = calcular_gramos(ppm_mgo, 16.0, volumen_agua)
            st.write(f"• **Sulfato de Magnesio (16% MgO):** `{g_sulf_mg / 1000:.2f} Kg` *(Aporta tus {ppm_mgo} PPM de MgO)*")
        elif opcion_mg == "Nitrato de Magnesio":
            # Si usas Nitrato de Magnesio comercial, su riqueza común en óxido ronda el 15%-16% MgO
            g_nit_mg = calcular_gramos(ppm_mgo, 15.0, volumen_agua)
            st.write(f"• **Nitrato de Magnesio (Aprox. 15% MgO):** `{g_nit_mg / 1000:.2f} Kg` *(Aporta tus {ppm_mgo} PPM de MgO)*")

    with col_b2:
        st.markdown("**Micronutrientes Quelatados (Fijos en gramos):**")
        g_boro = calcular_gramos(ppm_b, 20.5, volumen_agua)
        g_zinc = calcular_gramos(ppm_zn, 13.0, volumen_agua)
        g_manganeso = calcular_gramos(ppm_mn, 12.0, volumen_agua)
        g_molibdato = calcular_gramos(ppm_mo, 10.0, volumen_agua)
        
        st.write(f"• **Klip Boro (20.5% B):** `{g_boro:.1f} g`")
        st.write(f"• **Zinc EDTA (13% Zn):** `{g_zinc:.1f} g`")
        st.write(f"• **Manganeso EDTA (12% Mn):** `{g_manganeso:.1f} g`")
        st.write(f"• **Molibdato de Sodio (10% Mo):** `{g_molibdato:.1f} g`")

st.divider()
st.caption("Cálculo Directo: Gramos = (PPM Óxido Solicitadas × Volumen Agua × 0.1) / % Riqueza del saco.")
