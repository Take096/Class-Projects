import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("📊 Dashboard de Vendedores")

# --- FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data
def cargar_datos():
    ruta = "vendedores.xlsx"
    if not os.path.exists(ruta):
        st.error(f"No se encontró el archivo: {ruta}")
        return None
    else:
        df = pd.read_excel(ruta)
        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Crear columna "vendedor" combinando nombre y apellido
        if "nombre" in df.columns and "apellido" in df.columns:
            df["vendedor"] = df["nombre"] + " " + df["apellido"]

        # Renombrar columnas relevantes
        df = df.rename(columns={
            "región": "region",
            "unidades_vendidas": "unidades_vendidas",
            "ventas_totales": "ventas_totales",
            "porcentaje_de_ventas": "porcentaje_ventas"
        })

        return df

# --- CARGAR DATAFRAME ---
df = cargar_datos()

if df is None:
    st.stop()

# --- MOSTRAR TABLA COMPLETA ---
st.subheader("Datos de Vendedores")
st.dataframe(df)

st.write("Columnas disponibles:", df.columns.tolist())

# --- FILTRO POR REGIÓN ---
if "region" not in df.columns:
    st.error("No se encontró la columna 'region' en el archivo.")
    st.stop()

regiones = df["region"].unique()
region_sel = st.selectbox("Selecciona una Región:", options=["todas"] + list(regiones))

if region_sel != "todas":
    df_filtrado = df[df["region"] == region_sel]
else:
    df_filtrado = df

# --- MOSTRAR TABLA FILTRADA ---
st.write(f"Mostrando datos para: **{region_sel}**")
st.dataframe(df_filtrado)

# --- GRÁFICAS ---
st.subheader("📈 Gráficas")

# Validar columnas necesarias
for col in ["vendedor", "unidades_vendidas", "ventas_totales"]:
    if col not in df_filtrado.columns:
        st.error(f"Falta la columna '{col}' en el archivo Excel.")
        st.stop()

# --- Gráfica de Unidades Vendidas ---
st.write("**Unidades Vendidas por Vendedor**")
fig1, ax1 = plt.subplots()
ax1.bar(df_filtrado["vendedor"], df_filtrado["unidades_vendidas"])
plt.xticks(rotation=45)
st.pyplot(fig1)

# --- Gráfica de Ventas Totales ---
st.write("**Ventas Totales por Vendedor**")
fig2, ax2 = plt.subplots()
ax2.bar(df_filtrado["vendedor"], df_filtrado["ventas_totales"])
plt.xticks(rotation=45)
st.pyplot(fig2)

# --- Gráfica de Porcentaje de Ventas ---
st.write("**Porcentaje de Ventas**")
fig3, ax3 = plt.subplots()
ax3.pie(
    df_filtrado["ventas_totales"],
    labels=df_filtrado["vendedor"],
    autopct="%1.1f%%",
    startangle=90,
)
ax3.axis("equal")
st.pyplot(fig3)

# --- DATOS DE UN VENDEDOR ESPECÍFICO ---
st.subheader("🔍 Buscar un Vendedor Específico")
vendedores = df["vendedor"].unique()
vendedor_sel = st.selectbox("Selecciona un Vendedor:", options=vendedores)

vendedor_datos = df[df["vendedor"] == vendedor_sel]
st.write(f"Datos de **{vendedor_sel}**:")
st.dataframe(vendedor_datos)

# --- MÉTRICAS CLAVE ---
st.metric("Unidades Vendidas", int(vendedor_datos["unidades_vendidas"].values[0]))
st.metric(
    "Ventas Totales",
    f"${vendedor_datos['ventas_totales'].values[0]:,.2f}",
)
