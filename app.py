import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Flexible", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado")
st.write("Escribe libremente tanto tus metas objetivo de PPM como los Kilogramos y Gramos para cuadrar los requerimientos a tu acomodo.")

# ==========================================
# BASE DE DATOS DE MACRONUTRIENTES
# ==========================================
RIQUEZAS_MACROS = {
    "YaraLiva CALCINIT": {"CaO": 26.0, "NO3": 14.4, "NH4": 1.1, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0},
    "Poly-Feed Pony (13-3-43)": {"CaO": 0.0, "NO3": 13.0, "NH4": 0.0, "P2O5": 3.0, "K2O": 43.0, "MgO": 0.0, "SO3": 0.0},
    "Haifa DKP (0-41-54)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 41.0, "K2O": 54.0, "MgO": 0.0, "SO3": 0.0},
    "Sulfato de Potasio (Solupotasse)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 50.0, "MgO": 0.0, "SO3": 18.0},
    "Fosfato Monopotásico (MKP)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 52.0, "K2O": 34.0, "MgO": 0.0, "SO3": 0.0},
    "Van Iperen Magboro": {"CaO": 0.0, "NO3": 10.8, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 15.5, "SO3": 0.0},
    "Sulfato de Magnesio (Sulmag)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 16.4, "SO3": 0.0},
    "Nitrato de Amonio": {"CaO": 0.0, "NO3": 17.0, "NH4": 17.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0}
}

# Riquezas fijas de menores sólidos de tus marbetes Daymsa
PCT_FE = 6.0
PCT_B = 20.5
PCT_CU = 13.5
PCT_ZN = 13.0
PCT_MN = 12.0
PCT_MO = 10.0
S_SULMAG = 13.0

def calcular_ppm_manual(gramos, riqueza, volumen):
    if volumen <= 0 or gramos <= 0:
        return 0.0
    return (gramos * riqueza) / (volumen * 0.1)

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y DOSIS MANUALES
# ==========================================
st.sidebar.header("💧 Volumen de Agua")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)

st.sidebar.header("⚖️ Ingresa tus Macronutrientes (En Kilogramos)")
kg_calcinit = st.sidebar.number_input("YaraLiva CALCINIT (Kg):", min_value=0.0, value=5.10, step=0.1)
kg_pony = st.sidebar.number_input("Poly-Feed Pony 13-3-43 (Kg):", min_value=0.0, value=5.30, step=0.1)
kg_dkp = st.sidebar.number_input("Haifa DKP 0-41-54 (Kg):", min_value=0.0, value=4.76, step=0.1)
kg_soluk = st.sidebar.number_input("Sulfato de Potasio (Kg):", min_value=0.0, value=3.90, step=0.1)
kg_mkp = st.sidebar.number_input("Fosfato Monopotásico MKP (Kg):", min_value=0.0, value=0.00, step=0.1)
kg_magboro = st.sidebar.number_input("Van Iperen Magboro (Kg):", min_value=0.0, value=4.19, step=0.1)
kg_sulfmg = st.sidebar.number_input("Sulfato de Magnesio Sulmag (Kg):", min_value=0.0, value=3.17, step=0.1)
kg_nitamonio = st.sidebar.number_input("Nitrato de Amonio (Kg):", min_value=0.0, value=0.00, step=0.1)

st.sidebar.header("🧪 Ingresa tus Micronutrientes (En Gramos)")
g_fe = st.sidebar.number_input("Naturquel Fe (g):", min_value=0.0, value=1486.3, step=10.0)
g_b = st.sidebar.number_input("Klip Boro (g):", min_value=0.0, value=81.2, step=5.0)
g_cu = st.sidebar.number_input("Kellus Cu (g):", min_value=0.0, value=104.0, step=5.0)
g_zn = st.sidebar.number_input("Naturzinc (g):", min_value=0.0, value=172.0, step=5.0)
g_mn = st.sidebar.number_input("Naturmanganeso (g):", min_value=0.0, value=348.8, step=10.0)
g_mo = st.sidebar.number_input("Molibk (g):", min_value=0.0, value=2.8, step=0.5)

