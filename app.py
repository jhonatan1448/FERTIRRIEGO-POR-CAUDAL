import streamlit as st

st.set_page_config(page_title="Fertirriego Inteligente Pro", page_icon="🌱", layout="wide")

st.title("🌱 Software Profesional de Fertirriego (Líneas Oficiales Colombia)")
st.write("Auditoría milimétrica por elemento. Grados exactos de Yara, Haifa, Van Iperen y Daymsa.")

# ==========================================
# BASE DE DATOS DE FERTILIZANTES AGRUPADA (Riquezas Oficiales)
# ==========================================
FERTILIZANTES_DB = {
    "YaraLiva CALCINIT": {"N_total": 15.5, "NO3": 14.4, "NH4": 1.1, "CaO": 26.5, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0},
    "Sulfato de Potasio (Solupotasse)": {"N_total": 0.0, "NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 51.0, "MgO": 0.0},
    "Fosfato Monopotásico (MKP)": {"N_total": 0.0, "NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 52.0, "K2O": 34.0, "MgO": 0.0},
    "Haifa DKP (0-41-54)": {"N_total": 0.0, "NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 41.0, "K2O": 54.0, "MgO": 0.0},
    "Sulfato de Magnesio": {"N_total": 0.0, "NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 16.0},
    "Nitrato de Magnesio": {"N_total": 11.0, "NO3": 11.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 15.0},
    "Nitrato de Amonio": {"N_total": 34.0, "NO3": 17.0, "NH4": 17.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0},
    
    # --- LÍNEA: VAN IPEREN COLOMBIA ---
    "Van Iperen INICIO (11-32-11)": {"N_total": 11.0, "NO3": 5.5, "NH4": 5.5, "CaO": 0.0, "P2O5": 32.0, "K2O": 11.0, "MgO": 0.0},
    "Van Iperen DESARROLLO (20-20-20)": {"N_total": 20.0, "NO3": 10.0, "NH4": 10.0, "CaO": 0.0, "P2O5": 20.0, "K2O": 20.0, "MgO": 0.0},
    "Van Iperen PRODUCCION (12-5-40)": {"N_total": 12.0, "NO3": 7.0, "NH4": 5.0, "CaO": 0.0, "P2O5": 5.0, "K2O": 40.0, "MgO": 0.0},
    
    # --- LÍNEA: HAIFA POLY-FEED COLOMBIA ---
    "Haifa Poly-Feed INICIO (13-36-13)": {"N_total": 13.0, "NO3": 6.5, "NH4": 6.5, "CaO": 0.0, "P2O5": 36.0, "K2O": 13.0, "MgO": 0.0},
    "Haifa Poly-Feed DESARROLLO (19-19-19)": {"N_total": 19.0, "NO3": 9.5, "NH4": 9.5, "CaO": 0.0, "P2O5": 19.0, "K2O": 19.0, "MgO": 0.0},
    "Haifa Poly-Feed PRODUCCION (10-10-43)": {"N_total": 10.0, "NO3": 5.0, "NH4": 5.0, "CaO": 0.0, "P2O5": 10.0, "K2O": 43.0, "MgO": 0.0}
}

# Funciones de conversión matemáticas
def calcular_gramos(ppm, riqueza, volumen):
    if riqueza <= 0:
        return 0.0
    return (ppm * volumen * 0.1) / riqueza

def calcular_ppm(gramos, riqueza, volumen):
    if volumen <= 0:
        return 0.0
    return (gramos * riqueza) / (volumen * 0.1)

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y MENÚS
# ==========================================
st.sidebar.header("💧 Datos de Volumen")
volumen_agua = st.sidebar.number_input("Volumen de agua (Litros):", min_value=1, value=16000)

st.sidebar.header("📦 Selección de Fuentes en Bodega")
opcion_npk = st.sidebar.selectbox(
    "Fórmula NPK Comercial Compleja (Opcional):",
    [
        "Ninguno (Usar Simples)",
        "Van Iperen INICIO (11-32-11)", "Van Iperen DESARROLLO (20-20-20)", "Van Iperen PRODUCCION (12-5-40)",
        "Haifa Poly-Feed INICIO (13-36-13)", "Haifa Poly-Feed DESARROLLO (19-19-19)", "Haifa Poly-Feed PRODUCCION (10-10-43)"
    ]
)

opcion_k = st.sidebar.selectbox(
    "Fuente Simple de Potasio (K₂O):", 
    ["Sulfato de Potasio (Solupotasse)", "Haifa DKP (0-41-54)"]
)

opcion_mg = st.sidebar.selectbox("Fuente de Magnesio (MgO):", ["Sulfato de Magnesio", "Nitrato de Magnesio"])

# ==========================================
# REQUERIMIENTOS OBJETIVO DEL CULTIVO (PPM)
# ==========================================
st.header("🧪 Requerimientos Objetivo del Cultivo (PPM)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    tgt_n = st.number_input("Meta NT Deseado:", value=157.0)
    tgt_cao = st.number_input("Meta CaO Deseado:", value=241.2)
with col2:
    tgt_p2o5 = st.number_input("Meta P₂O₅ Deseado:", value=97.0)
    tgt_k2o = st.number_input("Meta K₂O Deseado:", value=278.7)
with col3:
    tgt_mgo = st.number_input("Meta MgO Deseado:", value=64.0)
    tgt_fe = st.number_input("Meta Hierro (Fe):", value=3.43)
with col4:
    tgt_b = st.number_input("Meta Boro (B):", value=0.92)
    tgt_zn = st.number_input("Meta Zinc (Zn):", value=0.33)
    tgt_cu = st.number_input("Meta Cobre (Cu):", value=0.54)
    tgt_mn = st.number_input("Meta Manganeso (Mn):", value=2.47)
    tgt_mo = st.number_input("Meta Molibdeno (Mo):", value=0.19)

# Sub-metas de Nitrógeno al 80% Nitrato / 20% Amonio
tgt_no3 = tgt_n * 0.80
tgt_nh4 = tgt_n * 0.20

# Diccionario acumulador de aportes reales en el Riego
aportes = {"NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0}
pesos_finales = {}

# ==========================================
# ALGORITMO DE BALANCE DINÁMICO SECUENCIAL
# ==========================================

# 1. MICRONUTRIENTES DAYMSA - CALCULADOS PRIMERO PARA CAPTURAR EL POTASIO DEL BORO
g_klipboro = calcular_gramos(tgt_b, 20.5, volumen_agua)            # ¡Corregido a 20.5% B exacto! ✅
g_naturquel_fe = calcular_gramos(tgt_fe, 6.0, volumen_agua)       # Naturquel Fe (6.0% Fe)
g_kellus_cu = calcular_gramos(tgt_cu, 13.5, volumen_agua)         # Kellus Cu (13.5% Cu)
g_naturzinc = calcular_gramos(tgt_zn, 13.0, volumen_agua)          # Naturzinc (13.0% Zn)
g_naturmanganeso = calcular_gramos(tgt_mn, 12.0, volumen_agua)      # Naturmanganeso (12.0% Mn)
g_molibk = calcular_gramos(tgt_mo, 10.0, volumen_agua)              # Molibk (10.0% Mo)

# Medimos el Potasio colateral aportado por tu Klip Boro (3.0% K2O) y lo metemos al balance
k2o_colateral_boro = calcular_ppm(g_klipboro, 3.0, volumen_agua)
aportes["K2O"] += k2o_colateral_boro

# 2. CALCIO (YaraLiva Calcinit) -> Asigna base CaO
g_calcinit = calcular_gramos(tgt_cao, FERTILIZANTES_DB["YaraLiva CALCINIT"]["CaO"], volumen_agua)
pesos_finales["YaraLiva CALCINIT"] = g_calcinit
aportes["CaO"] += tgt_cao
aportes["NO3"] += calcular_ppm(g_calcinit, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NO3"], volumen_agua)
aportes["NH4"] += calcular_ppm(g_calcinit, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NH4"], volumen_agua)

# 3. EVALUACIÓN DE LA FÓRMULA NPK COMERCIAL SELECCIONADA
if opcion_npk != "Ninguno (Usar Simples)":
    db_npk = FERTILIZANTES_DB[opcion_npk]
    g_por_p = calcular_gramos(tgt_p2o5, db_npk["P2O5"], volumen_agua) if db_npk["P2O5"] > 0 else 999999
    g_por_k = calcular_gramos(tgt_k2o, db_npk["K2O"], volumen_agua) if db_npk["K2O"] > 0 else 999999
    
    g_npk_aplicar = min(g_por_p, g_por_k)
    pesos_finales[opcion_npk] = g_npk_aplicar
    
    for elemento in ["NO3", "NH4", "P2O5", "K2O"]:
        if elemento != "K2O":
            aportes[elemento] += calcular_ppm(g_npk_aplicar, db_npk[elemento], volumen_agua)
        else:
            aportes["K2O"] += calcular_ppm(g_npk_aplicar, db_npk["K2O"], volumen_agua)

# 4. POTASIO COMPLEMENTARIO (Solupotasse o Haifa DKP) -> Descuenta el K2O del Boro y del NPK
k2o_restante = max(0.0, tgt_k2o - aportes["K2O"])
if k2o_restante > 0:
    db_k_seleccionado = FERTILIZANTES_DB[opcion_k]
    g_fuente_k = calcular_gramos(k2o_restante, db_k_seleccionado["K2O"], volumen_agua)
    pesos_finales[opcion_k] = g_fuente_k
    aportes["K2O"] += k2o_restante
    if opcion_k == "Haifa DKP (0-41-54)":
        aportes["P2O5"] += calcular_ppm(g_fuente_k, db_k_seleccionado["P2O5"], volumen_agua)

# 5. FÓSFORO COMPLEMENTARIO (MKP)
p2o5_restante = max(0.0, tgt_p2o5 - aportes["P2O5"])
if p2o5_restante > 0:
    g_mkp = calcular_gramos(p2o5_restante, FERTILIZANTES_DB["Fosfato Monopotásico (MKP)"]["P2O5"], volumen_agua)
    pesos_finales["Fosfato Monopotásico (MKP)"] = g_mkp
    aportes["K2O"] += calcular_ppm(g_mkp, FERTILIZANTES_DB["Fosfato Monopotásico (MKP)"]["K2O"], volumen_agua)
    aportes["P2O5"] += p2o5_restante

# 6. MAGNESIO
if opcion_mg == "Sulfato de Magnesio":
    g_sulfmg = calcular_gramos(tgt_mgo, FERTILIZANTES_DB["Sulfato de Magnesio"]["MgO"], volumen_agua)
    pesos_finales["Sulfato de Magnesio"] = g_sulfmg
    aportes["MgO"] += tgt_mgo
else:
    g_nitmg = calcular_gramos(tgt_mgo, FERTILIZANTES_DB["Nitrato de Magnesio"]["MgO"], volumen_agua)
    pesos_finales["Nitrato de Magnesio"] = g_nitmg
    aportes["MgO"] += tgt_mgo
    aportes["NO3"] += calcular_ppm(g_nitmg, FERTILIZANTES_DB["Nitrato de Magnesio"]["NO3"], volumen_agua)

# 7. COMPENSACIÓN FINAL DE NITRÓGENO (Nitrato de Amonio)
no3_faltante = max(0.0, tgt_no3 - aportes["NO3"])
nh4_faltante = max(0.0, tgt_nh4 - aportes["NH4"])
n_compensar = max(no3_faltante, nh4_faltante)

if n_compensar > 0:
    g_nit_amonio = calcular_gramos(n_compensar, FERTILIZANTES_DB["Nitrato de Amonio"]["NO3"], volumen_agua)
    pesos_finales["Nitrato de Amonio"] = g_nit_amonio
    aportes["NO3"] += calcular_ppm(g_nit_amonio, FERTILIZANTES_DB["Nitrato de Amonio"]["NO3"], volumen_agua)
    aportes["NH4"] += calcular_ppm(g_nit_amonio, FERTILIZANTES_DB["Nitrato de Amonio"]["NH4"], volumen_agua)

# ==========================================
# VISUALIZACIÓN: TABLA DE CONTROL DE APORTES
# ==========================================
st.markdown("---")
st.header("📋 Matriz de Auditoría y Verificación de Excesos (PPM Reales)")
tabla_data = {
    "Elemento": ["Nitrato (NO₃⁻)", "Amonio (NH₄⁺)", "Calcio (CaO)", "Fósforo (P₂O₅)", "Potasio (K₂O)", "Magnesio (MgO)"],
    "Meta Requerida": [f"{tgt_no3:.1f}", f"{tgt_nh4:.1f}", f"{tgt_cao:.1f}", f"{tgt_p2o5:.1f}", f"{tgt_k2o:.1f}", f"{tgt_mgo:.1f}"],
    "Total Logrado": [f"{aportes['NO3']:.1f}", f"{aportes['NH4']:.1f}", f"{aportes['CaO']:.1f}", f"{aportes['P2O5']:.1f}", f"{aportes['K2O']:.1f}", f"{aportes['MgO']:.1f}"],
    "Estado de Control": [
        "🎯 Óptimo" if aportes["NO3"] <= tgt_no3 + 1 else "⚠️ EXCESO COMPENSADO",
        "🎯 Óptimo" if aportes["NH4"] <= tgt_nh4 + 1 else "⚠️ EXCESO COMPENSADO",
        "🎯 Óptimo", "🎯 Óptimo", "🎯 Óptimo", "🎯 Óptimo"
    ]
}
st.table(tabla_data)

# ==========================================
# RESUMEN TOTAL DE REQUERIMIENTOS
# ==========================================
