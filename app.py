import streamlit as st

st.set_page_config(page_title="Fertirriego Avanzado - Pro", page_icon="🌱", layout="wide")

st.title("🌱 Software Profesional de Fertirriego (Balance de Nitrato y Amonio 80/20)")
st.write("Cálculo matemático exacto basado en PPM de óxidos y distribución lógica por tanques de bodega.")

# ==========================================
# BASE DE DATOS OFICIAL DE FERTILIZANTES (Riquezas y Fracciones N)
# ==========================================
FERTILIZANTES_DB = {
    "YaraLiva CALCINIT": {
        "riqueza": 26.5,  # % CaO
        "NO3": 14.4, "NH4": 1.1
    },
    "Sulfato de Potasio (Solupotasse)": {
        "riqueza": 51.0,  # % K2O
        "NO3": 0.0, "NH4": 0.0
    },
    "Nitrato Potásico (Master 15-5-30)": {
        "riqueza": 30.0,  # % K2O
        "NO3": 8.4, "NH4": 6.6
    },
    "Fosfato Dipotásico (Haifa)": {
        "riqueza": 54.0,  # % K2O
        "NO3": 0.0, "NH4": 0.0
    },
    "Fosfato Monopotásico (MKP)": {
        "riqueza": 52.0,  # % P2O5 estándar soluble
        "NO3": 0.0, "NH4": 0.0
    },
    "Sulfato de Magnesio": {
        "riqueza": 16.0,  # % MgO
        "NO3": 0.0, "NH4": 0.0
    },
    "Nitrato de Magnesio": {
        "riqueza": 15.0,  # % MgO
        "NO3": 11.0, "NH4": 0.0
    },
    "Nitrato de Amonio (Compensador)": {
        "NO3": 17.0, "NH4": 17.0
    }
}

# ==========================================
# FUNCIONES NÚCLEO DE CÁLCULO MÁTEMATICO
# ==========================================
def calcular_gramos(ppm_oxido, grado_fertilizante, volumen):
    if grado_fertilizante <= 0:
        return 0.0
    return (ppm_oxido * volumen * 0.1) / grado_fertilizante

def calcular_ppm_aportadas(gramos, grado_fertilizante, volumen):
    if volumen <= 0:
        return 0.0
    return (gramos * grado_fertilizante) / (volumen * 0.1)

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y FUENTES
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

st.sidebar.header("📦 Selección de Fuentes en Bodega")
opcion_k = st.sidebar.selectbox(
    "Fuente de Potasio (K₂O):",
    ["Sulfato de Potasio (Solupotasse)", "Nitrato Potásico (Master 15-5-30)", "Fosfato Dipotásico (Haifa)"]
)

opcion_mg = st.sidebar.selectbox(
    "Fuente de Magnesio (MgO):",
    ["Sulfato de Magnesio", "Nitrato de Magnesio"]
)

