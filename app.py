import streamlit as st

st.set_page_config(page_title="Simulador de Fertirriego Colombia", page_icon="🌱", layout="wide")

st.title("🌱 Simulador Manual de Fertirriego Avanzado con Inventario Editable")
st.write("Escribe tus metas, ajusta los kilos o añade fertilizantes nuevos a tu bodega. El sistema recordará tus cambios en tiempo real.")

# ==========================================
# REGLA DE MEMORIA: INICIALIZAR LA BODEGA DE FERTILIZANTES
# ==========================================
if "bodega" not in st.session_state:
    st.session_state.bodega = {
        "YaraLiva CALCINIT": {"CaO": 26.0, "NO3": 14.4, "NH4": 1.1, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0},
        "Poly-Feed Pony (13-3-43)": {"CaO": 0.0, "NO3": 13.0, "NH4": 0.0, "P2O5": 3.0, "K2O": 43.0, "MgO": 0.0, "SO3": 0.0},
        "Haifa DKP (0-41-54)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 41.0, "K2O": 54.0, "MgO": 0.0, "SO3": 0.0},
        "Sulfato de Potasio (Solupotasse)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 50.0, "MgO": 0.0, "SO3": 18.0},
        "Fosfato Monopotásico (MKP)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 52.0, "K2O": 34.0, "MgO": 0.0, "SO3": 0.0},
        "Van Iperen Magboro": {"CaO": 0.0, "NO3": 10.8, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 15.5, "SO3": 0.0},
        "Sulfato de Magnesio (Sulmag)": {"CaO": 0.0, "NO3": 0.0, "NH4": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 16.4, "SO3": 13.0},
        "Nitrato de Amonio": {"CaO": 0.0, "NO3": 17.0, "NH4": 17.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0}
    }

# Variables fijas de menores Daymsa
PCT_FE, PCT_B, PCT_CU, PCT_ZN, PCT_MN, PCT_MO = 6.0, 20.5, 13.5, 13.0, 12.0, 10.0

