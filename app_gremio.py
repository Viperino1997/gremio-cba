import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Gremio de Héroes", page_icon="⚔️", layout="wide")

# --- MEMORIA DE SESIÓN (ESTADO) ---
# Esto guarda los datos aunque la página se refresque
if 'gremio' not in st.session_state:
    st.session_state.gremio = []
if 'sala_actual' not in st.session_state:
    st.session_state.sala_actual = 1
if 'jugando' not in st.session_state:
    st.session_state.jugando = False
if 'historial' not in st.session_state:
    st.session_state.historial = []

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
        debilidad = st.text_input("Debilidad")
        
        enviar = st.form_submit_button("Evaluar Ingreso")

    if enviar and nombre:
        # Lógica de Dados para ingreso (Vara de 28)
        fza = sum([random.randint(1, 6) for _ in range(3)])
        agi = sum([random.randint(1, 6) for _ in range(3)])
        int_st = sum([random.randint(1, 6) for _ in range(3)])
        
        # Bonos raciales
        if raza == "Elfo": agi += 1
        elif raza == "Enano": fza += 1
        else: int_st += 1
        
        total = fza + agi + int_st
        
        if total >= 28:
            nuevo_pj = {
                "nombre": nombre, "clase": clase, "raza": raza,
                "stats": {"fuerza": fza, "agilidad": agi, "inteligencia": int_st},
                "total": total, "debilidad": debilidad
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
    
    if not st.session_state.gremio:
        st.info("Esperando héroes admitidos para comenzar la expedición...")
    else:
        # Lista de 10 Eventos
        eventos = [
            {"n": "Cofre Mimético", "d": "El cofre muerde.", "s": None, "dif": 17},
            {"n": "Trampa de Fuego", "d": "¡Llamas!", "s": "agilidad", "dif": 17},
            {"n": "Puerta de Hierro", "d": "Pesada.", "s": "fuerza", "dif": 16},
            {"n": "Acertijo Mortal", "d": "Enigma antiguo.", "s": "inteligencia", "dif": 16},
            {"n": "Runa Explosiva", "d": "Magia inestable.", "s": None, "dif": 17},
            {"n": "Puente Colgante", "d": "Equilibrio.", "s": "agilidad", "dif": 15},
            {"n": "Derrumbe", "d": "¡Piedras!", "s": "fuerza", "dif": 16},
            {"n": "Espectro", "d": "Duelo mental.", "s": "inteligencia", "dif": 14},
            {"n": "Niebla Venenosa", "d": "No respires.", "s": None, "dif": 15},
            {"n": "Piso Resbaladizo", "d": "Aceite goblin.", "s": "agilidad", "dif": 14}
        ]

        if st.session_state.sala_actual <= 5:
            st.subheader(f"Sala actual: {st.session_state.sala_actual} / 5")
            
            # Elección de camino
            camino = st.radio("El pasillo se divide:", ["Izquierda", "Derecha"], horizontal=True)
            
            # Elección de Héroe
            nombres_vivos = [p['nombre'] for p in st.session_state.gremio]
            heroe_nombre = st.selectbox("¿Quién avanza?", nombres_vivos)
            
            if st.button("¡AVANZAR!"):
                evento = random.choice(eventos)
                heroe = next(p for p in st.session_state.gremio if p['nombre'] == heroe_nombre)
                
                st.warning(f"**EVENTO:** {evento['n']} - {evento['d']}")
                
                # Tirada
                dados = sum([random.randint(1, 6) for _ in range(3)])
                bono = heroe['stats'][evento['s']] if evento['s'] else 0
                final = dados + bono
                
                stat_txt = f" + {evento['s']} ({bono})" if evento['s'] else ""
                st.write(f"🎲 {heroe['nombre']} tiró: {dados}{stat_txt} = **Total: {final}** (Dif: {evento['dif']})")
                
                if final >= evento['dif']:
                    st.success("¡ÉXITO! Han pasado a la siguiente sala.")
                    st.session_state.sala_actual += 1
                else:
                    st.error(f"💀 ¡MUERTE! {heroe['nombre']} ha caído. Su debilidad era: {heroe['debilidad']}")
                    st.session_state.gremio.remove(heroe)
        else:
            st.success("🏆 ¡EL GREMIO HA CONQUISTADO LA MAZMORRA!")
            if st.button("Reiniciar Aventura"):
                st.session_state.sala_actual = 1
                st.rerun()

# Mostrar el historial abajo
with st.expander("Ver miembros actuales del Gremio"):
    st.table(st.session_state.gremio)
