import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia Pro", page_icon="🌱", layout="wide")

st.title("🌱 Software de Fertirriego Profesional")
st.write("Ajusta tus metas de PPM o los Kilogramos/Gramos a la izquierda para balancear tu receta al instante.")

# Porcentajes de Menores Sólidos Daymsa
PCT_FE = 6.0
PCT_B = 20.5
PCT_CU = 13.5
PCT_ZN = 13.0
PCT_MN = 12.0
PCT_MO = 10.0

# ==========================================
# REGLA DE MEMORIA SEGURA: INVENTARIO EDITABLE DE NUEVAS FUENTES
# ==========================================
if "nuevos_fertilizantes" not in st.session_state:
    st.session_state.nuevos_fertilizantes = {}

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y DOSIS MANUALES
# ==========================================
st.sidebar.header("💧 Volumen de Agua")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)
denominador_agua = volumen_agua * 0.1

st.sidebar.header("⚖️ Control de Dosificación Manual (Kg)")
kg_calcinit = st.sidebar.number_input("YaraLiva CALCINIT (Kg):", min_value=0.0, value=5.20, step=0.1)
kg_pony = st.sidebar.number_input("Poly-Feed Pony 13-3-43 (Kg):", min_value=0.0, value=5.30, step=0.1)
kg_dkp = st.sidebar.number_input("Haifa DKP 0-41-54 (Kg):", min_value=0.0, value=4.76, step=0.1)
kg_soluk = st.sidebar.number_input("Sulfato de Potasio (Kg):", min_value=0.0, value=3.90, step=0.1)
kg_mkp = st.sidebar.number_input("Fosfato Monopotásico MKP (Kg):", min_value=0.0, value=0.00, step=0.1)
kg_magboro = st.sidebar.number_input("Van Iperen Magboro (Kg):", min_value=0.0, value=4.19, step=0.1)
kg_sulfmg = st.sidebar.number_input("Sulfato de Magnesio Sulmag (Kg):", min_value=0.0, value=3.17, step=0.1)
kg_nitamonio = st.sidebar.number_input("Nitrato de Amonio (Kg):", min_value=0.0, value=0.00, step=0.1)

# Renderizado dinámico para productos nuevos en la barra lateral
pesos_nuevos = {}
if st.session_state.nuevos_fertilizantes:
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 📦 Nuevos Fertilizantes en Bodega")
    for prod_n in st.session_state.nuevos_fertilizantes.keys():
        pesos_nuevos[prod_n] = st.sidebar.number_input(f"{prod_n} (Kg):", min_value=0.0, value=0.0, step=0.1)

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
# MATEMÁTICA PLANA DIRECTA DE TU CALCULADORA DE CAMPO
# ==========================================
ppm_cao_calcinit = ((kg_calcinit * 1000.0) * 26.0) / denominador_agua
ppm_p2o5_pony = ((kg_pony * 1000.0) * 3.0) / denominador_agua
ppm_k2o_pony = ((kg_pony * 1000.0) * 43.0) / denominador_agua
ppm_p2o5_dkp = ((kg_dkp * 1000.0) * 41.0) / denominador_agua
ppm_k2o_dkp = ((kg_dkp * 1000.0) * 54.0) / denominador_agua
ppm_k2o_soluk = ((kg_soluk * 1000.0) * 50.0) / denominador_agua
ppm_so3_soluk = ((kg_soluk * 1000.0) * 18.0) / denominador_agua
ppm_p2o5_mkp = ((kg_mkp * 1000.0) * 52.0) / denominador_agua
ppm_k2o_mkp = ((kg_mkp * 1000.0) * 34.0) / denominador_agua
ppm_mgo_magboro = ((kg_magboro * 1000.0) * 15.5) / denominador_agua
ppm_mgo_sulfmg = ((kg_sulfmg * 1000.0) * 16.4) / denominador_agua
ppm_so3_sulfmg = ((kg_sulfmg * 1000.0) * 13.0)

# Nitrógeno Nítrico y Amoniacal Base de la Libreta
ppm_no3_calcinit = (kg_calcinit * 1000.0 * 14.4) / (2600.0 / (197.3 / 72.2))
ppm_no3_pony = (kg_pony * 1000.0 * 13.0) / (2600.0 / (197.3 / 72.2))
ppm_no3_magboro = (kg_magboro * 1000.0 * 10.8) / (2600.0 / (197.3 / 72.2))
ppm_no3_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua

ppm_nh4_calcinit = ((kg_calcinit * 1000.0) * 1.1) / denominador_agua
ppm_nh4_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua

# Acumuladores para marcas nuevas creadas por el usuario
extra_no3_crudo, extra_nh4, extra_cao, extra_p2o5, extra_k2o, extra_mgo, extra_so3 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
extra_fe, extra_mn, extra_zn, extra_cu, extra_b, extra_mo = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

for prod_n, kg_n in pesos_nuevos.items():
    if kg_n > 0:
        db_n = st.session_state.nuevos_fertilizantes[prod_n]
        extra_cao += ((kg_n * 1000.0) * db_n.get("CaO", 0.0)) / denominador_agua
        extra_p2o5 += ((kg_n * 1000.0) * db_n.get("P2O5", 0.0)) / denominador_agua
        extra_k2o += ((kg_n * 1000.0) * db_n.get("K2O", 0.0)) / denominador_agua
        extra_mgo += ((kg_n * 1000.0) * db_n.get("MgO", 0.0)) / denominador_agua
        extra_so3 += ((kg_n * 1000.0) * db_n.get("SO3", 0.0)) / denominador_agua
        extra_nh4 += ((kg_n * 1000.0) * db_n.get("NH4", 0.0)) / denominador_agua
        extra_no3_crudo += ((kg_n * 1000.0) * db_n.get("NO3", 0.0)) / denominador_agua
        
        extra_fe += ((kg_n * 1000.0) * db_n.get("Fe", 0.0)) / denominador_agua
        extra_mn += ((kg_n * 1000.0) * db_n.get("Mn", 0.0)) / denominador_agua
        extra_zn += ((kg_n * 1000.0) * db_n.get("Zn", 0.0)) / denominador_agua
        extra_cu += ((kg_n * 1000.0) * db_n.get("Cu", 0.0)) / denominador_agua
        extra_b += ((kg_n * 1000.0) * db_n.get("B", 0.0)) / denominador_agua
        extra_mo += ((kg_n * 1000.0) * db_n.get("Mo", 0.0)) / denominador_agua

# CONSOLIDACIÓN FINAL TOTAL DE PPM LOGRADAS
total_no3 = ppm_no3_calcinit + ppm_no3_pony + ppm_no3_magboro + ppm_no3_nitamonio + (extra_no3_crudo * (197.3 / 72.2))
total_nh4 = ppm_nh4_calcinit + ppm_nh4_nitamonio + extra_nh4
total_cao = ppm_cao_calcinit + extra_cao
total_p2o5 = ppm_p2o5_pony + ppm_p2o5_dkp + ppm_p2o5_mkp + extra_p2o5
total_mgo = ppm_mgo_magboro + ppm_mgo_sulfmg + extra_mgo
total_so3 = ppm_so3_soluk + ppm_so3_sulfmg + extra_so3

ppm_k2o_boro_menor = (g_b * 3.0) / denominador_agua
ppm_k2o_molibk_menor = (g_mo * 3.0) / denominador_agua
total_k2o = ppm_k2o_pony + ppm_k2o_dkp + ppm_k2o_soluk + ppm_k2o_mkp + ppm_k2o_boro_menor + ppm_k2o_molibk_menor + extra_k2o

ppm_fe = ((g_fe * PCT_FE) / denominador_agua) + extra_fe
ppm_b = ((g_b * PCT_B) / denominador_agua) + extra_b
ppm_cu = ((g_cu * PCT_CU) / denominador_agua) + extra_cu
ppm_zn = ((g_zn * PCT_ZN) / denominador_agua) + extra_zn
ppm_mn = ((g_mn * PCT_MN) / denominador_agua) + extra_mn
ppm_mo = ((g_mo * PCT_MO) / denominador_agua) + extra_mo

# ==========================================
# 📊 2. MATRIZ EN BLOQUES DE COMPARACIÓN VISUAL DIRECTA (OBLIGATORIA ARRIBA)
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
