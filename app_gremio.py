import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Gremio de Héroes", page_icon="⚔️", layout="wide")

# --- MEMORIA DE SESIÓN (ESTADO) ---
if 'gremio' not in st.session_state:
    st.session_state.gremio = []
if 'sala_actual' not in st.session_state:
    st.session_state.sala_actual = 1

# --- ESTILOS ---
st.title("🛡️ Sistema de Gestión: Gremio de Córdoba")
st.divider()

# --- COLUMNAS PRINCIPALES ---
col1, col2 = st.columns([1, 2])

# ==========================================
# PANEL IZQUIERDO: RECLUTAMIENTO
# ==========================================
with col1:
    st.header("📋 Reclutamiento")
    with st.form("form_pj"):
        nombre = st.text_input("Nombre del Aspirante")
        raza = st.selectbox("Raza", ["Humano", "Elfo", "Enano"])
        clase = st.selectbox("Clase", ["Guerrero", "Mago", "Pícaro", "Clérigo", "Bardo"])
        genero = st.radio("Género del héroe", ["Hombre", "Mujer"], horizontal=True)
        enviar = st.form_submit_button("Evaluar Ingreso")

    if enviar and nombre:
        # 1. Lógica de Imágenes
        biblioteca_imagenes = {
            "Guerrero": {
                "Hombre": "https://img.itch.zone/aW1nLzExMzkwMDk4LnBuZw==/original/4O1qV%2F.png",
                "Mujer": "https://img.itch.zone/aW1nLzExMzkwMDk5LnBuZw==/original/8O1qV%2F.png"
            },
            "Mago": {
                "Hombre": "https://img.itch.zone/aW1nLzExMzkwMTAwLnBuZw==/original/CO1qV%2F.png",
                "Mujer": "https://img.itch.zone/aW1nLzExMzkwMTAxLnBuZw==/original/EO1qV%2F.png"
            }
        }
        img_url = biblioteca_imagenes.get(clase, {}).get(genero, "https://via.placeholder.com/150")
        
        # 2. Lógica de Dados
        fza = sum([random.randint(1, 6) for _ in range(3)])
        agi = sum([random.randint(1, 6) for _ in range(3)])
        int_st = sum([random.randint(1, 6) for _ in range(3)])
        
        if raza == "Elfo": agi += 2
        elif raza == "Enano": fza += 2
        
        total = fza + agi + int_st
        
        if total >= 32:
            nuevo_pj = {
                "nombre": nombre,
                "clase": clase,
                "raza": raza,
                "genero": genero,
                "imagen_url": img_url,
                "hp_max": 100,
                "hp_actual": 100,
                "stats": {"fuerza": fza, "agilidad": agi, "inteligencia": int_st},
                "total": total
            }
            st.session_state.gremio.append(nuevo_pj)
            st.success(f"¡{nombre} ADMITIDO! (Poder: {total})")
            st.balloons()
        else:
            st.error(f"{nombre} RECHAZADO (Poder: {total})")

# ==========================================
# PANEL DERECHO: LA MAZMORRA
# ==========================================
with col2:
    st.header("⚔️ La Mazmorra")
    
    nombres_vivos = [p['nombre'] for p in st.session_state.gremio]

    if not nombres_vivos:
        st.info("Esperando héroes admitidos para comenzar la expedición...")
    else:
        # 1. Selección de Héroe y Ficha Visual
        heroe_nombre = st.selectbox("¿Quién va al frente?", nombres_vivos)
        heroe = next(p for p in st.session_state.gremio if p['nombre'] == heroe_nombre)

        with st.container(border=True):
            c_img, c_txt = st.columns([1, 2])
            with c_img:
                st.image(heroe['imagen_url'], width=120)
            with c_txt:
                st.subheader(heroe['nombre'])
                st.caption(f"{heroe['clase']} {heroe['genero']}")
                pct_vida = heroe['hp_actual'] / heroe['hp_max']
                st.write(f"Vida: {heroe['hp_actual']} / {heroe['hp_max']}")
                st.progress(pct_vida)

        # 2. Lógica de Salas
        if st.session_state.sala_actual <= 5:
            st.subheader(f"Sala actual: {st.session_state.sala_actual} / 5")
            
            eventos = [
                {"n": "Trampa de Fuego", "d": "¡Llamas!", "s": "agilidad", "dif": 13},
                {"n": "Puerta de Hierro", "d": "Pesada.", "s": "fuerza", "dif": 15},
                {"n": "Acertijo Mortal", "d": "Enigma.", "s": "inteligencia", "dif": 12},
                {"n": "Derrumbe", "d": "¡Piedras!", "s": "fuerza", "dif": 14}
            ]

            if st.button("¡AVANZAR A LA SIGUIENTE SALA!"):
                evento = random.choice(eventos)
                st.warning(f"SALA {st.session_state.sala_actual}: {evento['n']}")
                
                dado = sum([random.randint(1, 6) for _ in range(3)])
                bono = heroe['stats'].get(evento['s'], 0) if evento['s'] else 0
                total_tiro = dado + bono
                
                if total_tiro >= evento['dif']:
                    st.success(f"¡Éxito! {heroe['nombre']} superó el desafío.")
                    st.session_state.sala_actual += 1
                else:
                    daño = random.randint(25, 45)
                    heroe['hp_actual'] -= daño
                    if heroe['hp_actual'] <= 0:
                        st.error(f"💀 {heroe['nombre']} ha muerto.")
                        st.session_state.gremio.remove(heroe)
                    else:
                        st.error(f"💥 ¡Fallo! Recibió {daño} de daño.")
                st.rerun()

        else:
            st.success("🏆 ¡EL GREMIO HA CONQUISTADO LA MAZMORRA!")
            if st.button("Reiniciar Aventura"):
                st.session_state.sala_actual = 1
                st.rerun()

# Historial al final
st.divider()
with st.expander("Ver miembros actuales del Gremio"):
    if st.session_state.gremio:
        st.table(st.session_state.gremio)
    else:
        st.write("No hay héroes en el gremio todavía.")

