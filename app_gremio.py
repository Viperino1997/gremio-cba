import streamlit as st
import random
import time

# Configuración de la página
st.set_page_config(page_title="Gremio de Héroes", page_icon="⚔️", layout="wide")

# --- MEMORIA DE SESIÓN ---
if 'gremio' not in st.session_state:
    st.session_state.gremio = []
if 'sala_actual' not in st.session_state:
    st.session_state.sala_actual = 1
if 'log_aventura' not in st.session_state:
    st.session_state.log_aventura = []

st.title("🛡️ Sistema de Gestión: Gremio de Córdoba")
st.divider()

col1, col2 = st.columns([1, 2])

# ==========================================
# PANEL IZQUIERDO: RECLUTAMIENTO
# ==========================================
with col1:
    st.header("📋 Reclutamiento")
    with st.form("form_pj", clear_on_submit=True):
        nombre = st.text_input("Nombre del Aspirante")
        raza = st.selectbox("Raza", ["Humano", "Elfo", "Enano"])
        clase = st.selectbox("Clase", ["Guerrero", "Mago", "Pícaro", "Clérigo", "Bardo"])
        debilidad = st.text_input("¿Cuál es su gran debilidad?")
        genero = st.radio("Género", ["Hombre", "Mujer"], horizontal=True)
        enviar = st.form_submit_button("Evaluar Ingreso")

    if enviar and nombre:
        biblioteca_imagenes = {
            "Guerrero": {"Hombre": "https://img.itch.zone/aW1nLzExMzkwMDk4LnBuZw==/original/4O1qV%2F.png", "Mujer": "https://img.itch.zone/aW1nLzExMzkwMDk5LnBuZw==/original/8O1qV%2F.png"},
            "Mago": {"Hombre": "https://img.itch.zone/aW1nLzExMzkwMTAwLnBuZw==/original/CO1qV%2F.png", "Mujer": "https://img.itch.zone/aW1nLzExMzkwMTAxLnBuZw==/original/EO1qV%2F.png"}
        }
        img_url = biblioteca_imagenes.get(clase, {}).get(genero, "https://via.placeholder.com/150")
        
        # Tirada de stats (3d6)
        fza, agi, int_st = sum([random.randint(1,6) for _ in range(3)]), sum([random.randint(1,6) for _ in range(3)]), sum([random.randint(1,6) for _ in range(3)])
        if raza == "Elfo": agi += 2
        elif raza == "Enano": fza += 2
        
        total = fza + agi + int_st
        
        if total >= 32:
            nuevo_pj = {
                "nombre": nombre, "clase": clase, "raza": raza, "genero": genero,
                "debilidad": debilidad, "imagen_url": img_url, "hp_max": 100, "hp_actual": 100,
                "stats": {"fuerza": fza, "agilidad": agi, "inteligencia": int_st}, "total": total
            }
            st.session_state.gremio.append(nuevo_pj)
            st.success(f"¡{nombre} ADMITIDO! Poder: {total}")
        else:
            st.error(f"{nombre} RECHAZADO. Poder insuficiente ({total})")

