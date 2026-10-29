import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia Pro", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado")
st.write("Ajusta tus metas de PPM o los Kilogramos/Gramos a la izquierda para balancear tu receta al instante.")

# Porcentajes de Menores Sólidos Daymsa
PCT_FE = 6.0
PCT_B = 20.5
PCT_CU = 13.5
PCT_ZN = 13.0
PCT_MN = 12.0
PCT_MO = 10.0
S_SULMAG = 13.0

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y DOSIS MANUALES
# ==========================================
st.sidebar.header("💧 Volumen de Agua")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)
denominador_agua = volumen_agua * 0.1

st.sidebar.header("⚖️ Control de Dosificación Manual (Kg)")
kg_calcinit = st.sidebar.number_input("YaraLiva CALCINIT (Kg):", min_value=0.0, value=5.10, step=0.1)
kg_pony = st.sidebar.number_input("Poly-Feed Pony 13-3-43 (Kg):", min_value=0.0, value=5.30, step=0.1)
kg_dkp = st.sidebar.number_input("Haifa DKP 0-41-54 (Kg):", min_value=0.0, value=4.76, step=0.1)
kg_soluk = st.sidebar.number_input("Sulfato de Potasio (Kg):", min_value=0.0, value=3.90, step=0.1)
kg_mkp = st.sidebar.number_input("Fosfato Monopotásico MKP (Kg):", min_value=0.0, value=0.00, step=0.1)
kg_magboro = st.sidebar.number_input("Van Iperen Magboro (Kg):", min_value=0.0, value=4.19, step=0.1)
kg_sulfmg = st.sidebar.number_input("Sulfato de Magnesio Sulmag (Kg):", min_value=0.0, value=3.17, step=0.1)
kg_nitamonio = st.sidebar.number_input("Nitrato de Amonio (Kg):", min_value=0.0, value=0.00, step=0.1)

st.sidebar.header("🧪 Ingresa tus Micronutrientes Puros (En Gramos)")
g_fe = st.sidebar.number_input("Naturquel Fe (g):", min_value=0.0, value=1486.3, step=10.0)
g_b = st.sidebar.number_input("Klip Boro (g):", min_value=0.0, value=81.2, step=5.0)
g_cu = st.sidebar.number_input("Kellus Cu (g):", min_value=0.0, value=104.0, step=5.0)
g_zn = st.sidebar.number_input("Naturzinc (g):", min_value=0.0, value=172.0, step=5.0)
g_mn = st.sidebar.number_input("Naturmanganeso (g):", min_value=0.0, value=348.8, step=10.0)
g_mo = st.sidebar.number_input("Molibk (g):", min_value=0.0, value=2.8, step=0.5)

