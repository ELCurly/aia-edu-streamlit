import streamlit as st
import time

# ✅ Base de datos de estudiantes
studentsDB = [
    {
        "id": "stu001",
        "password": "stu001",
        "nombre": "Juan Pérez",
        "carrera": "Ingeniería de Sistemas",
        "semestre": "1er Semestre",
        "promedio": 14.5,
        "fortalezas": ["Física", "Teoría de Sistemas"],
        "areasMejora": ["Cálculo", "Redacción"],
        "materiasCompletas": ["Álgebra", "Geometría"],
        "proximosExamenes": ["Cálculo - 15/07/2025", "Redacción - 20/07/2025"],
        "tareasPendientes": 3,
        "horasEstudio": 25
    },
    {
        "id": "stu002",
        "password": "stu002",
        "nombre": "María Gómez",
        "carrera": "Ingeniería Civil",
        "semestre": "2do Semestre",
        "promedio": 16.8,
        "fortalezas": ["Matemática", "Programación"],
        "areasMejora": ["Inglés", "Historia"],
        "materiasCompletas": ["Algoritmos", "Estructuras de Datos"],
        "proximosExamenes": ["Inglés - 18/07/2025", "Historia - 22/07/2025"],
        "tareasPendientes": 1,
        "horasEstudio": 32
    },
    {
        "id": "stu003",
        "password": "stu003",
        "nombre": "Carlos López",
        "carrera": "Psicología",
        "semestre": "3er Semestre",
        "promedio": 13.2,
        "fortalezas": ["Química", "Biología"],
        "areasMejora": ["Estadística", "Literatura"],
        "materiasCompletas": ["Química Orgánica"],
        "proximosExamenes": ["Estadística - 16/07/2025", "Literatura - 25/07/2025"],
        "tareasPendientes": 5,
        "horasEstudio": 18
    }
]

# ✅ Login
def login():
    st.title("🔐 Asesor Académico")
    id_input = st.text_input("ID de Estudiante")
    pwd_input = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        user = next((u for u in studentsDB if u["id"] == id_input and u["password"] == pwd_input), None)
        if user:
            st.session_state.user = user
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("❌ Credenciales incorrectas")

# ✅ Menú lateral fijo
def sidebar_menu():
    st.sidebar.title("📋 Menú")
    menu = st.sidebar.radio("Navegación", ["🏠 Dashboard", "📈 Recomendaciones", "🤖 Asistente ARIA", "👤 Perfil", "🚪 Cerrar Sesión"])
    if menu == "🚪 Cerrar Sesión":
        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.rerun()
    else:
        st.session_state.page = menu

# ✅ Dashboard
def dashboard(user):
    st.title("🏠 Dashboard")
    st.header(f"👋 Bienvenido, {user['nombre']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Promedio General", user['promedio'])
    col2.metric("📌 Tareas Pendientes", user['tareasPendientes'])
    col3.metric("🕒 Horas de Estudio", f"{user['horasEstudio']}h")

    st.subheader("🎯 Fortalezas")
    for f in user['fortalezas']:
        st.success(f"✔️ {f}")

    st.subheader("⚠️ Áreas de Oportunidad")
    for a in user['areasMejora']:
        st.warning(f"🔶 {a}")

# ✅ Recomendaciones con colores mejorados
def recomendaciones(user):
    st.title("📈 Recomendaciones")
    st.markdown("Aquí tienes recomendaciones personalizadas para mejorar tu rendimiento académico.")

    # 🎨 Tarjetas para áreas de mejora
    for area in user['areasMejora']:
        st.markdown(
            f"""
            <div style="
                border:1px solid #EF9A9A;
                border-radius:12px;
                padding:15px;
                margin-bottom:15px;
                background-color:#FFEBEE;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            ">
                <h4 style="color:#C62828; margin:0;">🔴 Reforzar: {area}</h4>
                <p style="color:#555;">💡 Es importante que trabajes en <b>{area}</b> para fortalecer tu desempeño en esta área.</p>
                <p style="color:#777;">📅 Considera sesiones de estudio semanales para consolidar el aprendizaje.</p>
            </div>
            """, unsafe_allow_html=True
        )

    # 🎨 Tarjetas para fortalezas
    for fortaleza in user['fortalezas']:
        st.markdown(
            f"""
            <div style="
                border:1px solid #A5D6A7;
                border-radius:12px;
                padding:15px;
                margin-bottom:15px;
                background-color:#E8F5E9;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            ">
                <h4 style="color:#2E7D32; margin:0;">🟢 Mantener: {fortaleza}</h4>
                <p style="color:#555;">🎯 Continúa reforzando tus conocimientos en <b>{fortaleza}</b>.</p>
                <p style="color:#777;">📖 Considera profundizar con materiales avanzados o participar en tutorías especializadas.</p>
            </div>
            """, unsafe_allow_html=True
        )

# ✅ Asistente ARIA
def asistente_aria(user):
    st.title("🤖 Asistente ARIA")
    st.info(f"Hola {user['nombre']} 👋, soy ARIA. Pregúntame sobre matemáticas o temas académicos.")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"sender": "aria", "text": "¡Hola! Soy ARIA, tu asistente académico."}]

    for msg in st.session_state.messages:
        if msg["sender"] == "user":
            st.chat_message("user").markdown(f"**Tú:** {msg['text']}")
        else:
            st.chat_message("assistant").markdown(f"**ARIA:** {msg['text']}")

    user_input = st.chat_input("Escribe tu mensaje aquí...")
    if user_input:
        st.session_state.messages.append({"sender": "user", "text": user_input})
        st.chat_message("user").markdown(f"**Tú:** {user_input}")

        with st.chat_message("assistant"):
            with st.spinner("ARIA está escribiendo..."):
                time.sleep(1.2)
                try:
                    result = eval(user_input)
                    response = f"📐 El resultado de '{user_input}' es: {result}"
                except:
                    response = "🤖 No entendí eso. Intenta con una operación matemática."
                st.session_state.messages.append({"sender": "aria", "text": response})
                st.markdown(f"**ARIA:** {response}")

# ✅ Perfil
def perfil(user):
    st.title("👤 Perfil del Usuario")
    st.write(f"**Nombre:** {user['nombre']}")
    st.write(f"**Carrera:** {user['carrera']}")
    st.write(f"**Semestre:** {user['semestre']}")
    st.write(f"**Promedio:** {user['promedio']}")
    st.write(f"**Horas de Estudio:** {user['horasEstudio']}")
    st.write(f"**Materias Completas:** {', '.join(user['materiasCompletas'])}")
    st.write(f"**Próximos Exámenes:** {', '.join(user['proximosExamenes'])}")

# ✅ App principal
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if st.session_state.user:
    sidebar_menu()
    if st.session_state.page == "🏠 Dashboard":
        dashboard(st.session_state.user)
    elif st.session_state.page == "📈 Recomendaciones":
        recomendaciones(st.session_state.user)
    elif st.session_state.page == "🤖 Asistente ARIA":
        asistente_aria(st.session_state.user)
    elif st.session_state.page == "👤 Perfil":
        perfil(st.session_state.user)
else:
    login()