# ==========================================
# PANEL PRINCIPAL: ENTRADA DE REQUERIMIENTOS (PPM ÓXIDOS)
# ==========================================
st.header("🧪 Requerimientos Nutricionales del Cultivo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ppm_n_objetivo = st.number_input("PPM Nitrógeno Total (NT) Deseado:", value=202.9, step=5.0)
    ppm_cao = st.number_input("PPM Óxido de Calcio (CaO) deseadas:", value=241.2, step=1.0)
    
with col2:
    ppm_p2o5 = st.number_input("PPM Pentóxido de Fósforo (P₂O₅) deseadas:", value=97.0, step=1.0)
    ppm_k2o = st.number_input("PPM Óxido de Potasio (K₂O) deseadas:", value=278.7, step=1.0)

with col3:
    ppm_mgo = st.number_input("PPM Óxido de Magnesio (MgO) deseadas:", value=72.0, step=1.0)
    ppm_b = st.number_input("PPM Boro (B):", value=0.92, format="%.2f")

with col4:
    ppm_zn = st.number_input("PPM Zinc (Zn):", value=0.33, format="%.2f")
    ppm_cu = st.number_input("PPM Cobre (Cu):", value=0.06, format="%.2f")

# Distribución técnica requerida de Nitrógeno (80% Nitrato / 20% Amonio)
ppm_no3_target = ppm_n_objetivo * 0.80
ppm_nh4_target = ppm_n_objetivo * 0.20

# Variables para rastrear aportes de Nitrógeno en tiempo real
ppm_no3_acumulado = 0.0
ppm_nh4_acumulado = 0.0

# ==========================================
# MATRIZ DE BALANCE LOGÍCO DE ELEMENTOS
# ==========================================

# 1. Calcio (YaraLiva CALCINIT -> Tanque A)
db_calcinit = FERTILIZANTES_DB["YaraLiva CALCINIT"]
g_calcinit = calcular_gramos(ppm_cao, db_calcinit["riqueza"], volumen_agua)
no3_calcinit = calcular_ppm_aportadas(g_calcinit, db_calcinit["NO3"], volumen_agua)
nh4_calcinit = calcular_ppm_aportadas(g_calcinit, db_calcinit["NH4"], volumen_agua)
ppm_no3_acumulado += no3_calcinit
ppm_nh4_acumulado += nh4_calcinit

# 2. Potasio (Selección de menú)
g_solu_k, g_master, g_haifa_k = 0.0, 0.0, 0.0
no3_master, nh4_master = 0.0, 0.0

if opcion_k == "Sulfato de Potasio (Solupotasse)":
    db_solu = FERTILIZANTES_DB["Sulfato de Potasio (Solupotasse)"]
    g_solu_k = calcular_gramos(ppm_k2o, db_solu["riqueza"], volumen_agua)
elif opcion_k == "Nitrato Potásico (Master 15-5-30)":
    db_master = FERTILIZANTES_DB["Nitrato Potásico (Master 15-5-30)"]
    g_master = calcular_gramos(ppm_k2o, db_master["riqueza"], volumen_agua)
    no3_master = calcular_ppm_aportadas(g_master, db_master["NO3"], volumen_agua)
    nh4_master = calcular_ppm_aportadas(g_master, db_master["NH4"], volumen_agua)
    ppm_no3_acumulado += no3_master
    ppm_nh4_acumulado += nh4_master
elif opcion_k == "Fosfato Dipotásico (Haifa)":
    db_haifa = FERTILIZANTES_DB["Fosfato Dipotásico (Haifa)"]
    g_haifa_k = calcular_gramos(ppm_k2o, db_haifa["riqueza"], volumen_agua)

# 3. Magnesio (Selección de menú sin condicionales sueltos que causen error)
g_sulf_mg, g_nit_mg = 0.0, 0.0
no3_nitmag = 0.0

if opcion_mg == "Sulfato de Magnesio":
    db_sulf_mg = FERTILIZANTES_DB["Sulfato de Magnesio"]
    g_sulf_mg = calcular_gramos(ppm_mgo, db_sulf_mg["riqueza"], volumen_agua)
elif opcion_mg == "Nitrato de Magnesio":
    db_nit_mg = FERTILIZANTES_DB["Nitrato de Magnesio"]
    g_nit_mg = calcular_gramos(ppm_mgo, db_nit_mg["riqueza"], volumen_agua)
    no3_nitmag = calcular_ppm_aportadas(g_nit_mg, db_nit_mg["NO3"], volumen_agua)
    ppm_no3_acumulado += no3_nitmag

# 4. Fósforo Base (Fosfato Monopotásico MKP -> Tanque B)
db_mkp = FERTILIZANTES_DB["Fosfato Monopotásico (MKP)"]
g_fosfato_mono = calcular_gramos(ppm_p2o5, db_mkp["riqueza"], volumen_agua)

# 5. Compensación de Faltantes con Nitrato de Amonio
ppm_no3_faltante = max(0.0, ppm_no3_target - ppm_no3_acumulado)
ppm_nh4_faltante = max(0.0, ppm_nh4_target - ppm_nh4_acumulado)

# Se equilibra usando la mayor deficiencia fraccionada
ppm_compensar_n = max(ppm_no3_faltante, ppm_nh4_faltante)
g_nitrato_amonio = 0.0
no3_nit_amonio, nh4_nit_amonio = 0.0, 0.0

if ppm_compensar_n > 0:
    db_amonio = FERTILIZANTES_DB["Nitrato de Amonio (Compensador)"]
    g_nitrato_amonio = calcular_gramos(ppm_compensar_n, db_amonio["NO3"], volumen_agua)
    no3_nit_amonio = calcular_ppm_aportadas(g_nitrato_amonio, db_amonio["NO3"], volumen_agua)
    nh4_nit_amonio = calcular_ppm_aportadas(g_nitrato_amonio, db_amonio["NH4"], volumen_agua)
    ppm_no3_acumulado += no3_nit_amonio
    ppm_nh4_acumulado += nh4_nit_amonio

# 6. Micronutrientes (Gramos directos)
g_boro = calcular_gramos(ppm_b, 20.5, volumen_agua)
g_zinc = calcular_gramos(ppm_zn, 13.0, volumen_agua)
g_cobre = calcular_gramos(ppm_cu, 12.0, volumen_agua)
g_manganeso = calcular_gramos(2.47, 12.0, volumen_agua)
g_molibdato = calcular_gramos(0.19, 10.0, volumen_agua)

# ==========================================
# SECCIÓN VISUAL: PANTALLA DE CONTROL METRICO
# ==========================================
st.markdown("---")
st.header("📊 Cuadro de Control y Auditoría de Nitrógeno (Fracción 80% NO₃⁻ / 20% NH₄⁺)")

c_meta, c_no3, c_nh4 = st.columns(3)
with c_meta:
    st.metric("Meta Nitrógeno Total", f"{ppm_n_objetivo} PPM")
with c_no3:
    st.metric("Nitrato (NO₃⁻) Logrado vs Meta", f"{ppm_no3_acumulado:.1f} / {ppm_no3_target:.1f} PPM")
with c_nh4:
    st.metric("Amonio (NH₄⁺) Logrado vs Meta", f"{ppm_nh4_acumulado:.1f} / {ppm_nh4_target:.1f} PPM")

# ==========================================
# DOSIFICACIÓN DE BODEGA SEPARADA POR TANQUES COMPATIBLES
# ==========================================
st.header("📋 Dosificación Recomendada por Tanques")

tab1, tab2 = st.tabs(["🛢️ TANQUE A (YaraLiva + Nitratos)", "🛢️ TANQUE B (Fósforo, Sulfatos y Micros)"])

with tab1:
    st.subheader("Solución Concentrada A - Reactivos de Calcio")
    st.markdown(f"• **YaraLiva CALCINIT (26.5% CaO):** `{g_calcinit / 1000:.2f} Kg`  \n *Aporte Real: {no3_calcinit:.1f} PPM NO₃⁻ | {nh4_calcinit:.1f} PPM NH₄⁺*")
    
    if g_master > 0:
        st.markdown(f"• **Nitrato Potásico (Master 15-5-30):** `{g_master / 1000:.2f} Kg`  \n *Aporte Real: {no3_master:.1f} PPM NO₃⁻ | {nh4_master:.1f} PPM NH₄⁺*")
    
    if g_nitrato_amonio > 0:
        st.markdown(f"• **Nitrato de Amonio (Compensador Balance):** `{g_nitrato_amonio / 1000:.2f} Kg` ⚖️  \n *Aporte de Ajuste: {no3_nit_amonio:.1f} PPM NO₃⁻ | {nh4_nit_amonio:.1f} PPM NH₄⁺*")
    
    st.caption("⚠️ Nota: Mantén este tanque libre de fósforo y sulfatos para prevenir la precipitación de yeso e incrustaciones químicas.")

with tab2:
    st.subheader("Solución Concentrada B - Reactivos de Fondo y Microelementos")
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("**Macronutrientes:**")
        st.write(f"• **Fosfato Monopotásico (MKP - 52% P₂O₅):** `{g_fosfato_mono / 1000:.2f} Kg` *(Aporta tus {ppm_p2o5} PPM de P₂O₅)*")
        
        if g_solu_k > 0:
            st.write(f"• **Sulfato Potásico (Solupotasse - 51% K₂O):** `{g_solu_k / 1000:.2f} Kg`")
        if g_haifa_k > 0:
            st.write(f"• **Fosfato Dipotásico (Haifa - 54% K₂O):** `{g_haifa_k / 1000:.2f} Kg`")
        if g_sulf_mg > 0:
            st.write(f"• **Sulfato de Magnesio (16% MgO):** `{g_sulf_mg / 1000:.2f} Kg`")
        if g_nit_mg > 0:
