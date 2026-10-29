import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado")
st.write("Escribe libremente tanto tus metas objetivo de PPM como los Kilogramos y Gramos para cuadrar los requerimientos a tu acomodo.")

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
# PANEL CENTRAL: REQUERIMIENTOS OBJETIVO
# ==========================================
st.header("🎯 Tus Metas Teóricas (PPM)")
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

# ==========================================
# MATEMÁTICA EN LÍNEA BASADA EN TU CALCULADORA DE MANO
# ==========================================
denominador_agua = volumen_agua * 0.1

# Conversión y cálculo individual por producto (Kg * 1000 = Gramos)
ppm_no3_calcinit = ((kg_calcinit * 1000.0) * 14.4) / denominador_agua
ppm_nh4_calcinit = ((kg_calcinit * 1000.0) * 1.1) / denominador_agua
ppm_cao_calcinit = ((kg_calcinit * 1000.0) * 26.0) / denominador_agua

ppm_no3_pony = ((kg_pony * 1000.0) * 13.0) / denominador_agua
ppm_p2o5_pony = ((kg_pony * 1000.0) * 3.0) / denominador_agua
ppm_k2o_pony = ((kg_pony * 1000.0) * 43.0) / denominador_agua

ppm_p2o5_dkp = ((kg_dkp * 1000.0) * 41.0) / denominador_agua
ppm_k2o_dkp = ((kg_dkp * 1000.0) * 54.0) / denominador_agua

ppm_k2o_soluk = ((kg_soluk * 1000.0) * 50.0) / denominador_agua
ppm_so3_soluk = ((kg_soluk * 1000.0) * 18.0) / denominador_agua

ppm_p2o5_mkp = ((kg_mkp * 1000.0) * 52.0) / denominador_agua
ppm_k2o_mkp = ((kg_mkp * 1000.0) * 34.0) / denominador_agua

ppm_mgo_magboro = ((kg_magboro * 1000.0) * 15.5) / denominador_agua
ppm_no3_magboro = ((kg_magboro * 1000.0) * 10.8) / denominador_agua

ppm_mgo_sulfmg = ((kg_sulfmg * 1000.0) * 16.4) / denominador_agua
ppm_s_sulmag = ((kg_sulfmg * 1000.0) * S_SULMAG) / denominador_agua

ppm_no3_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua
ppm_nh4_nitamonio = ((kg_nitamonio * 1000.0) * 17.0) / denominador_agua

# Aportes colaterales fijos de Potasio (3%) en los gramos de Klip Boro y Molibk
ppm_k2o_boro_menor = (g_b * 3.0) / denominador_agua
ppm_k2o_molibk_menor = (g_mo * 3.0) / denominador_agua

# SUMATORIAS AGREGADAS TOTALES
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
# MATRIZ VISUAL DE CONTROL DINÁMICO
# ==========================================
st.markdown("---")
st.header("📋 Matriz de Auditoría y Verificación de Excesos (PPM Reales)")
st.write("Modifica los requerimientos arriba o las dosis a la izquierda para balancear tu receta al instante:")

st.write(f"**Nitrógeno Nitratado (NO₃⁻):** Logrado: `{total_no3:.1f}` / Meta: `{tgt_no3:.1f}` PPM")
st.write(f"**Nitrógeno Amoniacal (NH₄⁺):** Logrado: `{total_nh4:.1f}` / Meta: `{tgt_nh4:.1f}` PPM")
st.write(f"**Calcio (CaO):** Logrado: `{total_cao:.1f}` / Meta: `{tgt_cao:.1f}` PPM")
st.write(f"**Fósforo (P₂O₅):** Logrado: `{total_p2o5:.1f}` / Meta: `{tgt_p2o5:.1f}` PPM")
st.write(f"**Potasio (K₂O):** Logrado: `{total_k2o:.1f}` / Meta: `{tgt_k2o:.1f}` PPM")
st.write(f"**Magnesio (MgO):** Logrado: `{total_mgo:.1f}` / Meta: `{tgt_mgo:.1f}` PPM")
st.write(f"**Azufre Solupotasse (SO₃):** `{ppm_so3_soluk:.1f}` PPM | **Azufre Sulmag (S puro):** `{ppm_s_sulmag:.1f}` PPM")

st.markdown("#### Balance de Elementos Menores Logrado:")
st.write(f"• **Hierro (Fe):** Logrado: `{ppm_fe:.2f}` / Meta: `{tgt_fe:.2f}` PPM")
st.write(f"• **Boro (B):** Logrado: `{ppm_b:.2f}` / Meta: `{tgt_b:.2f}` PPM")
st.write(f"• **Cobre (Cu):** Logrado: `{ppm_cu:.2f}` / Meta: `{tgt_cu:.2f}` PPM")
st.write(f"• **Zinc (Zn):** Logrado: `{ppm_zn:.2f}` / Meta: `{tgt_zn:.2f}` PPM")
st.write(f"• **Manganeso (Mn):** Logrado: `{ppm_mn:.2f}` / Meta: `{tgt_mn:.2f}` PPM")
st.write(f"• **Molibdeno (Mo):** Logrado: `{ppm_mo:.4f}` / Meta: `{tgt_mo:.4f}` PPM")
