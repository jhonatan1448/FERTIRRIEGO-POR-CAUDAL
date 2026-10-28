import streamlit as st

st.set_page_config(page_title="Fertirriego Pro - Inteligente", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego con Menú de Selección")
st.write("Selecciona tus fertilizantes disponibles en bodega y calcula la receta exacta al instante.")

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
    st.sidebar.success(f"Volumen calculado: {volumen_agua:,.0f} Litros")

# ==========================================
# SELECCIÓN DE FERTILIZANTES EN BODEGA (MENÚS)
# ==========================================
st.sidebar.header("📦 Fertilizantes Disponibles")

# Menú interactivo para Potasio (K)
opcion_k = st.sidebar.selectbox(
    "Fuente de Potasio (K):",
    ["Sulfato de Potasio (Solupotasse)", "Nitrato Potásico (Master 15-5-30)", "Fosfato Dipotásico (Haifa)"]
)

# Menú interactivo para Magnesio (Mg)
opcion_mg = st.sidebar.selectbox(
    "Fuente de Magnesio (Mg):",
    ["Sulfato de Magnesio", "Nitrato de Magnesio"]
)

# ==========================================
# PANEL PRINCIPAL: ENTRADA DE REQUERIMIENTOS (PPM)
# ==========================================
st.header("🧪 Requerimientos Nutricionales del Cultivo (PPM Elementales)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ppm_ca = st.number_input("PPM Calcio (Ca) deseadas:", value=172.3, step=1.0)
    ppm_mg = st.number_input("PPM Magnesio (Mg) deseadas:", value=45.0, step=1.0)

with col2:
    ppm_p = st.number_input("PPM Fósforo (P) deseadas:", value=43.0, step=1.0)
    ppm_k = st.number_input("PPM Potasio (K) deseadas:", value=232.3, step=1.0)

with col3:
    ppm_b = st.number_input("PPM Boro (B):", value=0.92, format="%.2f")
    ppm_zn = st.number_input("PPM Zinc (Zn):", value=0.33, format="%.2f")

with col4:
    ppm_mn = st.number_input("PPM Manganeso (Mn):", value=2.47, format="%.2f")
    ppm_mo = st.number_input("PPM Molibdeno (Mo):", value=0.19, format="%.2f")

# ==========================================
# LÓGICA DE CONVERSIONES ÓXIDO
# ==========================================
ppm_cao = ppm_ca * FACTORES["Ca_a_CaO"]
ppm_p2o5 = ppm_p * FACTORES["P_a_P2O5"]
ppm_mgo = ppm_mg * FACTORES["Mg_a_MgO"]
ppm_k2o = ppm_k * FACTORES["K_a_K2O"]

# ==========================================
# DESPLIEGUE VISUAL POR TANQUES COMPATIBLES
# ==========================================
st.markdown("---")
st.header("📋 Receta Dinámica Distribuida por Tanques")

tab1, tab2 = st.tabs(["🛢️ TANQUE A (Calcio y Nitratos)", "🛢️ TANQUE B (Fósforo, Sulfatos y Micros)"])

with tab1:
    st.subheader("Nutrientes Concentrados")
    
    # Calcinit va por defecto en el Tanque A
    g_calcinit = calcular_gramos(ppm_cao, 26.5, volumen_agua)
    st.write(f"• **Nitrato Cálcico (Calcinit):** `{g_calcinit / 1000:.2f} Kg` *(Aporta {ppm_ca} PPM de Ca)*")
    
    # Si seleccionas Master en la barra lateral, aparece en el Tanque A (por compatibilidad)
    if opcion_k == "Nitrato Potásico (Master 15-5-30)":
        g_master = calcular_gramos(ppm_k2o, 30.0, volumen_agua)
        st.write(f"• **Nitrato Potásico (Master 15-5-30):** `{g_master / 1000:.2f} Kg` *(Aporta {ppm_k} PPM de K)*")
        st.info("💡 El Nitrato de Potasio se ha asignado al Tanque A para mantener la solubilidad.")

with tab2:
    st.subheader("Nutrientes de Fondo y Microelementos")
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("**Macronutrientes Seleccionados:**")
        
        # Fósforo Base (Fosfato Monopotásico)
        g_fosfato_mono = calcular_gramos(ppm_p2o5, 41.0, volumen_agua)
        st.write(f"• **Fosfato Monopotásico:** `{g_fosfato_mono / 1000:.2f} Kg`")
        
        # Lógica del menú de Potasio (si no es Master)
        if opcion_k == "Sulfato de Potasio (Solupotasse)":
            g_solu_k = calcular_gramos(ppm_k2o, 50.0, volumen_agua)
            st.write(f"• **Sulfato Potásico (Solupotasse):** `{g_solu_k / 1000:.2f} Kg`")
        elif opcion_k == "Fosfato Dipotásico (Haifa)":
            g_haifa_k = calcular_gramos(ppm_k2o, 54.0, volumen_agua)
            st.write(f"• **Fosfato Dipotásico (Haifa K=54%):** `{g_haifa_k / 1000:.2f} Kg`")

        # Lógica del menú de Magnesio
        if opcion_mg == "Sulfato de Magnesio":
            g_sulf_mg = calcular_gramos(ppm_mgo, 16.0, volumen_agua)
            st.write(f"• **Sulfato de Magnesio (16% MgO):** `{g_sulf_mg / 1000:.2f} Kg`")
        elif opcion_mg == "Nitrato de Magnesio":
            g_nit_mg = calcular_gramos(ppm_mg, 10.67, volumen_agua) # Directo según tus notas
            st.write(f"• **Nitrato de Magnesio (10.67% Mg):** `{g_nit_mg / 1000:.2f} Kg`")

    with col_b2:
        st.markdown("**Micronutrientes Quelatados (Fijos):**")
        g_boro = calcular_gramos(ppm_b, 20.5, volumen_agua)
        g_zinc = calcular_gramos(ppm_zn, 13.0, volumen_agua)
        g_manganeso = calcular_gramos(ppm_mn, 12.0, volumen_agua)
        g_molibdato = calcular_gramos(ppm_mo, 10.0, volumen_agua)
        
        st.write(f"• **Klip Boro:** `{g_boro:.1f} gramos`")
        st.write(f"• **Zinc EDTA:** `{g_zinc:.1f} gramos`")
        st.write(f"• **Manganeso EDTA:** `{g_manganeso:.1f} gramos`")
        st.write(f"• **Molibdato de Sodio:** `{g_molibdato:.1f} gramos`")

st.divider()
st.caption("Estructura de menús reactivos basada en condicionales `if/elif`. Cambia las fuentes en la barra de la izquierda para ver el cambio instantáneo.")