# ==========================================
# PANEL DERECHO: LA MAZMORRA (DIFICULTAD HARD)
# ==========================================
with col2:
    st.header("⚔️ La Mazmorra")
    
    nombres_vivos = [p['nombre'] for p in st.session_state.gremio]

    if not nombres_vivos:
        st.info("El gremio está vacío. Reclutá héroes para explorar.")
    else:
        # Ficha Visual del Héroe seleccionado
        heroe_nombre = st.selectbox("Elegí quién lidera la marcha:", nombres_vivos)
        heroe = next(p for p in st.session_state.gremio if p['nombre'] == heroe_nombre)

        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            c1.image(heroe['imagen_url'], width=100)
            c2.subheader(f"{heroe['nombre']}")
            c2.progress(heroe['hp_actual'] / heroe['hp_max'])
            c2.caption(f"Salud: {heroe['hp_actual']}/100 | {heroe['clase']} | Debilidad: {heroe['debilidad']}")

        if st.session_state.sala_actual <= 5:
            st.subheader(f"🚩 Sala Actual: {st.session_state.sala_actual} / 5")
            
            # --- EVENTOS RECARGADOS (Dificultad subida) ---
            eventos = [
                {"n": "Cofre Mimético", "d": "¡No era un cofre! Tiene colmillos.", "s": "fuerza", "dif": 18},
                {"n": "Trampa de Fuego", "d": "Llamas brotan del suelo.", "s": "agilidad", "dif": 17},
                {"n": "Puerta de Hierro", "d": "Está trabada por siglos de óxido.", "s": "fuerza", "dif": 20},
                {"n": "Acertijo del Esfinge", "d": "Un enigma que quema el cerebro.", "s": "inteligencia", "dif": 19},
                {"n": "Runa Explosiva", "d": "Magia inestable a punto de estallar.", "s": "inteligencia", "dif": 18},
                {"n": "Puente de Cuerdas", "d": "El abismo te mira desde abajo.", "s": "agilidad", "dif": 19},
                {"n": "Derrumbe Súbito", "d": "¡El techo se viene abajo!", "s": "fuerza", "dif": 21},
                {"n": "Espectro del Gremio", "d": "Un antiguo héroe busca tu alma.", "s": "inteligencia", "dif": 17},
                {"n": "Niebla Ácida", "d": "Corroe el metal y la piel.", "s": "agilidad", "dif": 18},
                {"n": "Aceite Resbaladizo", "d": "Imposible mantener el equilibrio.", "s": "agilidad", "dif": 16}
            ]

            if st.button("🚨 ¡EXPLORAR SIGUIENTE SALA!"):
                evento = random.choice(eventos)
                d1, d2, d3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
                bono = heroe['stats'].get(evento['s'], 0)
                total_tiro = d1 + d2 + d3 + bono
                
                # Narración en el Log
                st.session_state.log_aventura = [] # Limpiamos para el nuevo evento
                st.session_state.log_aventura.append(f"**SALA {st.session_state.sala_actual}**: {evento['n']}")
                st.session_state.log_aventura.append(f"🎲 Dados: ({d1}+{d2}+{d3}) + Bono {evento['s']}: {bono} = **{total_tiro}**")
                st.session_state.log_aventura.append(f"🎯 Dificultad a vencer: **{evento['dif']}**")

                if total_tiro >= evento['dif']:
                    st.session_state.log_aventura.append(f"✅ ¡ÉPICO! {heroe['nombre']} superó el desafío.")
                    st.session_state.sala_actual += 1
                else:
                    daño = random.randint(30, 55)
                    heroe['hp_actual'] -= daño
                    if heroe['hp_actual'] <= 0:
                        heroe['hp_actual'] = 0
                        st.session_state.log_aventura.append(f"💀 **MUERTE:** {heroe['nombre']} no pudo evitarlo... Su debilidad por **{heroe['debilidad']}** fue su fin.")
                        st.session_state.gremio.remove(heroe)
                    else:
                        st.session_state.log_aventura.append(f"💥 **FALLO:** Recibió {daño} de daño. ¡Está herido!")
                st.rerun()

            # Mostrar el Log de la última acción para que no sea "frío"
            for msg in st.session_state.log_aventura:
                st.write(msg)
        else:
            st.balloons()
            st.success("🏆 ¡EL GREMIO DE CÓRDOBA HA SAQUEADO LA MAZMORRA!")
            if st.button("Empezar otra expedición"):
                st.session_state.sala_actual = 1
                st.session_state.log_aventura = []
                st.rerun()

# --- TABLA DE MIEMBROS ---
st.divider()
with st.expander("📜 Registros del Gremio"):
    if st.session_state.gremio:
        st.table(st.session_state.gremio)
