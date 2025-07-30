import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
from PIL import Image

# Cargar imágenes
bandera = Image.open("base.jpg")
escudo = Image.open("base1.jpg")

# Mostrar imágenes y título
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image(bandera, width=100)
with col2:
    st.markdown("<h2 style='text-align: center;'>REGISTRO DE HORAS DE SERVICIO SOCIAL - COLEGIO PIO XI</h2>", unsafe_allow_html=True)
with col3:
    st.image(escudo, width=100)

st.write("---")

# Conexión a la base de datos SQLite
conn = sqlite3.connect("registro.db")
c = conn.cursor()

# Crear tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS actividades (
        fecha TEXT,
        lugar TEXT,
        encargado TEXT,
        proyecto TEXT,
        descripcion TEXT,
        horas INTEGER,
        firma TEXT
    )
''')
conn.commit()

# Formulario de registro
with st.form("formulario"):
    fecha = st.date_input("Fecha", value=date.today())
    lugar = st.text_input("Lugar")
    encargado = st.text_input("Encargado del servicio social")
    proyecto = st.text_input("Nombre del proyecto")
    descripcion = st.text_area("Descripción de la actividad realizada")
    horas = st.number_input("Número de horas", min_value=0, step=1)
    firma = st.text_input("Firma del responsable del proyecto")

    enviado = st.form_submit_button("Registrar actividad")

    if enviado:
        c.execute('''
            INSERT INTO actividades (fecha, lugar, encargado, proyecto, descripcion, horas, firma)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fecha, lugar, encargado, proyecto, descripcion, horas, firma))
        conn.commit()
        st.success("¡Actividad registrada exitosamente!")

# Mostrar datos registrados
st.subheader("Registros guardados")
df = pd.read_sql_query("SELECT * FROM actividades", conn)
st.dataframe(df)

# Descargar como Excel
if not df.empty:
    df_excel = df.copy()
    st.download_button(
        label="📥 Descargar en Excel",
        data=df_excel.to_excel(index=False, engine='openpyxl'),
        file_name="registro_servicio_social.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

conn.close()