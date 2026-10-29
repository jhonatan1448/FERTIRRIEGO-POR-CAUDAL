import streamlit as st

st.set_page_config(page_title="Fertirriego Maestro - Colombia", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego Avanzado - Clonación Matemática de Campo")
st.write("Auditoría milimétrica basada en la secuencia real de bodega para 26,000 Litros o volumen personalizado.")

# ==========================================
# BASE DE DATOS MAESTRA DE FERTILIZANTES (Riquezas de tus Marbetes)
# ==========================================
FERTILIZANTES_DB = {
    "YaraLiva CALCINIT": {"CaO": 26.0, "NO3": 14.4, "NH4": 1.1},
    "Sulfato de Potasio (Solupotasse)": {"K2O": 50.0, "SO3": 18.0},
    "Fosfato Monopotásico (MKP)": {"P2O5": 52.0, "K2O": 34.0},
    "Haifa DKP (0-41-54)": {"K2O": 54.0, "P2O5": 41.0},
    "Van Iperen Magboro": {"MgO": 15.5, "NO3": 10.8, "B": 0.2},
    "Sulfato de Magnesio (Sulmag)": {"MgO": 16.4, "S_elemental": 13.0},
    "Nitrato de Amonio": {"NO3": 17.0, "NH4": 17.0},
    "Poly-Feed Pony (13-3-43)": {"NO3": 13.0, "P2O5": 3.0, "K2O": 43.0}
}

# Funciones de conversión basadas en tus apuntes de calculadora
def calcular_gramos(ppm, riqueza, volumen):
    if riqueza <= 0:
        return 0.0
    return (ppm * volumen * 0.1) / riqueza

def calcular_ppm(gramos, riqueza, volumen):
    if volumen <= 0:
        return 0.0
    return (gramos * riqueza) / (volumen * 0.1)

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y VOLUMEN
# ==========================================
st.sidebar.header("💧 Parámetros del Sistema")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)

st.sidebar.header("📦 Inventario de Fuentes Disponibles")
opcion_npk = st.sidebar.selectbox("Fórmula NPK Comercial:", ["Poly-Feed Pony (13-3-43)", "Ninguno (Solo simples)"])
opcion_k = st.sidebar.selectbox("Fuente Simple de Potasio:", ["Haifa DKP (0-41-54)", "Sulfato de Potasio (Solupotasse)"])
opcion_mg = st.sidebar.selectbox("Fuente de Magnesio Base:", ["Van Iperen Magboro", "Sulfato de Magnesio (Sulmag)"])

