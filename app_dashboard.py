import streamlit as st
from streamlit_folium import st_folium
from data_loader import load_data
from map_utils import load_geojson, render_folium_map

st.set_page_config(page_title="Dashboard CDMX", layout="wide")
st.title("🚨 Dashboard de Incidentes Delictivos – CDMX")

# === 1. Carga de datos y GeoJSON ===
url_geojson = "https://datos.cdmx.gob.mx/dataset/7fcbad2f-2f25-4c65-a6f5-8fef98fdaa6e/resource/ca1766b2-60c4-4e4b-b888-38b7b9e8e67e/download/limite-de-las-alcaldias.json"
delegaciones = load_geojson(url_geojson)
df = load_data("df_streamlit.csv")

# === 2. Controles de interfaz ===
st.sidebar.header("⚙️ Configuración del mapa")
# opciones_equipo = ["TODAS", "GUSTAVO A. MADERO", "TLALPAN"]
# opcion = st.sidebar.selectbox("Selecciona alcaldía (opcional):", opciones_equipo, index=0)
alcaldias_disponibles = sorted(df["alcaldia_hecho"].dropna().unique().tolist()) # Obtiene una lista de las alcaldías
opcion = st.sidebar.selectbox("Selecciona alcaldía (opcional):",["TODAS"] + alcaldias_disponibles, index=0)
tipo_capa = st.sidebar.multiselect("Capas a mostrar:", ["Puntos", "Heatmap"], default=["Heatmap"])
num_points = st.sidebar.slider("Número de puntos (muestreo)", 100, 2000, 500, step=100)
# Muestra la info sobre registros totales
total_registros = len(df)
st.sidebar.info(f" Registros totales: {total_registros:,}")

# === 3. Filtrado ===
# Filtrar por alcaldía si se seleccionó una específica
df_filtrado = df.copy()
if opcion != "TODAS":
    df_filtrado = df_filtrado[df_filtrado["alcaldia_hecho"] == opcion]
if len(df_filtrado) > num_points:
    df_filtrado = df_filtrado.sample(num_points, random_state=42)

# === 4. Render del mapa ===
m = render_folium_map(
    df_filtrado,
    delegaciones,
    show_points="Puntos" in tipo_capa,
    show_heatmap="Heatmap" in tipo_capa
)
st_folium(m, width=800, height=600)
