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
        genero = st.radio("Género del héroe", ["Hombre", "Mujer"], horizontal=True)

# Al final, cuando el usuario le da al botón 'Enviar':
if enviar and nombre:
    # Diccionario de imágenes (Podés buscar URLs de pixel art que te gusten)
    biblioteca_imagenes = {
        "Guerrero": {
            "Hombre": "https://img.itch.zone/aW1nLzExMzkwMDk4LnBuZw==/original/4O1qV%2F.png",
            "Mujer": "https://img.itch.zone/aW1nLzExMzkwMDk5LnBuZw==/original/8O1qV%2F.png"
        },
        "Mago": {
            "Hombre": "https://img.itch.zone/aW1nLzExMzkwMTAwLnBuZw==/original/CO1qV%2F.png",
            "Mujer": "https://img.itch.zone/aW1nLzExMzkwMTAxLnBuZw==/original/EO1qV%2F.png"
        }
        # Agregá las otras clases siguiendo el mismo formato
    }
    
    # Obtenemos la URL según clase y género
    img_url = biblioteca_imagenes.get(clase, {}).get(genero, "https://via.placeholder.com/150")
    enviar = st.form_submit_button("Evaluar Ingreso")

    if enviar and nombre:
        # Lógica de Dados para ingreso (Vara de 32)
        fza = sum([random.randint(1, 6) for _ in range(3)])
        agi = sum([random.randint(1, 6) for _ in range(3)])
        int_st = sum([random.randint(1, 6) for _ in range(3)])
        
        # Bonos raciales
        if raza == "Elfo": agi += 1
        elif raza == "Enano": fza += 1
        else: int_st += 1
        
        total = fza + agi + int_st
        
        if total >= 32:
        nuevo_pj = {
        "nombre": nombre,
        "clase": clase,
        "genero": genero,
        "imagen_url": img_url,
        "hp_max": 100,
        "hp_actual": 100,  # Empiezan con la vida al máximo
        "stats": {"fuerza": f, "agilidad": a, "inteligencia": i},
        "total": f + a + i,
        "vivo": True
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
    # --- En la columna de la Mazmorra (col2) ---
if nombres_vivos:
    heroe_nombre = st.selectbox("¿Quién va al frente?", nombres_vivos)
    # Buscamos los datos del héroe elegido
    heroe = next(p for p in st.session_state.gremio if p['nombre'] == heroe_nombre)

    # Creamos un contenedor con borde para que parezca una carta
    with st.container(border=True):
        col_img, col_txt = st.columns([1, 2])
        
        with col_img:
            st.image(heroe['imagen_url'], width=120)
        
        with col_txt:
            st.subheader(f"{heroe['nombre']}")
            st.caption(f"{heroe['clase']} {heroe['genero']}")
            
            # Cálculo de porcentaje para la barra de vida
            porcentaje_vida = heroe['hp_actual'] / heroe['hp_max']
            
            # Color de la barra: verde si está bien, rojo si está crítico
            st.write(f"Vida: {heroe['hp_actual']} / {heroe['hp_max']}")
            st.progress(porcentaje_vida)
    if not st.session_state.gremio:
        st.info("Esperando héroes admitidos para comenzar la expedición...")
    else:
        # Lista de 10 Eventos
        eventos = [
            {"n": "Cofre Mimético", "d": "El cofre muerde.", "s": None, "dif": 14},
            {"n": "Trampa de Fuego", "d": "¡Llamas!", "s": "agilidad", "dif": 13},
            {"n": "Puerta de Hierro", "d": "Pesada.", "s": "fuerza", "dif": 15},
            {"n": "Acertijo Mortal", "d": "Enigma antiguo.", "s": "inteligencia", "dif": 12},
            {"n": "Runa Explosiva", "d": "Magia inestable.", "s": None, "dif": 11},
            {"n": "Puente Colgante", "d": "Equilibrio.", "s": "agilidad", "dif": 15},
            {"n": "Derrumbe", "d": "¡Piedras!", "s": "fuerza", "dif": 16},
            {"n": "Espectro", "d": "Duelo mental.", "s": "inteligencia", "dif": 14},
            {"n": "Niebla Venenosa", "d": "No respires.", "s": None, "dif": 13},
            {"n": "Piso Resbaladizo", "d": "Aceite goblin.", "s": "agilidad", "dif": 12}
        ]

        if st.session_state.sala_actual <= 5:
            st.subheader(f"Sala actual: {st.session_state.sala_actual} / 5")
            
            # Elección de camino
            camino = st.radio("El pasillo se divide:", ["Izquierda", "Derecha"], horizontal=True)
            
            # Elección de Héroe
            nombres_vivos = [p['nombre'] for p in st.session_state.gremio]
            heroe_nombre = st.selectbox("¿Quién avanza?", nombres_vivos)
            
            # --- 2. BOTÓN DE ACCIÓN Y LÓGICA DE DAÑO ---
if st.button("¡AVANZAR A LA SIGUIENTE SALA!"):
    evento = random.choice(eventos)
    st.warning(f"⚠️ **SALA {st.session_state.sala_actual}:** {evento['n']} - {evento['d']}")
    
    # Tirada de dados
    dados = sum([random.randint(1, 6) for _ in range(3)])
    bono = heroe['stats'].get(evento['s'], 0) if evento['s'] else 0
    total_tirada = dados + bono
    
    st.write(f"🎲 Tirada: {dados} + bono {bono} = **{total_tirada}** (Dificultad: {evento['dif']})")

    if total_tirada >= evento['dif']:
        st.success(f"✨ ¡ÉXITO! {heroe['nombre']} superó el desafío sin rasguños.")
        st.session_state.sala_actual += 1
    else:
        # NIVEL 3: Cálculo de daño
        puntos_daño = random.randint(25, 45) # Podés subir o bajar este rango
        heroe['hp_actual'] -= puntos_daño
        
        # Validamos que no sea menor a 0
        if heroe['hp_actual'] <= 0:
            heroe['hp_actual'] = 0
            st.error(f"💀 ¡TRAGEDIA! {heroe['nombre']} recibió {puntos_daño} de daño y ha muerto.")
            st.session_state.gremio.remove(heroe)
        else:
            st.error(f"💥 ¡FALLO! {heroe['nombre']} recibió {puntos_daño} de daño, pero sigue en pie.")
            # Opcional: Avanzar de sala igual aunque reciba daño
            # st.session_state.sala_actual += 1 

    # Forzamos recarga para que la barra de vida se actualice arriba
    st.rerun()
        else:
            st.success("🏆 ¡EL GREMIO HA CONQUISTADO LA MAZMORRA!")
            if st.button("Reiniciar Aventura"):
                st.session_state.sala_actual = 1
                st.rerun()

# Mostrar el historial abajo
with st.expander("Ver miembros actuales del Gremio"):
    st.table(st.session_state.gremio)

