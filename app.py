import streamlit as st
import random

# --- Datos simulados de estudiantes ---
students = {
    "stu001": {
        "name": "Juan Pérez",
        "career": "Ingeniería de Sistemas",
        "semester": "1er Semestre",
        "gpa": 15.6,
        "strengths": ["Teoría de Sistemas", "Física"],
        "weaknesses": ["Redacción", "Cálculo"]
    },
    "stu002": {
        "name": "María García",
        "career": "Ingeniería Civil",
        "semester": "2do Semestre",
        "gpa": 14.3,
        "strengths": ["Estática", "Geometría"],
        "weaknesses": ["Programación", "Redacción"]
    },
    "stu003": {
        "name": "Carlos López",
        "career": "Psicología",
        "semester": "3er Semestre",
        "gpa": 16.1,
        "strengths": ["Psicología Cognitiva", "Estadística"],
        "weaknesses": ["Biología", "Filosofía"]
    }
}

# --- Recomendaciones comunes ---
recommendations = [
    {
        "type": "Recurso de Aprendizaje",
        "title": "Taller de Redacción Académica",
        "description": "Mejora tus habilidades de escritura y comprensión lectora",
        "priority": "Alta",
        "estimated_time": "4 semanas"
    },
    {
        "type": "Tutoría",
        "title": "Tutoría en Cálculo",
        "description": "Refuerzo en límites y derivadas",
        "priority": "Alta",
        "estimated_time": "2 horas semanales"
    },
    {
        "type": "Actividad Práctica",
        "title": "Laboratorio de Física",
        "description": "Fortalece tus conceptos teóricos con práctica",
        "priority": "Media",
        "estimated_time": "3 horas semanales"
    }
]

# --- Simulación de respuestas IA sin API ---
def simulated_response(message, student):
    msg = message.lower()
    responses = []

    if any(word in msg for word in ["hola", "buenas", "hey"]):
        responses = [
            f"¡Hola {student['name']}! ¿En qué puedo ayudarte hoy?",
            "¡Bienvenido de nuevo! Estoy aquí para apoyarte.",
            "Saludos, listo para ayudarte en tu camino académico."
        ]
    elif "promedio" in msg or "nota" in msg:
        responses = [
            f"Tu promedio actual es de {student['gpa']} sobre 20.",
            f"Estás manteniendo un promedio de {student['gpa']} puntos. ¡Sigue así!",
            f"Tu rendimiento actual es de {student['gpa']}/20."
        ]
    elif "fortaleza" in msg or "bueno" in msg:
        strengths = ", ".join(student['strengths'])
        responses = [
            f"Destacas especialmente en: {strengths}.",
            f"Tus principales fortalezas académicas son: {strengths}.",
            f"Excelente trabajo en: {strengths}."
        ]
    elif "debilidad" in msg or "mejorar" in msg:
        weaknesses = ", ".join(student['weaknesses'])
        responses = [
            f"Podrías mejorar en: {weaknesses}.",
            f"Te recomiendo reforzar estas áreas: {weaknesses}.",
            f"Áreas a mejorar detectadas: {weaknesses}."
        ]
    elif "recomendación" in msg or "sugerencia" in msg:
        responses = [
            "Puedes revisar la pestaña de recomendaciones para recursos útiles.",
            "Te sugiero revisar los talleres disponibles en tu sección de recomendaciones.",
            "Las recomendaciones están personalizadas en la pestaña correspondiente."
        ]
    else:
        responses = [
            "Puedes preguntarme por tu promedio, fortalezas, debilidades o recomendaciones.",
            "Estoy aquí para ayudarte con tu rendimiento académico.",
            "No entendí bien tu mensaje, pero puedo ayudarte con tu progreso académico."
        ]

    return random.choice(responses)

# --- Configuración de sesión ---
st.set_page_config("IA Asesor Académico", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_id" not in st.session_state:
    st.session_state.current_id = None
if "chat" not in st.session_state:
    st.session_state.chat = []

st.title("🧠 IA Asesor Académico")
st.caption("Universidad Nacional del Centro del Perú — Proyecto 2025")

# --- Inicio de sesión ---
if not st.session_state.logged_in:
    st.subheader("🔐 Iniciar Sesión")
    user_id = st.text_input("Ingresa tu ID de estudiante (ej. stu001)")
    if st.button("Ingresar"):
        if user_id in students:
            st.session_state.logged_in = True
            st.session_state.current_id = user_id
            st.success("Inicio de sesión exitoso")
        else:
            st.error("ID no válido. Usa stu001, stu002 o stu003")
    st.stop()

# --- Datos del estudiante logueado ---
student = students[st.session_state.current_id]

# --- Menú lateral ---
st.sidebar.title("👤 Menú")
st.sidebar.write(f"Estudiante: {student['name']}")
if st.sidebar.button("Cerrar sesión"):
    st.session_state.logged_in = False
    st.session_state.current_id = None
    st.session_state.chat = []
    st.rerun()

tab = st.sidebar.radio("Ir a:", ["📊 Panel", "🎯 Recomendaciones", "💬 Asistente", "📋 Perfil"])

# --- Panel de rendimiento ---
if tab == "📊 Panel":
    st.subheader("📊 Panel de Rendimiento Académico")
    st.metric("Promedio General", f"{student['gpa']}/20")
    st.write("### Fortalezas")
    st.success(", ".join(student["strengths"]))
    st.write("### Áreas de Mejora")
    st.warning(", ".join(student["weaknesses"]))

# --- Recomendaciones ---
elif tab == "🎯 Recomendaciones":
    st.subheader("🎯 Recomendaciones Personalizadas")
    for rec in recommendations:
        with st.expander(f"{rec['title']} [{rec['priority']}]"):
            st.write(f"**Tipo:** {rec['type']}")
            st.write(rec["description"])
            st.write(f"⏳ Tiempo estimado: {rec['estimated_time']}")

# --- Chat Asistente ---
elif tab == "💬 Asistente":
    st.subheader("💬 Chat con tu Asistente IA")
    for entry in st.session_state.chat:
        if entry["role"] == "user":
            st.write(f"🧑 Tú: {entry['msg']}")
        else:
            st.info(f"🤖 IA: {entry['msg']}")
    message = st.text_input("Escribe tu mensaje", key="chat_input")
    if st.button("Enviar"):
        if message.strip():
            st.session_state.chat.append({"role": "user", "msg": message})
            response = simulated_response(message, student)
            st.session_state.chat.append({"role": "bot", "msg": response})
            st.rerun()

# --- Perfil del estudiante ---
elif tab == "📋 Perfil":
    st.subheader("📋 Perfil del Estudiante")
    st.write(f"**Nombre:** {student['name']}")
    st.write(f"**Carrera:** {student['career']}")
    st.write(f"**Semestre:** {student['semester']}")
    st.write(f"**Promedio:** {student['gpa']}")
    st.write(f"**Fortalezas:** {', '.join(student['strengths'])}")
    st.write(f"**Áreas de Mejora:** {', '.join(student['weaknesses'])}")
