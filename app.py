import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia Pro", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado")
st.write("Ajusta tus metas de PPM, los Kilogramos/Gramos a la izquierda, o añade fertilizantes nuevos a tu bodega en tiempo real.")

# Porcentajes de Menores Sólidos Daymsa
PCT_FE = 6.0
PCT_B = 20.5
PCT_CU = 13.5
PCT_ZN = 13.0
PCT_MN = 12.0
PCT_MO = 10.0
S_SULMAG = 13.0

# ==========================================
# REGLA DE MEMORIA SEGURA: INVENTARIO EDITABLE DE NUEVAS FUENTES
# ==========================================
if "nuevos_fertilizantes" not in st.session_state:
    st.session_state.nuevos_fertilizantes = {}

# ==========================================
# FORMULARIO CENTRAL: REGISTRO MANUAL DE NUEVAS MARCAS
# ==========================================
st.header("📦 Creación y Registro de Nuevos Fertilizantes")
with st.expander("➕ Haz clic aquí para registrar una marca o mezcla nueva en tu inventario"):
    nombre_nuevo = st.text_input("Nombre Comercial del Fertilizante:", placeholder="Ej: Kelatex, Mix Menores, Fertisolo, etc.")
    
    st.markdown("#### 🥦 Macronutrientes (%)")
    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    with col_n1:
        n_no3 = st.number_input("% Nitrato (NO₃⁻) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_nh4 = st.number_input("% Amonio (NH₄⁺) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n2:
        n_p2o5 = st.number_input("% Fósforo (P₂O₅) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_k2o = st.number_input("% Potasio (K₂O) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n3:
        n_cao = st.number_input("% Calcio (CaO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        n_mgo = st.number_input("% Magnesio (MgO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col_n4:
        n_so3 = st.number_input("% Azufre (SO₃) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
    st.markdown("#### 🧪 Micronutrientes (%)")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        n_fe = st.number_input("% Hierro (Fe) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_mn = st.number_input("% Manganeso (Mn) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    with col_m2:
        n_zn = st.number_input("% Zinc (Zn) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_cu = st.number_input("% Cobre (Cu) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
    with col_m3:
        n_b = st.number_input("% Boro (B) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.01)
        n_mo = st.number_input("% Molibdeno (Mo) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0, step=0.001, format="%.4f")
        
    if st.button("💾 Guardar e Incorporar a la Barra Lateral"):
        if nombre_nuevo:
            st.session_state.nuevos_fertilizantes[nombre_nuevo] = {
                "CaO": n_cao, "NO3": n_no3, "NH4": n_nh4, "P2O5": n_p2o5, "K2O": n_k2o, "MgO": n_mgo, "SO3": n_so3,
                "Fe": n_fe, "Mn": n_mn, "Zn": n_zn, "Cu": n_cu, "B": n_b, "Mo": n_mo
            }
            st.success(f"✅ ¡{nombre_nuevo} guardado! Ya puedes asignarle kilos a la izquierda.")
        else:
            st.error("⚠️ Por favor escribe un nombre comercial válido.")

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

# Renderizado dinámico para productos nuevos
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
# PANEL CENTRAL PASO 2: METAS MODIFICABLES
# ==========================================
st.markdown("---")
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

# Cálculos de Fuentes Estándar
ppm_cao_calcinit = calcular_ppm_campo(kg_calcinit, 26.0)
ppm_p2o5_pony = calcular_ppm_campo(kg_pony, 3.0)
ppm_k2o_pony = calcular_ppm_campo(kg_pony, 43.0)
ppm_p2o5_dkp = calcular_ppm_campo(kg_dkp, 41.0)
ppm_k2o_dkp = calcular_ppm_campo(kg_dkp, 54.0)
ppm_k2o_soluk = calcular_ppm_campo(kg_soluk, 50.0)
ppm_so3_soluk = calcular_ppm_campo(kg_soluk, 18.0)
ppm_p2o5_mkp = calcular_ppm_campo(kg_mkp, 52.0)
ppm_k2o_mkp = calcular_ppm_campo(kg_mkp, 34.0)
ppm_mgo_magboro = calcular_ppm_campo(kg_magboro, 15.5)
ppm_mgo_sulfmg = calcular_ppm_campo(kg_sulfmg, 16.4)
ppm_so3_sulfmg = calcular_ppm_campo(kg_sulfmg, S_SULMAG)

# Nitrógeno Nítrico y Amoniacal Base
ppm_no3_calcinit = (kg_calcinit * 1000.0 * 14.4) / (2600.0 / (197.3 / 72.2))
ppm_no3_pony = (kg_pony * 1000.0 * 13.0) / (2600.0 / (197.3 / 72.2))
ppm_no3_magboro = (kg_magboro * 1000.0 * 10.8) / (2600.0 / (197.3 / 72.2))
ppm_no3_nitamonio = calcular_ppm_campo(kg_nitamonio, 17.0)

ppm_nh4_calcinit = calcular_ppm_campo(kg_calcinit, 1.1)
ppm_nh4_nitamonio = calcular_ppm_campo(kg_nitamonio, 17.0)

# Acumuladores para marcas nuevas
extra_no3_crudo, extra_nh4, extra_cao, extra_p2o5, extra_k2o, extra_mgo, extra_so3 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
extra_fe, extra_mn, extra_zn, extra_cu, extra_b, extra_mo = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

for prod_n, kg_n in pesos_nuevos.items():
    if kg_n > 0:
        db_n = st.session_state.nuevos_fertilizantes[prod_n]
        extra_cao += calcular_ppm_campo(kg_n, db_n.get("CaO", 0.0))
        extra_p2o5 += calcular_ppm_campo(kg_n, db_n.get("P2O5", 0.0))
        extra_k2o += calcular_ppm_campo(kg_n, db_n.get("K2O", 0.0))
        extra_mgo += calcular_ppm_campo(kg_n, db_n.get("MgO", 0.0))
        extra_so3 += calcular_ppm_campo(kg_n, db_n.get("SO3", 0.0))
        extra_nh4 += calcular_ppm_campo(kg_n, db_n.get("NH4", 0.0))
        extra_no3_crudo += calcular_ppm_campo(kg_n, db_n.get("NO3", 0.0))
        
        extra_fe += calcular_ppm_campo(kg_n, db_n.get("Fe", 0.0))
        extra_mn += calcular_ppm_campo(kg_n, db_n.get("Mn", 0.0))
        extra_zn += calcular_ppm_campo(kg_n, db_n.get("Zn", 0.0))
        extra_cu += calcular_ppm_campo(kg_n, db_n.get("Cu", 0.0))
        extra_b += calcular_ppm_campo(kg_n, db_n.get("B", 0.0))
        extra_mo += calcular_ppm_campo(kg_n, db_n.get("Mo", 0.0))

# CONSOLIDACIÓN FINAL
total_no3 = ppm_no3_calcinit + ppm_no3_pony + ppm_no3_magboro + ppm_no3_nitamonio + (extra_no3_crudo * (197.3 / 72.2))
total_nh4 = ppm_nh4_calcinit + ppm_nh4_nitamonio + extra_nh4
total_cao = ppm_cao_calcinit + extra_cao
