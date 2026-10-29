import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Manual", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado")
st.write("Escribe libremente los Kilogramos y Gramos en la barra lateral para cuadrar los requerimientos a tu acomodo.")

# ==========================================
# BASE DE DATOS DE RIQUEZAS DE BODEGA
# ==========================================
RIQUEZAS = {
    "YaraLiva CALCINIT": {"CaO": 26.0, "NO3": 14.4, "NH4": 1.1, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0},
    "Poly-Feed Pony (13-3-43)": {"CaO": 0.0, "NO3": 13.0, "NH4": 0.0, "P2O5": 3.0, "K2O": 43.0, "MgO": 0.0, "SO3": 0.0},
    "Haifa DKP (0-41-54)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 41.0, "K2O": 54.0, "MgO": 0.0, "SO3": 0.0},
    "Sulfato de Potasio (Solupotasse)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 50.0, "MgO": 0.0, "SO3": 18.0},
    "Fosfato Monopotásico (MKP)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 52.0, "K2O": 34.0, "MgO": 0.0, "SO3": 0.0},
    "Van Iperen Magboro": {"CaO": 0.0, "NO3": 10.8, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 15.5, "SO3": 0.0},
    "Sulfato de Magnesio (Sulmag)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 16.4, "S_puro": 13.0, "SO3": 0.0},
    "Nitrato de Amonio": {"CaO": 0.0, "NO3": 17.0, "NH4": 17.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0},
    # Menores Sólidos Daymsa
    "Naturquel Fe": 6.0,
    "Klip Boro": 20.5,
    "Kellus Cu": 13.5,
    "Naturzinc": 13.0,
    "Naturmanganeso": 12.0,
    "Molibk": 10.0
}

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
kg_calcinit = st.sidebar.number_input("YaraLiva CALCINIT (Kg):", min_value=0.0, value=5.00, step=0.1)
kg_pony = st.sidebar.number_input("Poly-Feed Pony 13-3-43 (Kg):", min_value=0.0, value=5.20, step=0.1)
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
# PANEL CENTRAL: METAS FIJAS DE TU TABLA
# ==========================================
st.header("🎯 Tus Metas Teóricas (PPM)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Meta NO₃⁻", "133.6 PPM")
    st.metric("Meta NH₄⁺", "23.6 PPM")
    st.metric("Meta CaO", "158.6 PPM")
with col2:
    st.metric("Meta P₂O₅", "81.4 PPM")
    st.metric("Meta K₂O", "503.6 PPM")
    st.metric("Meta MgO", "63.8 PPM")
with col3:
    st.metric("Meta Hierro (Fe)", "3.43 PPM")
    st.metric("Meta Manganeso (Mn)", "1.61 PPM")
    st.metric("Meta Zinc (Zn)", "0.86 PPM")
with col4:
    st.metric("Meta Boro (B)", "0.64 PPM")
    st.metric("Meta Cobre (Cu)", "0.54 PPM")
    st.metric("Meta Molibdeno (Mo)", "0.0107 PPM")

# ==========================================
# CÁLCULO DE PPM LOGRADAS EN TIEMPO REAL
# ==========================================
logrado = {"NO3": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0, "S_puro": 0.0}

# Conversión de ingresos Kg a gramos para la fórmula
f_gramos = {
    "YaraLiva CALCINIT": kg_calcinit * 1000,
    "Poly-Feed Pony (13-3-43)": kg_pony * 1000,
    "Haifa DKP (0-41-54)": kg_dkp * 1000,
    "Sulfato de Potasio (Solupotasse)": kg_soluk * 1000,
    "Fosfato Monopotásico (MKP)": kg_mkp * 1000,
    "Van Iperen Magboro": kg_magboro * 1000,
    "Sulfato de Magnesio (Sulmag)": kg_sulfmg * 1000,
    "Nitrato de Amonio": kg_nitamonio * 1000,
}

# Acumulación de Macros
for fert, gramos in f_gramos.items():
    for elem, riqueza in RIQUEZAS[fert].items():
        if elem in logrado:
            logrado[elem] += calcular_ppm_manual(gramos, riqueza, volumen_agua)

# Aportes colaterales fijos de Potasio (3%) en los menores Klip Boro y Molibk
logrado["K2O"] += calcular_ppm_manual(g_b, 3.0, volumen_agua)
logrado["K2O"] += calcular_ppm_manual(g_mo, 3.0, volumen_agua)

# Cálculo de Menores en PPM
ppm_fe = calcular_ppm_manual(g_fe, RIQUEZAS["Naturquel Fe"], volumen_agua)
ppm_b = calcular_ppm_manual(g_b, RIQUEZAS["Klip Boro"], volumen_agua)
ppm_cu = calcular_ppm_manual(g_cu, RIQUEZAS["Kellus Cu"], volumen_agua)
ppm_zn = calcular_ppm_manual(g_zn, RIQUEZAS["Naturzinc"], volumen_agua)
ppm_mn = calcular_ppm_manual(g_mn, RIQUEZAS["Naturmanganeso"], volumen_agua)
ppm_mo = calcular_ppm_manual(g_mo, RIQUEZAS["Molibk"], volumen_agua)

# ==========================================
# MATRIZ VISUAL DE CONTROL DINÁMICO
# ==========================================
st.markdown("---")
st.header("📋 Matriz de Auditoría y Verificación de Excesos (PPM Reales)")
st.write("Modifica los valores de la izquierda para ver cómo cambian los balances al instante:")

st.write(f"**Nitrógeno Nitratado (NO₃⁻):** Logrado: `{logrado['NO3']:.1f}` / Meta: `133.6` PPM")
st.write(f"**Nitrógeno Amoniacal (NH₄⁺):** Logrado: `{logrado['NH4']:.1f}` / Meta: `23.6` PPM")
st.write(f"**Calcio (CaO):** Logrado: `{logrado['CaO']:.1f}` / Meta: `241.2` PPM")
st.write(f"**Fósforo (P₂O₅):** Logrado: `{logrado['P2O5']:.1f}` / Meta: `81.4` PPM")
st.write(f"**Potasio (K₂O):** Logrado: `{logrado['K2O']:.1f}` / Meta: `503.6` PPM")
st.write(f"**Magnesio (MgO):** Logrado: `{logrado['MgO']:.1f}` / Meta: `63.8` PPM")
st.write(f"**Azufre Solupotasse (SO₃):** `{logrado['SO3']:.1f}` PPM | **Azufre Sulmag (S puro):** `{logrado['S_puro']:.1f}` PPM")

st.markdown("#### Balance de Elementos Menores Logrado:")
st.write(f"• **Hierro (Fe):** Logrado: `{ppm_fe:.2f}` / Meta: `3.43` PPM")
st.write(f"• **Boro (B):** Logrado: `{ppm_b:.2f}` / Meta: `0.64` PPM")
st.write(f"• **Cobre (Cu):** Logrado: `{ppm_cu:.2f}` / Meta: `0.54` PPM")
st.write(f"• **Zinc (Zn):** Logrado: `{ppm_zn:.2f}` / Meta: `0.86` PPM")
st.write(f"• **Manganeso (Mn):** Logrado: `{ppm_mn:.2f}` / Meta: `1.61` PPM")
st.write(f"• **Molibdeno (Mo):** Logrado: `{ppm_mo:.4f}` / Meta: `0.0107` PPM")
