# -*- coding: utf-8 -*-
"""
Fertirriego Inteligente Pro
Calculadora profesional de soluciones nutritivas (líneas comerciales Colombia).
Motor de balance por mínimos cuadrados no negativos (NNLS) con fallback secuencial.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field

import pandas as pd
import streamlit as st

try:
    from scipy.optimize import nnls
    SCIPY_OK = True
except Exception:  # pragma: no cover
    SCIPY_OK = False


# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Fertirriego Inteligente Pro",
    page_icon="🌱",
    layout="wide",
)

ELEMENTOS = ["NO3", "NH4", "CaO", "P2O5", "K2O", "MgO"]

ETIQUETAS = {
    "NO3": "Nitrógeno nítrico (N-NO₃⁻)",
    "NH4": "Nitrógeno amoniacal (N-NH₄⁺)",
    "CaO": "Calcio (CaO)",
    "P2O5": "Fósforo (P₂O₅)",
    "K2O": "Potasio (K₂O)",
    "MgO": "Magnesio (MgO)",
    "S": "Azufre (S)",
}


# ==============================================================================
# BASE DE DATOS DE FERTILIZANTES (riquezas de etiqueta, % p/p)
# ==============================================================================
@dataclass
class Fertilizante:
    nombre: str
    NO3: float = 0.0
    NH4: float = 0.0
    CaO: float = 0.0
    P2O5: float = 0.0
    K2O: float = 0.0
    MgO: float = 0.0
    S: float = 0.0
    tanque: str = "B"           # "A" = calcios/nitratos, "B" = sulfatos/fosfatos, "AB" = indiferente
    familia: str = "Simple"
    incompatible: tuple = field(default_factory=tuple)

    @property
    def N_total(self) -> float:
        return self.NO3 + self.NH4

    def riqueza(self, elem: str) -> float:
        return float(getattr(self, elem, 0.0))


FERTILIZANTES_DB: dict[str, Fertilizante] = {
    # --- Fuentes simples ---
    "YaraLiva CALCINIT": Fertilizante(
        "YaraLiva CALCINIT", NO3=14.4, NH4=1.1, CaO=26.5,
        tanque="A", familia="Calcio", incompatible=("sulfato", "fosfato"),
    ),
    "Nitrato de Potasio": Fertilizante(
        "Nitrato de Potasio", NO3=13.5, K2O=46.0, tanque="A", familia="Potasio",
    ),
    "Sulfato de Potasio (Solupotasse)": Fertilizante(
        "Sulfato de Potasio (Solupotasse)", K2O=51.0, S=18.0,
        tanque="B", familia="Potasio",
    ),
    "Fosfato Monopotásico (MKP)": Fertilizante(
        "Fosfato Monopotásico (MKP)", P2O5=52.0, K2O=34.0,
        tanque="B", familia="Fósforo",
    ),
    "Haifa DKP (0-41-54)": Fertilizante(
        "Haifa DKP (0-41-54)", P2O5=41.0, K2O=54.0, tanque="B", familia="Fósforo",
    ),
    "Sulfato de Magnesio": Fertilizante(
        "Sulfato de Magnesio", MgO=16.0, S=13.0, tanque="B", familia="Magnesio",
    ),
    "Nitrato de Magnesio": Fertilizante(
        "Nitrato de Magnesio", NO3=11.0, MgO=15.0, tanque="A", familia="Magnesio",
    ),
    "Nitrato de Amonio": Fertilizante(
        "Nitrato de Amonio", NO3=17.0, NH4=17.0, tanque="AB", familia="Nitrógeno",
    ),
    "Sulfato de Amonio": Fertilizante(
        "Sulfato de Amonio", NH4=21.0, S=24.0, tanque="B", familia="Nitrógeno",
    ),
    "Ácido Fosfórico 85%": Fertilizante(
        "Ácido Fosfórico 85%", P2O5=61.0, tanque="B", familia="Ácido",
    ),

    # --- Línea Van Iperen Colombia ---
    "Van Iperen INICIO (11-32-11)": Fertilizante(
        "Van Iperen INICIO (11-32-11)", NO3=5.5, NH4=5.5, P2O5=32.0, K2O=11.0,
        tanque="B", familia="NPK complejo",
    ),
    "Van Iperen DESARROLLO (20-20-20)": Fertilizante(
        "Van Iperen DESARROLLO (20-20-20)", NO3=10.0, NH4=10.0, P2O5=20.0, K2O=20.0,
        tanque="B", familia="NPK complejo",
    ),
    "Van Iperen PRODUCCION (12-5-40)": Fertilizante(
        "Van Iperen PRODUCCION (12-5-40)", NO3=7.0, NH4=5.0, P2O5=5.0, K2O=40.0,
        tanque="B", familia="NPK complejo",
    ),

    # --- Línea Haifa Poly-Feed Colombia ---
    "Haifa Poly-Feed INICIO (13-36-13)": Fertilizante(
        "Haifa Poly-Feed INICIO (13-36-13)", NO3=6.5, NH4=6.5, P2O5=36.0, K2O=13.0,
        tanque="B", familia="NPK complejo",
    ),
    "Haifa Poly-Feed DESARROLLO (19-19-19)": Fertilizante(
        "Haifa Poly-Feed DESARROLLO (19-19-19)", NO3=9.5, NH4=9.5, P2O5=19.0, K2O=19.0,
        tanque="B", familia="NPK complejo",
    ),
    "Haifa Poly-Feed PRODUCCION (10-10-43)": Fertilizante(
        "Haifa Poly-Feed PRODUCCION (10-10-43)", NO3=5.0, NH4=5.0, P2O5=10.0, K2O=43.0,
        tanque="B", familia="NPK complejo",
    ),
}

NPK_COMPLEJOS = [k for k, v in FERTILIZANTES_DB.items() if v.familia == "NPK complejo"]


# ==============================================================================
# MICRONUTRIENTES (quelatos / complejos comerciales)
# riqueza = % del elemento objetivo; colateral = aportes secundarios en %
# ==============================================================================
MICROS_DB = {
    "B":  {"producto": "Klip Boro",        "riqueza": 20.5, "colateral": {"K2O": 3.0}},
    "Fe": {"producto": "Naturquel Fe",     "riqueza": 6.0,  "colateral": {}},
    "Cu": {"producto": "Kellus Cu",        "riqueza": 13.5, "colateral": {}},
    "Zn": {"producto": "NaturZinc",        "riqueza": 13.0, "colateral": {}},
    "Mn": {"producto": "NaturManganeso",   "riqueza": 12.0, "colateral": {}},
    "Mo": {"producto": "Molib-K",          "riqueza": 10.0, "colateral": {}},
}


# ==============================================================================
# FUNCIONES DE CONVERSIÓN
# ==============================================================================
def gramos_desde_ppm(ppm: float, riqueza: float, volumen_l: float) -> float:
    """Gramos de producto necesarios para alcanzar `ppm` (mg/L) en `volumen_l`."""
    if riqueza <= 0 or volumen_l <= 0:
        return 0.0
    return (ppm * volumen_l * 0.1) / riqueza


def ppm_desde_gramos(gramos: float, riqueza: float, volumen_l: float) -> float:
    """ppm (mg/L) que aportan `gramos` de producto en `volumen_l`."""
    if volumen_l <= 0:
        return 0.0
    return (gramos * riqueza) / (volumen_l * 0.1)


def oxido_a_elemento(valor: float, oxido: str) -> float:
    """Convierte óxido -> elemento (factores estequiométricos estándar)."""
    factores = {"CaO": 0.7147, "P2O5": 0.4364, "K2O": 0.8301, "MgO": 0.6030}
    return valor * factores.get(oxido, 1.0)


# ==============================================================================
# MOTOR DE BALANCE
# ==============================================================================
def resolver_nnls(
    productos: list[str],
    objetivos: dict[str, float],
    volumen_l: float,
    pesos: dict[str, float],
) -> dict[str, float]:
    """Mínimos cuadrados no negativos: minimiza ||W(Ax - b)|| con x >= 0."""
    import numpy as np

    A = np.array(
        [
            [
                ppm_desde_gramos(1.0, FERTILIZANTES_DB[p].riqueza(e), volumen_l)
                for p in productos
            ]
            for e in ELEMENTOS
        ],
        dtype=float,
    )
    b = np.array([objetivos[e] for e in ELEMENTOS], dtype=float)
    w = np.array([pesos.get(e, 1.0) for e in ELEMENTOS], dtype=float).reshape(-1, 1)

    x, _ = nnls(A * w, (b * w.ravel()))
    return {p: float(g) for p, g in zip(productos, x)}


def resolver_secuencial(
    productos: list[str],
    objetivos: dict[str, float],
    volumen_l: float,
) -> dict[str, float]:
    """Fallback greedy por orden de prioridad agronómica (sin SciPy)."""
    orden = ["MgO", "CaO", "P2O5", "K2O", "NH4", "NO3"]
    pendiente = dict(objetivos)
    sol = {p: 0.0 for p in productos}

    for elem in orden:
        if pendiente.get(elem, 0.0) <= 0.01:
            continue
        candidatos = [p for p in productos if FERTILIZANTES_DB[p].riqueza(elem) > 0]
        if not candidatos:
            continue
        # el más concentrado en el elemento pendiente
        elegido = max(candidatos, key=lambda p: FERTILIZANTES_DB[p].riqueza(elem))
        fert = FERTILIZANTES_DB[elegido]
        g = gramos_desde_ppm(pendiente[elem], fert.riqueza(elem), volumen_l)
        sol[elegido] += g
        for e in ELEMENTOS:
            pendiente[e] = pendiente.get(e, 0.0) - ppm_desde_gramos(
                g, fert.riqueza(e), volumen_l
            )
    return sol


def calcular_aportes(
    solucion: dict[str, float], volumen_l: float
) -> dict[str, float]:
    aportes = {e: 0.0 for e in ELEMENTOS + ["S"]}
    for prod, g in solucion.items():
        fert = FERTILIZANTES_DB[prod]
        for e in aportes:
            aportes[e] += ppm_desde_gramos(g, fert.riqueza(e), volumen_l)
    return aportes


# ==============================================================================
# INTERFAZ: ENCABEZADO
# ==============================================================================
st.title("🌱 Fertirriego Inteligente Pro")
st.caption(
    "Balance de soluciones nutritivas con optimización no negativa, "
    "descuento del análisis de agua y separación de tanques A/B."
)

if not SCIPY_OK:
    st.warning(
        "SciPy no está disponible: se usará el motor secuencial de respaldo. "
        "Añade `scipy` a requirements.txt para activar la optimización completa."
    )


# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("💧 Volumen y agua")
    volumen_agua = st.number_input(
        "Volumen de solución final (L)",
        min_value=1.0, value=16000.0, step=100.0, format="%.0f",
    )

    usar_agua = st.checkbox("Descontar análisis del agua de riego", value=True)
    agua = {e: 0.0 for e in ELEMENTOS}
    if usar_agua:
        st.caption("ppm presentes en la fuente de agua")
        c1, c2 = st.columns(2)
        with c1:
            agua["NO3"] = st.number_input("N-NO₃ agua", min_value=0.0, value=2.0, step=0.5)
            agua["CaO"] = st.number_input("CaO agua", min_value=0.0, value=40.0, step=1.0)
            agua["K2O"] = st.number_input("K₂O agua", min_value=0.0, value=3.0, step=0.5)
        with c2:
            agua["NH4"] = st.number_input("N-NH₄ agua", min_value=0.0, value=0.0, step=0.5)
            agua["MgO"] = st.number_input("MgO agua", min_value=0.0, value=12.0, step=1.0)
            agua["P2O5"] = st.number_input("P₂O₅ agua", min_value=0.0, value=0.0, step=0.5)

    st.header("📦 Fuentes disponibles en bodega")
    opcion_npk = st.selectbox(
        "NPK complejo (opcional)", ["Ninguno (solo fuentes simples)"] + NPK_COMPLEJOS
    )
    simples_default = [
        "YaraLiva CALCINIT",
        "Sulfato de Potasio (Solupotasse)",
        "Fosfato Monopotásico (MKP)",
        "Sulfato de Magnesio",
        "Nitrato de Amonio",
        "Sulfato de Amonio",
    ]
    simples = st.multiselect(
        "Fuentes simples habilitadas",
        [k for k, v in FERTILIZANTES_DB.items() if v.familia != "NPK complejo"],
        default=simples_default,
    )

    st.header("⚙️ Parámetros del balance")
    pct_no3 = st.slider("% del N total como nitrato", 50, 100, 80, step=5)
    st.caption(f"Relación NO₃ : NH₄ = {pct_no3} : {100 - pct_no3}")

    st.subheader("Prioridad por elemento")
    st.caption("Mayor peso = el optimizador se ajusta más estrictamente a esa meta.")
    pesos = {
        "NO3": st.slider("Peso NO₃", 0.1, 5.0, 1.0, 0.1),
        "NH4": st.slider("Peso NH₄", 0.1, 5.0, 2.0, 0.1),
        "CaO": st.slider("Peso CaO", 0.1, 5.0, 2.0, 0.1),
        "P2O5": st.slider("Peso P₂O₅", 0.1, 5.0, 1.5, 0.1),
        "K2O": st.slider("Peso K₂O", 0.1, 5.0, 1.5, 0.1),
        "MgO": st.slider("Peso MgO", 0.1, 5.0, 2.0, 0.1),
    }
    motor = st.radio(
        "Motor de cálculo",
        ["Optimizador NNLS", "Secuencial (greedy)"],
        index=0 if SCIPY_OK else 1,
        disabled=not SCIPY_OK,
    )


# ==============================================================================
# METAS DEL CULTIVO
# ==============================================================================
st.subheader("🧪 Requerimientos objetivo del cultivo (ppm)")

cm1, cm2, cm3 = st.columns(3)
with cm1:
    tgt_n = st.number_input("N total", min_value=0.0, value=157.0, step=1.0)
    tgt_cao = st.number_input("CaO", min_value=0.0, value=241.2, step=1.0)
with cm2:
    tgt_p2o5 = st.number_input("P₂O₅", min_value=0.0, value=97.0, step=1.0)
    tgt_k2o = st.number_input("K₂O", min_value=0.0, value=278.7, step=1.0)
with cm3:
    tgt_mgo = st.number_input("MgO", min_value=0.0, value=64.0, step=1.0)
    tolerancia = st.number_input(
        "Tolerancia aceptable (±%)", min_value=1.0, value=5.0, step=1.0
    )

with st.expander("🔬 Micronutrientes objetivo (ppm)", expanded=False):
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        tgt_fe = st.number_input("Fe", min_value=0.0, value=3.43, step=0.01)
        tgt_b = st.number_input("B", min_value=0.0, value=0.92, step=0.01)
    with mc2:
        tgt_zn = st.number_input("Zn", min_value=0.0, value=0.33, step=0.01)
        tgt_cu = st.number_input("Cu", min_value=0.0, value=0.54, step=0.01)
    with mc3:
        tgt_mn = st.number_input("Mn", min_value=0.0, value=2.47, step=0.01)
        tgt_mo = st.number_input("Mo", min_value=0.0, value=0.19, step=0.01)

metas_micro = {
    "Fe": tgt_fe, "B": tgt_b, "Zn": tgt_zn,
    "Cu": tgt_cu, "Mn": tgt_mn, "Mo": tgt_mo,
}


# ==============================================================================
# CÁLCULO
# ==============================================================================
# 1) Micronutrientes y sus aportes colaterales de macro
micro_pesos: dict[str, float] = {}
colateral_macro = {e: 0.0 for e in ELEMENTOS}

for elem, meta in metas_micro.items():
    info = MICROS_DB[elem]
    g = gramos_desde_ppm(meta, info["riqueza"], volumen_agua)
    micro_pesos[info["producto"]] = g
    for ox, riq in info["colateral"].items():
        colateral_macro[ox] += ppm_desde_gramos(g, riq, volumen_agua)

# 2) Metas netas = meta - agua - colateral de micros
metas_brutas = {
    "NO3": tgt_n * pct_no3 / 100.0,
    "NH4": tgt_n * (100 - pct_no3) / 100.0,
    "CaO": tgt_cao,
    "P2O5": tgt_p2o5,
    "K2O": tgt_k2o,
    "MgO": tgt_mgo,
}
metas_netas = {
    e: max(0.0, metas_brutas[e] - agua.get(e, 0.0) - colateral_macro.get(e, 0.0))
    for e in ELEMENTOS
}

# 3) Cartera de productos habilitados
productos = list(simples)
if opcion_npk != "Ninguno (solo fuentes simples)":
    productos.append(opcion_npk)
productos = list(dict.fromkeys(productos))

if not productos:
    st.error("Selecciona al menos una fuente fertilizante en la barra lateral.")
    st.stop()

# 4) Resolver
if motor == "Optimizador NNLS" and SCIPY_OK:
    solucion = resolver_nnls(productos, metas_netas, volumen_agua, pesos)
else:
    solucion = resolver_secuencial(productos, metas_netas, volumen_agua)

solucion = {p: g for p, g in solucion.items() if g > 0.01}
aportes_fert = calcular_aportes(solucion, volumen_agua)

# 5) ppm finales en el gotero = fertilizantes + agua + colateral de micros
final = {
    e: aportes_fert.get(e, 0.0) + agua.get(e, 0.0) + colateral_macro.get(e, 0.0)
    for e in ELEMENTOS
}
final["S"] = aportes_f