# ==========================================
# PANEL CENTRAL PASO 1: METAS MODIFICABLES
# ==========================================
st.header("🎯 1. Tus Metas Teóricas Requeridas (PPM)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    tgt_no3 = st.number_input("Meta Nitrato (NO₃⁻):", value=133.6, step=1.0)
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
    tgt_so3 = st.number_input("Meta Azufre (SO₃):", value=45.0, step=1.0)

# ==========================================
# MATEMÁTICA EN LÍNEA PLANA DE TU CALCULADORA MANUAL
# ==========================================
def calcular_ppm_campo(kg_fert, pct_elemento):
    if volumen_agua <= 0 or kg_fert <= 0 or pct_elemento <= 0:
        return 0.0
    return ((kg_fert * 1000.0) * pct_elemento) / denominador_agua

# Calcio, Fósforo, Potasio y Magnesio se mantienen con la fórmula estándar
ppm_cao_calcinit = calcular_ppm_campo(kg_calcinit, 26.0)
ppm_p2o5_pony = calcular_ppm_campo(kg_pony, 3.0)
ppm_k2o_pony = calcular_ppm_campo(kg_pony, 43.0)
ppm_p2o5_dkp = calcular_ppm_campo(kg_dkp, 41.0)
ppm_k2o_dkp = calcular_ppm_campo(kg_dkp, 54.0)
ppm_k2o_soluk = calcular_ppm_campo(kg_soluk, 50.0)
ppm_p2o5_mkp = calcular_ppm_campo(kg_mkp, 52.0)
ppm_k2o_mkp = calcular_ppm_campo(kg_mkp, 34.0)
ppm_mgo_magboro = calcular_ppm_campo(kg_magboro, 15.5)
ppm_mgo_sulfmg = calcular_ppm_campo(kg_sulfmg, 16.4)

# Cálculo unificado de Azufre (SO₃)
ppm_so3_soluk = calcular_ppm_campo(kg_soluk, 18.0)
ppm_so3_sulfmg = calcular_ppm_campo(kg_sulfmg, S_SULMAG)
total_so3 = ppm_so3_soluk + ppm_so3_sulfmg

# Nitrógeno Nítrico calibrado con tus factores de libreta
ppm_no3_calcinit = (kg_calcinit * 1000.0 * 14.4) / (2600.0 / (197.3 / 72.2))
ppm_no3_pony = (kg_pony * 1000.0 * 13.0) / (2600.0 / (197.3 / 72.2))
ppm_no3_magboro = (kg_magboro * 1000.0 * 10.8) / (2600.0 / (197.3 / 72.2))
ppm_no3_nitamonio = calcular_ppm_campo(kg_nitamonio, 17.0)

ppm_nh4_calcinit = calcular_ppm_campo(kg_calcinit, 1.1)
ppm_nh4_nitamonio = calcular_ppm_campo(kg_nitamonio, 17.0)

# Aportes colaterales de Potasio (3%) en los gramos de Klip Boro y Molibk
ppm_k2o_boro_menor = (g_b * 3.0) / denominador_agua
ppm_k2o_molibk_menor = (g_mo * 3.0) / denominador_agua

# SUMATORIAS AGREGADAS TOTALES CONSOLIDADAS
total_no3 = ppm_no3_calcinit + ppm_no3_pony + ppm_no3_magboro + ppm_no3_nitamonio
total_nh4 = ppm_nh4_calcinit + ppm_nh4_nitamonio
total_cao = ppm_cao_calcinit
total_p2o5 = ppm_p2o5_pony + ppm_p2o5_dkp + ppm_p2o5_mkp
total_k2o = ppm_k2o_pony + ppm_k2o_dkp + ppm_k2o_soluk + ppm_k2o_mkp + ppm_k2o_boro_menor + ppm_k2o_molibk_menor
total_mgo = ppm_mgo_magboro + ppm_mgo_sulfmg

# Menores Sólidos Daymsa
ppm_fe = (g_fe * PCT_FE) / denominador_agua
ppm_b = (g_b * PCT_B) / denominador_agua
ppm_cu = (g_cu * PCT_CU) / denominador_agua
ppm_zn = (g_zn * PCT_ZN) / denominador_agua
ppm_mn = (g_mn * PCT_MN) / denominador_agua
ppm_mo = (g_mo * PCT_MO) / denominador_agua

# ==========================================
# 📊 MATRIZ EN BLOQUES GIGANTES DE COMPARACIÓN VISUAL DIRECTA
# ==========================================
st.markdown("---")
st.header("📋 2. Matriz de Auditoría Dinámica (Logrado vs Requerimiento)")
st.write("Seguimiento instantáneo de PPM. El valor inferior muestra el balance matemático exacto:")

st.markdown("### 🥦 Balance de Macronutrientes (PPM)")
c_b1, c_b2, c_b3, c_b4, c_b5, c_b6, c_b7 = st.columns(7)
with c_b1: st.metric(label="N-Nitrato (NO₃⁻)", value=f"{total_no3:.1f}", delta=f"{total_no3 - tgt_no3:.1f} vs {tgt_no3:.1f}")
with c_b2: st.metric(label="N-Amonio (NH₄⁺)", value=f"{total_nh4:.1f}", delta=f"{total_nh4 - tgt_nh4:.1f} vs {tgt_nh4:.1f}")
with c_b3: st.metric(label="Calcio (CaO)", value=f"{total_cao:.1f}", delta=f"{total_cao - tgt_cao:.1f} vs {tgt_cao:.1f}")
with c_b4: st.metric(label="Fósforo (P₂O₅)", value=f"{total_p2o5:.1f}", delta=f"{total_p2o5 - tgt_p2o5:.1f} vs {tgt_p2o5:.1f}")
with c_b5: st.metric(label="Potasio (K₂O)", value=f"{total_k2o:.1f}", delta=f"{total_k2o - tgt_k2o:.1f} vs {tgt_k2o:.1f}")
with c_b6: st.metric(label="Magnesio (MgO)", value=f"{total_mgo:.1f}", delta=f"{total_mgo - tgt_mgo:.1f} vs {tgt_mgo:.1f}")
with c_b7: st.metric(label="Azufre (SO₃)", value=f"{total_so3:.1f}", delta=f"{total_so3 - tgt_so3:.1f} vs {tgt_so3:.1f}")

st.markdown("### 🧪 Balance de Elementos Menores (PPM)")
c_m1, c_m2, c_m3, c_m4, c_m5, c_m6 = st.columns(6)
with c_m1: st.metric(label="Hierro (Fe)", value=f"{ppm_fe:.2f}", delta=f"{ppm_fe - tgt_fe:.2f} vs {tgt_fe:.2f}")
with c_m2: st.metric(label="Manganeso (Mn)", value=f"{ppm_mn:.2f}", delta=f"{ppm_mn - tgt_mn:.2f} vs {tgt_mn:.2f}")
with c_m3: st.metric(label="Zinc (Zn)", value=f"{ppm_zn:.2f}", delta=f"{ppm_zn - tgt_zn:.2f} vs {tgt_zn:.2f}")
with c_m4: st.metric(label="Cobre (Cu)", value=f"{ppm_cu:.2f}", delta=f"{ppm_cu - tgt_cu:.2f} vs {tgt_cu:.2f}")
with c_m5: st.metric(label="Boro (B)", value=f"{ppm_b:.2f}", delta=f"{ppm_b - tgt_b:.2f} vs {tgt_b:.2f}")
with c_m6: st.metric(label="Molibdeno (Mo)", value=f"{ppm_mo:.4f}", delta=f"{ppm_mo - tgt_mo:.4f} vs {tgt_mo:.4f}")
