import streamlit as st

# Configuración estética de la app web
st.set_page_config(page_title="Fertirriego Pro", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego Avanzado")
st.write("Cálculos instantáneos basados en PPM elementales y factores de conversión óxido.")

# Factores de conversión oficiales (según tu manual Nutriterra)
FACTORES = {
    "P_a_P2O5": 2.293,
    "K_a_K2O": 1.205,
    "Ca_a_CaO": 1.399,
    "Mg_a_MgO": 1.658,
    "S_a_SO3": 2.500
}

# Fórmula maestra de tus apuntes
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
    st.sidebar.success(f"Volumen calculated: {volumen_agua:,.0f} Litros")

# ==========================================
# PANEL PRINCIPAL: MACRONUTRIENTES
# ==========================================
st.header("🧪 Macronutrientes (PPM Requeridas)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Calcio (Ca)")
    ppm_ca = st.number_input("PPM Ca deseadas:", value=172.3, step=1.0)
    grado_ca = st.number_input("% CaO (Calcinit):", value=26.5)
    
    ppm_cao = ppm_ca * FACTORES["Ca_a_CaO"]
    kg_calcinit = calcular_gramos(ppm_cao, grado_ca, volumen_agua) / 1000
    st.metric("Calcinit Necesario", f"{kg_calcinit:.2f} Kg")

with col2:
    st.subheader("Fósforo (P)")
    ppm_p = st.number_input("PPM P deseadas:", value=43.0, step=1.0)
    grado_p = st.number_input("% P2O5 (Haifa):", value=41.0)
    
    ppm_p2o5 = ppm_p * FACTORES["P_a_P2O5"]
    kg_fosfato = calcular_gramos(ppm_p2o5, grado_p, volumen_agua) / 1000
    st.metric("Fosfato Necesario", f"{kg_fosfato:.2f} Kg")

with col3:
    st.subheader("Potasio (K)")
    ppm_k = st.number_input("PPM K deseadas:", value=70.0, step=1.0)
    grado_k = st.number_input("% K2O (Solupotasse):", value=50.0)
    
    ppm_k2o = ppm_k * FACTORES["K_a_K2O"]
    kg_potasio = calcular_gramos(ppm_k2o, grado_k, volumen_agua) / 1000
    st.metric("Sulfato K Necesario", f"{kg_potasio:.2f} Kg")

with col4:
    st.subheader("Magnesio (Mg)")
    ppm_mg = st.number_input("PPM Mg deseadas:", value=45.0, step=1.0)
    grado_mg = st.number_input("% MgO (Sulfato Mg):", value=16.0)
    
    ppm_mgo = ppm_mg * FACTORES["Mg_a_MgO"]
    kg_magnesio = calcular_gramos(ppm_mgo, grado_mg, volumen_agua) / 1000
    st.metric("Sulfato Mg Necesario", f"{kg_magnesio:.2f} Kg")

# ==========================================
# PANEL SECUNDARIO: MICRONUTRIENTES (EDTA)
# ==========================================
st.markdown("---")
st.header("🔬 Micronutrientes (EDTA / Quelatos)")

col_b, col_zn, col_mn, col_mo = st.columns(4)

with col_b:
    ppm_b = st.number_input("PPM Boro (B):", value=0.76, format="%.2f")
    porcentaje_b = st.number_input("% Boro en producto:", value=20.5, key="b_pct")
    g_boro = calcular_gramos(ppm_b, porcentaje_b, volumen_agua)
    st.metric("Klip Boro Requerido", f"{g_boro:.1f} g")

with col_zn:
    ppm_zn = st.number_input("PPM Zinc (Zn):", value=0.30, format="%.2f")
    porcentaje_zn = st.number_input("% Zinc en producto:", value=13.0, key="zn_pct")
    g_zinc = calcular_gramos(ppm_zn, porcentaje_zn, volumen_agua)
    st.metric("Zinc EDTA Requerido", f"{g_zinc:.1f} g")

with col_mn:
    ppm_mn = st.number_input("PPM Manganeso (Mn):", value=2.00, format="%.2f")
    porcentaje_mn = st.number_input("% Mn en producto:", value=12.0, key="mn_pct")
    g_mn = calcular_gramos(ppm_mn, porcentaje_mn, volumen_agua)
    st.metric("Manganeso EDTA", f"{g_mn:.1f} g")

with col_mo:
    ppm_mo = st.number_input("PPM Molibdeno (Mo):", value=0.19, format="%.2f")
    porcentaje_mo = st.number_input("% Mo en producto:", value=10.0, key="mo_pct")
    g_mo = calcular_gramos(ppm_mo, porcentaje_mo, volumen_agua)
    st.metric("Molibdato Requerido", f"{g_mo:.1f} g")
