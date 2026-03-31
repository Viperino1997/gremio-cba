import streamlit as st
import random

# Configuración
st.set_page_config(page_title="Gremio de Córdoba - Hardcore", page_icon="⚔️", layout="wide")

# --- ESTADO DE SESIÓN ---
if 'gremio' not in st.session_state:
    st.session_state.gremio = []
if 'sala_actual' not in st.session_state:
    st.session_state.sala_actual = 1
if 'log' not in st.session_state:
    st.session_state.log = ""

st.title("🛡️ Sistema de Gestión: Gremio de Córdoba")
st.divider()

col1, col2 = st.columns([1, 1.5])

# ==========================================
# PANEL IZQUIERDO: RECLUTAMIENTO Y LISTA
# ==========================================
with col1:
    st.header("📋 Reclutamiento de Elite")
    with st.form("form_pj", clear_on_submit=True):
        nombre = st.text_input("Nombre del Aspirante")
        raza = st.selectbox("Raza", ["Humano", "Elfo", "Enano"])
        clase = st.selectbox("Clase", ["Guerrero", "Mago", "Pícaro", "Clérigo", "Bardo"])
        debilidad = st.text_input("Debilidad Fatal")
        genero = st.radio("Género", ["Hombre", "Mujer"], horizontal=True)
        enviar = st.form_submit_button("EVALUAR DIGINIDAD")

    if enviar and nombre:
        # Stats puros 3d6
        f, a, i = sum([random.randint(1,6) for _ in range(3)]), sum([random.randint(1,6) for _ in range(3)]), sum([random.randint(1,6) for _ in range(3)])
        if raza == "Elfo": a += 2
        elif raza == "Enano": f += 2
        
        total = f + a + i
        # VARA DE 38: Solo los mejores entran
        if total >= 38:
            biblioteca = {
                "Guerrero": {"Hombre": "https://img.itch.zone/aW1nLzExMzkwMDk4LnBuZw==/original/4O1qV%2F.png", "Mujer": "https://img.itch.zone/aW1nLzExMzkwMDk5LnBuZw==/original/8O1qV%2F.png"},
                "Mago": {"Hombre": "https://img.itch.zone/aW1nLzExMzkwMTAwLnBuZw==/original/CO1qV%2F.png", "Mujer": "https://img.itch.zone/aW1nLzExMzkwMTAxLnBuZw==/original/EO1qV%2F.png"}
            }
            url = biblioteca.get(clase, {}).get(genero, "https://via.placeholder.com/150")
            
            nuevo = {
                "nombre": nombre, "clase": clase, "raza": raza, "debilidad": debilidad,
                "img": url, "hp": 100, "stats": {"fuerza": f, "agilidad": a, "inteligencia": i}
            }
            st.session_state.gremio.append(nuevo)
            st.success(f"¡{nombre} ES DIGNO! (Poder: {total})")
        else:
            st.error(f"{nombre} FUE RECHAZADO. Poder de {total} es insignificante.")

    # --- LISTA DE HÉROES (UNO ABAJO DEL OTRO) ---
    st.subheader("👥 Miembros del Gremio")
    if not st.session_state.gremio:
        st.write("El salón está vacío...")
    else:
        for p in st.session_state.gremio:
            with st.container(border=True):
                c_img, c_txt = st.columns([1, 3])
                c_img.image(p['img'], width=70)
                c_txt.markdown(f"**{p['nombre']}** ({p['clase']})\n\nHP: {p['hp']}/100 | Stats: F:{p['stats']['fuerza']} A:{p['stats']['agilidad']} I:{p['stats']['inteligencia']}")
                c_txt.caption(f"Debilidad: {p['debilidad']}")

# ==========================================
# PANEL DERECHO: MAZMORRA (MODO INFIERNO)
# ==========================================
with col2:
    st.header("⚔️ La Mazmorra")
    
    vivos = [p['nombre'] for p in st.session_state.gremio]
    if not vivos:
        st.info("Necesitás héroes dignos para entrar.")
    else:
        lider = st.selectbox("Elegí al valiente que irá al frente:", vivos)
        heroe = next(p for p in st.session_state.gremio if p['nombre'] == lider)

        if st.session_state.sala_actual <= 5:
            st.subheader(f"Sala {st.session_state.sala_actual} de 5")
            
            eventos = [
                {"n": "Tirano de Hierro", "d": "Un coloso que exige fuerza bruta.", "s": "fuerza", "dif": 22},
                {"n": "Lluvia de Flechas", "d": "Trampa de presión en el suelo.", "s": "agilidad", "dif": 20},
                {"n": "Glifo de Aniquilación", "d": "Un sello mágico incomprensible.", "s": "inteligencia", "dif": 25},
                {"n": "Derrumbe de Techo", "d": "¡Piedras gigantes!", "s": "fuerza", "dif": 24},
                {"n": "Sombra del Vacío", "d": "Ataca los miedos mentales.", "s": "inteligencia", "dif": 21}
            ]

            if st.button("¡AVANZAR A LA SIGUIENTE SALA!"):
                ev = random.choice(eventos)
                st.session_state.log = f"**{ev['n']}**: {ev['d']}\n\n"
                
                # Tirada 3d6 + Bono
                d1, d2, d3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
                bono = heroe['stats'].get(ev['s'], 0)
                total_t = d1 + d2 + d3 + bono
                
                st.session_state.log += f"🎲 Tirada: ({d1}+{d2}+{d3}) + Bono {ev['s']} ({bono}) = **{total_t}** (Dif: {ev['dif']})\n\n"

                if total_t >= ev['dif']:
                    st.session_state.log += "✨ **¡ÉXITO SOBRENATURAL!** Avanzás ileso."
                    st.session_state.sala_actual += 1
                else:
                    dmg = random.randint(40, 70) # Daño masivo
                    heroe['hp'] -= dmg
                    if heroe['hp'] <= 0:
                        st.session_state.log += f"💀 **MUERTE:** {heroe['nombre']} cayó ante el desafío. Su debilidad por **'{heroe['debilidad']}'** lo distrajo en el momento final."
                        st.session_state.gremio.remove(heroe)
                    else:
                        st.session_state.log += f"💥 **FALLO CRÍTICO:** Recibió {dmg} de daño."
                st.rerun()

            # Mostrar resultado de la acción
            if st.session_state.log:
                st.info(st.session_state.log)
        else:
            st.balloons()
            st.success("🏆 ¡EL GREMIO DE CÓRDOBA HA SOBREVIVIDO! El tesoro es suyo.")
            if st.button("Reiniciar"):
                st.session_state.sala_actual = 1
                st.session_state.log = ""
                st.rerun()