# ==========================================
# PANEL CENTRAL: REQUERIMIENTOS MODIFICABLES
# ==========================================
st.header("🎯 Tus Metas Teóricas (Modifica los valores de PPM según tu cultivo)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    tgt_no3 = st.number_input("Meta Nitrato (NO₃⁻):", value=157.0, step=1.0)
    tgt_nh4 = st.number_input("Meta Amonio (NH₄⁺):", value=23.6, step=1.0)
    tgt_cao = st.number_input("Meta Calcio (CaO):", value=158.6, step=1.0)
with col2:
    tgt_p2o5 = st.number_input("Meta Fósforo (P₂O₅):", value=81.4, step=1.0)
    tgt_k2o = st.number_input("Meta Potasio (K₂O):", value=503.6, step=5.0)
    tgt_mgo = st.number_input("Meta Magnesio (MgO):", value=63.8, step=1.0)
with col3:
    tgt_fe = st.number_input("Meta Hierro (Fe):", value=3.43, step=0.1)
    tgt_mn = st.number_input("Meta Manganeso (Mn):", value=1.61, step=0.1)
    tgt_zn = st.number_input("Meta Zinc (Zn):", value=0.86, step=0.1)
with col4:
    tgt_b = st.number_input("Meta Boro (B):", value=0.64, step=0.1)
    tgt_cu = st.number_input("Meta Cobre (Cu):", value=0.54, step=0.1)
    tgt_mo = st.number_input("Meta Molibdeno (Mo):", value=0.0107, format="%.4f")

# ==========================================
# CÁLCULO DE PPM LOGRADAS EN TIEMPO REAL
# ==========================================
logrado = {"NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0}

# Conversión directa e individual elemento por elemento (Suma plana ultra segura)
logrado["CaO"] += calcular_ppm_manual(kg_calcinit * 1000, RIQUEZAS_MACROS["YaraLiva CALCINIT"]["CaO"], volumen_agua)
logrado["NO3"] += calcular_ppm_manual(kg_calcinit * 1000, RIQUEZAS_MACROS["YaraLiva CALCINIT"]["NO3"], volumen_agua)
logrado["NH4"] += calcular_ppm_manual(kg_calcinit * 1000, RIQUEZAS_MACROS["YaraLiva CALCINIT"]["NH4"], volumen_agua)

logrado["NO3"] += calcular_ppm_manual(kg_pony * 1000, RIQUEZAS_MACROS["Poly-Feed Pony (13-3-43)"]["NO3"], volumen_agua)
logrado["P2O5"] += calcular_ppm_manual(kg_pony * 1000, RIQUEZAS_MACROS["Poly-Feed Pony (13-3-43)"]["P2O5"], volumen_agua)
logrado["K2O"] += calcular_ppm_manual(kg_pony * 1000, RIQUEZAS_MACROS["Poly-Feed Pony (13-3-43)"]["K2O"], volumen_agua)

logrado["P2O5"] += calcular_ppm_manual(kg_dkp * 1000, RIQUEZAS_MACROS["Haifa DKP (0-41-54)"]["P2O5"], volumen_agua)
logrado["K2O"] += calcular_ppm_manual(kg_dkp * 1000, RIQUEZAS_MACROS["Haifa DKP (0-41-54)"]["K2O"], volumen_agua)

logrado["K2O"] += calcular_ppm_manual(kg_soluk * 1000, RIQUEZAS_MACROS["Sulfato de Potasio (Solupotasse)"]["K2O"], volumen_agua)
logrado["SO3"] += calcular_ppm_manual(kg_soluk * 1000, RIQUEZAS_MACROS["Sulfato de Potasio (Solupotasse)"]["SO3"], volumen_agua)

logrado["P2O5"] += calcular_ppm_manual(kg_mkp * 1000, RIQUEZAS_MACROS["Fosfato Monopotásico (MKP)"]["P2O5"], volumen_agua)
logrado["K2O"] += calcular_ppm_manual(kg_mkp * 1000, RIQUEZAS_MACROS["Fosfato Monopotásico (MKP)"]["K2O"], volumen_agua)

logrado["MgO"] += calcular_ppm_manual(kg_magboro * 1000, RIQUEZAS_MACROS["Van Iperen Magboro"]["MgO"], volumen_agua)
logrado["NO3"] += calcular_ppm_manual(kg_magboro * 1000, RIQUEZAS_MACROS["Van Iperen Magboro"]["NO3"], volumen_agua)

logrado["MgO"] += calcular_ppm_manual(kg_sulfmg * 1000, RIQUEZAS_MACROS["Sulfato de Magnesio (Sulmag)"]["MgO"], volumen_agua)
ppm_s_sulmag = calcular_ppm_manual(kg_sulfmg * 1000, S_SULMAG, volumen_agua)

logrado["NO3"] += calcular_ppm_manual(kg_nitamonio * 1000, RIQUEZAS_MACROS["Nitrato de Amonio"]["NO3"], volumen_agua)
logrado["NH4"] += calcular_ppm_manual(kg_nitamonio * 1000, RIQUEZAS_MACROS["Nitrato de Amonio"]["NH4"], volumen_agua)

# Aportes colaterales fijos de Potasio (3%) en los menores Klip Boro y Molibk
logrado["K2O"] += calcular_ppm_manual(g_b, 3.0, volumen_agua)
logrado["K2O"] += calcular_ppm_manual(g_mo, 3.0, volumen_agua)

# Cálculo plano de menores en PPM (Evita el KeyError al 100%)
ppm_fe = calcular_ppm_manual(g_fe, PCT_FE, volumen_agua)
ppm_b = calcular_ppm_manual(g_b, PCT_B, volumen_agua)
ppm_cu = calcular_ppm_manual(g_cu, PCT_CU, volumen_agua)
ppm_zn = calcular_ppm_manual(g_zn, PCT_ZN, volumen_agua)
ppm_mn = calcular_ppm_manual(g_mn, PCT_MN, volumen_agua)
ppm_mo = calcular_ppm_manual(g_mo, PCT_MO, volumen_agua)

# ==========================================
# MATRIZ VISUAL DE CONTROL DINÁMICO
# ==========================================
st.markdown("---")
st.header("📋 Matriz de Auditoría y Verificación de Excesos (PPM Reales)")
st.write("Modifica los requerimientos arriba o las dosis a la izquierda para balancear tu receta al instante:")

st.write(f"**Nitrógeno Nitratado (NO₃⁻):** Logrado: `{logrado['NO3']:.1f}` / Meta: `{tgt_no3:.1f}` PPM")
st.write(f"**Nitrógeno Amoniacal (NH₄⁺):** Logrado: `{logrado['NH4']:.1f}` / Meta: `{tgt_nh4:.1f}` PPM")
st.write(f"**Calcio (CaO):** Logrado: `{logrado['CaO']:.1f}` / Meta: `{tgt_cao:.1f}` PPM")
st.write(f"**Fósforo (P₂O₅):** Logrado: `{logrado['P2O5']:.1f}` / Meta: `{tgt_p2o5:.1f}` PPM")
st.write(f"**Potasio (K₂O):** Logrado: `{logrado['K2O']:.1f}` / Meta: `{tgt_k2o:.1f}` PPM")
st.write(f"**Magnesio (MgO):** Logrado: `{logrado['MgO']:.1f}` / Meta: `{tgt_mgo:.1f}` PPM")
st.write(f"**Azufre Solupotasse (SO₃):** `{logrado['SO3']:.1f}` PPM | **Azufre Sulmag (S puro):** `{ppm_s_sulmag:.1f}` PPM")

st.markdown("#### Balance de Elementos Menores Logrado:")
st.write(f"• **Hierro (Fe):** Logrado: `{ppm_fe:.2f}` / Meta: `{tgt_fe:.2f}` PPM")
st.write(f"• **Boro (B):** Logrado: `{ppm_b:.2f}` / Meta: `{tgt_b:.2f}` PPM")
st.write(f"• **Cobre (Cu):** Logrado: `{ppm_cu:.2f}` / Meta: `{tgt_cu:.2f}` PPM")
st.write(f"• **Zinc (Zn):** Logrado: `{ppm_zn:.2f}` / Meta: `{tgt_zn:.2f}` PPM")
st.write(f"• **Manganeso (Mn):** Logrado: `{ppm_mn:.2f}` / Meta: `{tgt_mn:.2f}` PPM")
st.write(f"• **Molibdeno (Mo):** Logrado: `{ppm_mo:.4f}` / Meta: `{tgt_mo:.4f}` PPM")