# ==========================================
# PANEL PRINCIPAL: ENTRADA DE REQUERIMIENTOS (METAS)
# ==========================================
st.header("🧪 Requerimientos Objetivo del Cultivo (PPM)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    tgt_no3 = st.number_input("Meta Nitrato (NO₃⁻):", value=133.6)
    tgt_nh4 = st.number_input("Meta Amonio (NH₄⁺):", value=23.6)
    tgt_cao = st.number_input("Meta Calcio (CaO):", value=158.6)
with col2:
    tgt_p2o5 = st.number_input("Meta Fósforo (P₂O₅):", value=81.4)
    tgt_k2o = st.number_input("Meta Potasio (K₂O):", value=503.6)
    tgt_mgo = st.number_input("Meta Magnesio (MgO):", value=63.8)
with col3:
    tgt_fe = st.number_input("Meta Hierro (Fe):", value=3.43)
    tgt_mn = st.number_input("Meta Manganeso (Mn):", value=1.61)
    tgt_zn = st.number_input("Meta Zinc (Zn):", value=0.86)
with col4:
    tgt_b = st.number_input("Meta Boro (B):", value=0.64)
    tgt_cu = st.number_input("Meta Cobre (Cu):", value=0.54)
    tgt_mo = st.number_input("Meta Molibdeno (Mo):", value=0.0107)

# Inicializador de contenedores para resultados y acumulados
aportes = {"NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0, "S_puro": 0.0}
pesos_finales = {}

# ==============================================================================
# ALGORITMO SECUENCIAL EXACTO DE TU CUADERNO DE CAMPO
# ==============================================================================

# Paso 1. MICRONUTRIENTES SÓLIDOS DE DAYMSA (El Molibk inyecta K2O y Boro colateral)
g_molibk = calcular_gramos(tgt_mo, 10.0, volumen_agua)
g_klipboro = calcular_gramos(tgt_b, 20.5, volumen_agua)
g_naturquel_fe = calcular_gramos(tgt_fe, 6.0, volumen_agua)
g_kellus_cu = calcular_gramos(tgt_cu, 13.5, volumen_agua)
g_naturzinc = calcular_gramos(tgt_zn, 13.0, volumen_agua)
g_naturmanganeso = calcular_gramos(tgt_mn, 12.0, volumen_agua)

# Registramos los aportes colaterales del Molibk (3.0% K2O) y Klip Boro (3.0% K2O) al contador
aportes["K2O"] += calcular_ppm(g_molibk, 3.0, volumen_agua)
aportes["K2O"] += calcular_ppm(g_klipboro, 3.0, volumen_agua)

# Paso 2. CÁLCULO DE LAS FUENTES DE MAGNESIO (Magboro y Sulmag)
g_magboro = calcular_gramos(25.0, FERTILIZANTES_DB["Van Iperen Magboro"]["MgO"], volumen_agua)
pesos_finales["Van Iperen Magboro"] = g_magboro
aportes["MgO"] += 25.0
aportes["NO3"] += calcular_ppm(g_magboro, FERTILIZANTES_DB["Van Iperen Magboro"]["NO3"], volumen_agua)

g_sulfmg = calcular_gramos(20.0, FERTILIZANTES_DB["Sulfato de Magnesio (Sulmag)"]["MgO"], volumen_agua)
pesos_finales["Sulfato de Magnesio (Sulmag)"] = g_sulfmg
aportes["MgO"] += 20.0
aportes["S_puro"] += calcular_ppm(g_sulfmg, FERTILIZANTES_DB["Sulfato de Magnesio (Sulmag)"]["S_elemental"], volumen_agua)

# Si falta un remanente para llegar a la meta de la tabla, lo completa el Sulfato de Mg de forma automática
mgo_restante = max(0.0, tgt_mgo - aportes["MgO"])
if mgo_restante > 0:
    g_extra_mg = calcular_gramos(mgo_restante, FERTILIZANTES_DB["Sulfato de Magnesio (Sulmag)"]["MgO"], volumen_agua)
    pesos_finales["Sulfato de Magnesio (Sulmag)"] += g_extra_mg
    aportes["MgO"] += mgo_restante
    aportes["S_puro"] += calcular_ppm(g_extra_mg, FERTILIZANTES_DB["Sulfato de Magnesio (Sulmag)"]["S_elemental"], volumen_agua)

# Paso 3. CALCIO (YaraLiva Calcinit) -> Calculamos tus primeras 50 PPM básicas
g_calcinit = calcular_gramos(50.0, FERTILIZANTES_DB["YaraLiva CALCINIT"]["CaO"], volumen_agua)
pesos_finales["YaraLiva CALCINIT"] = g_calcinit
aportes["CaO"] += 50.0
aportes["NO3"] += calcular_ppm(g_calcinit, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NO3"], volumen_agua)
aportes["NH4"] += calcular_ppm(g_calcinit, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NH4"], volumen_agua)

# Completamos el Calcio restante de la tabla de forma segura
cao_restante = max(0.0, tgt_cao - aportes["CaO"])
if cao_restante > 0:
    g_extra_ca = calcular_gramos(cao_restante, FERTILIZANTES_DB["YaraLiva CALCINIT"]["CaO"], volumen_agua)
    pesos_finales["YaraLiva CALCINIT"] += g_extra_ca
    aportes["CaO"] += cao_restante
    aportes["NO3"] += calcular_ppm(g_extra_ca, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NO3"], volumen_agua)
    aportes["NH4"] += calcular_ppm(g_extra_ca, FERTILIZANTES_DB["YaraLiva CALCINIT"]["NH4"], volumen_agua)

# Paso 4. FÓSFORO Y POTASIO CON BASE EN TUS PASOS MAESTROS (DKP, Pony y Sulfato de K)
g_dkp = calcular_gramos(75.0, FERTILIZANTES_DB["Haifa DKP (0-41-54)"]["P2O5"], volumen_agua)
pesos_finales["Haifa DKP (0-41-54)"] = g_dkp
aportes["P2O5"] += 75.0
aportes["K2O"] += calcular_ppm(g_dkp, FERTILIZANTES_DB["Haifa DKP (0-41-54)"]["K2O"], volumen_agua)

g_pony = calcular_gramos(6.0, FERTILIZANTES_DB["Poly-Feed Pony (13-3-43)"]["P2O5"], volumen_agua)
pesos_finales["Poly-Feed Pony (13-3-43)"] = g_pony
aportes["P2O5"] += 6.0
aportes["K2O"] += calcular_ppm(g_pony, FERTILIZANTES_DB["Poly-Feed Pony (13-3-43)"]["K2O"], volumen_agua)
aportes["NO3"] += calcular_ppm(g_pony, FERTILIZANTES_DB["Poly-Feed Pony (13-3-43)"]["NO3"], volumen_agua)

g_soluk = calcular_gramos(75.0, FERTILIZANTES_DB["Sulfato de Potasio (Solupotasse)"]["K2O"], volumen_agua)
pesos_finales["Sulfato de Potasio (Solupotasse)"] = g_soluk
aportes["K2O"] += 75.0
aportes["SO3"] += calcular_ppm(g_soluk, FERTILIZANTES_DB["Sulfato de Potasio (Solupotasse)"]["SO3"], volumen_agua)

# Si falta Fósforo o Potasio residual para llegar al 100% de la tabla, el MKP y Solupotasse lo cubren automáticamente
p2o5_restante = max(0.0, tgt_p2o5 - aportes["P2O5"])
if p2o5_restante > 0:
    g_mkp = calcular_gramos(p2o5_restante, FERTILIZANTES_DB["Fosfato Monopotásico (MKP)"]["P2O5"], volumen_agua)
    pesos_finales["Fosfato Monopotásico (MKP)"] = g_mkp
    aportes["P2O5"] += p2o5_restante
    aportes["K2O"] += calcular_ppm(g_mkp, FERTILIZANTES_DB["Fosfato Monopotásico (MKP)"]["K2O"], volumen_agua)

k2o_restante = max(0.0, tgt_k2o - aportes["K2O"])
if k2o_restante > 0:
    g_extra_k = calcular_gramos(k2o_restante, FERTILIZANTES_DB["Sulfato de Potasio (Solupotasse)"]["K2O"], volumen_agua)
    if "Sulfato de Potasio (Solupotasse)" in pesos_finales:
        pesos_finales["Sulfato de Potasio (Solupotasse)"] += g_extra_k
    else:
        pesos_finales["Sulfato de Potasio (Solupotasse)"] = g_extra_k
    aportes["K2O"] += k2o_restante
    aportes["SO3"] += calcular_ppm(g_extra_k, FERTILIZANTES_DB["Sulfato de Potasio (Solupotasse)"]["SO3"], volumen_agua)

# Paso 5. COMPENSACIÓN CONTROLADA DE NITRÓGENO RESTANTE (Nitrato de Amonio)
no3_faltante = max(0.0, tgt_no3 - aportes["NO3"])
nh4_faltante = max(0.0, tgt_nh4 - aportes["NH4"])
n_compensar = max(no3_faltante, nh4_faltante)

if n_compensar > 0:
    g_nit_amonio = calcular_gramos(n_compensar, FERTILIZANTES_DB["Nitrato de Amonio"]["NO3"], volumen_agua)
    pesos_finales["Nitrato de Amonio"] = g_nit_amonio
    aportes["NO3"] += calcular_ppm(g_nit_amonio, FERTILIZANTES_DB["Nitrato de Amonio"]["NO3"], volumen_agua)
    aportes["NH4"] += calcular_ppm(g_nit_amonio, FERTILIZANTES_DB["Nitrato de Amonio"]["NH4"], volumen_agua)

# ==========================================
# VISUALIZACIÓN EN PANTALLA: MATRIZ DE AUDITORÍA
# ==========================================
st.markdown("---")
st.header("📋 Matriz de Auditoría y Verificación de Excesos (PPM Reales)")

st.write(f"**Nitrato (NO₃⁻):** Meta: `{tgt_no3:.1f}` | Logrado: `{aportes['NO3']:.1f}` PPM")
st.write(f"**Amonio (NH₄⁺):** Meta: `{tgt_nh4:.1f}` | Logrado: `{aportes['NH4']:.1f}` PPM")
st.write(f"**Calcio (CaO):** Meta: `{tgt_cao:.1f}` | Logrado: `{aportes['CaO']:.1f}` PPM")
st.write(f"**Fósforo (P₂O₅):** Meta: `{tgt_p2o5:.1f}` | Logrado: `{aportes['P2O5']:.1f}` PPM")
st.write(f"**Potasio (K₂O):** Meta: `{tgt_k2o:.1f}` | Logrado: `{aportes['K2O']:.1f}` PPM")
st.write(f"**Magnesio (MgO):** Meta: `{tgt_mgo:.1f}` | Logrado: `{aportes['MgO']:.1f}` PPM")