# ==========================================
# FORMULARIO CENTRAL: AÑADIR NUEVOS ELEMENTOS A BODEGA
# ==========================================
st.header("📦 Creación y Registro de Nuevos Fertilizantes")
with st.expander("➕ Haz clic aquí para registrar una marca o mezcla nueva en tu inventario"):
    nombre_nuevo = st.text_input("Nombre Comercial del Fertilizante:", placeholder="Ej: Master 15-5-30, Fertisolo, etc.")
    
    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    with col_n1:
        n_no3 = st.number_input("% Nitrato (NO₃⁻) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
        n_nh4 = st.number_input("% Amonio (NH₄⁺) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
    with col_n2:
        n_p2o5 = st.number_input("% Fósforo (P₂O₅) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
        n_k2o = st.number_input("% Potasio (K₂O) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
    with col_n3:
        n_cao = st.number_input("% Calcio (CaO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
        n_mgo = st.number_input("% Magnesio (MgO) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
    with col_n4:
        n_so3 = st.number_input("% Azufre (SO₃) del saco nuevo:", min_value=0.0, max_value=100.0, value=0.0)
        
    if st.button("💾 Guardar e Incorporar a la Barra Lateral"):
        if nombre_nuevo:
            st.session_state.bodega[nombre_nuevo] = {
                "CaO": n_cao, "NO3": n_no3, "NH4": n_nh4, "P2O5": n_p2o5, "K2O": n_k2o, "MgO": n_mgo, "SO3": n_so3
            }
            st.success(f"✅ ¡{nombre_nuevo} se ha guardado con éxito! Ya puedes asignarle kilos a la izquierda.")
        else:
            st.error("⚠️ Por favor escribe un nombre válido antes de guardar.")

# ==========================================
# BARRA LATERAL: CONTROL DE AGUA Y DOSIS GENERALES
# ==========================================
st.sidebar.header("💧 Volumen de Agua")
volumen_agua = st.sidebar.number_input("Volumen de agua total (Litros):", min_value=1, value=26000, step=1000)
denominador_agua = volumen_agua * 0.1

st.sidebar.header("⚖️ Control de Dosificación Manual (Kg)")
pesos_ingresados = {}

# Genera dinámicamente casillas para cada fertilizante registrado en la memoria
for producto in st.session_state.bodega.keys():
    # Mantiene los valores por defecto del ejercicio manual anterior
    valor_inicial = 0.0
    if producto == "YaraLiva CALCINIT": valor_inicial = 5.10
    elif producto == "Poly-Feed Pony (13-3-43)": valor_inicial = 5.30
    elif producto == "Haifa DKP (0-41-54)": valor_inicial = 4.76
    elif producto == "Sulfato de Potasio (Solupotasse)": valor_inicial = 3.90
    elif producto == "Van Iperen Magboro": valor_inicial = 4.19
    elif producto == "Sulfato de Magnesio (Sulmag)": valor_inicial = 3.17
    
    pesos_ingresados[producto] = st.sidebar.number_input(f"{producto} (Kg):", min_value=0.0, value=valor_inicial, step=0.1)

st.sidebar.header("🧪 Ingresa tus Micronutrientes (En Gramos)")
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
st.header("🎯 2. Tus Metas Teóricas Requeridas (PPM)")
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
# ALGORITMO DINÁMICO DE ACUMULACIÓN DE NUTRIENTES
# ==========================================
logrado = {"NO3_crudo": 0.0, "NH4": 0.0, "CaO": 0.0, "P2O5": 0.0, "K2O": 0.0, "MgO": 0.0, "SO3": 0.0}

# Procesamiento plano de la bodega en base a lo digitado en la barra lateral
for producto, kg in pesos_ingresados.items():
    gramos = kg * 1000.0
    if gramos > 0:
        logrado["CaO"] += (gramos * st.session_state.bodega[producto]["CaO"]) / denominador_agua
        logrado["P2O5"] += (gramos * st.session_state.bodega[producto]["P2O5"]) / denominador_agua
        logrado["K2O"] += (gramos * st.session_state.bodega[producto]["K2O"]) / denominador_agua
        logrado["MgO"] += (gramos * st.session_state.bodega[producto]["MgO"]) / denominador_agua
        logrado["SO3"] += (gramos * st.session_state.bodega[producto]["SO3"]) / denominador_agua
        logrado["NH4"] += (gramos * st.session_state.bodega[producto]["NH4"]) / denominador_agua
        
        # Guardamos el nitrato crudo para aplicar la calibración lineal de tu libreta abajo
        logrado["NO3_crudo"] += (gramos * st.session_state.bodega[producto]["NO3"]) / denominador_agua

# 🚨 CALIBRACIÓN MATEMÁTICA DE TU LIBRETA PARA EL NITRATO DE AMARRE (Factor de conversión exacto)
total_no3 = logrado["NO3_crudo"] * (197.3 / 72.2)

# Aportes colaterales fijos de Potasio (3%) en los gramos de Klip Boro y Molibk
total_k2o = logrado["K2O"] + ((g_b * 3.0) / denominador_agua) + ((g_mo * 3.0) / denominador_agua)

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
st.header("📋 3. Matriz de Auditoría y Verificación de Excesos (PPM Reales)")

st.write(f"**Nitrógeno Nitratado (NO₃⁻):** Logrado: `{total_no3:.1f}` / Meta: `{tgt_no3:.1f}` PPM")
st.write(f"**Nitrógeno Amoniacal (NH₄⁺):** Logrado: `{logrado['NH4']:.1f}` / Meta: `{tgt_nh4:.1f}` PPM")
st.write(f"**Calcio (CaO):** Logrado: `{logrado['CaO']:.1f}` / Meta: `{tgt_cao:.1f}` PPM")
st.write(f"**Fósforo (P₂O₅):** Logrado: `{logrado['P2O5']:.1f}` / Meta: `{tgt_p2o5:.1f}` PPM")
st.write(f"**Potasio (K₂O):** Logrado: `{total_k2o:.1f}` / Meta: `{tgt_k2o:.1f}` PPM")
st.write(f"**Magnesio (MgO):** Logrado: `{logrado['MgO']:.1f}` / Meta: `{tgt_mgo:.1f}` PPM")
st.write(f"**Azufre Total Logrado (SO₃):** Logrado: `{logrado['SO3']:.1f}` / Meta: `{tgt_so3:.1f}` PPM")

st.markdown("#### Balance de Elementos Menores Logrado:")
st.write(f"• **Hierro (Fe):** Logrado: `{ppm_fe:.2f}` / Meta: `{tgt_fe:.2f}` PPM")
st.write(f"• **Boro (B):** Logrado: `{ppm_b:.2f}` / Meta: `{tgt_b:.2f}` PPM")
st.write(f"• **Cobre (Cu):** Logrado: `{ppm_cu:.2f}` / Meta: `{tgt_cu:.2f}` PPM")
st.write(f"• **Zinc (Zn):** Logrado: `{ppm_zn:.2f}` / Meta: `{tgt_zn:.2f}` PPM")
st.write(f"• **Manganeso (Mn):** Logrado: `{ppm_mn:.2f}` / Meta: `{tgt_mn:.2f}` PPM")
st.write(f"• **Molibdeno (Mo):** Logrado: `{ppm_mo:.4f}` / Meta: `{tgt_mo:.4f}` PPM")
