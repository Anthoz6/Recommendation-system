import streamlit as st
import pandas as pd
import tensorflow as tf
from data_courses import get_all_courses, get_courses_for_career
from data_students import get_students

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def app():
    # Cargar el modelo entrenado
    model = tf.keras.models.load_model('career_recommender_model.h5')

    # Aplicar CSS
    load_css('static/style.css')

    st.title('Sistema de Recomendación de Cursos por Carrera')

    # Obtener los estudiantes de la base de datos
    students = get_students()

    # Seleccionar estudiante por su ID
    student_ids = [student[0] for student in students]
    selected_student_id = st.selectbox('Selecciona tu ID de estudiante', student_ids)

    # Obtener el estudiante seleccionado por su ID
    selected_student = next(student for student in students if student[0] == selected_student_id)
    student_name = selected_student[1]
    default_career = selected_student[2]

    st.write(f'Bienvenido, {student_name}. Tu carrera es {default_career}.')

        # Cargar todos los cursos de la base de datos
    all_courses = get_all_courses()

    # Verificar si se han recuperado cursos
    if not all_courses:
        st.write("No se han encontrado cursos en la base de datos.")
        return

    # Campo de búsqueda
    search_query = st.text_input('Buscar cursos:')

    # Filtrar los cursos según la búsqueda
    if search_query:
        filtered_courses = [course for course in all_courses if search_query.lower() in course[0].lower()]
    else:
        filtered_courses = all_courses
    
    # Mostrar resultados solo si hay una consulta de búsqueda
    if search_query:
        filtered_courses = [course for course in all_courses if search_query.lower() in course[0].lower()]

        # Mostrar cursos filtrados
        st.subheader('Resultados de la búsqueda:')
        
        if filtered_courses:
            cols = st.columns(len(filtered_courses))
            for idx, (course, image_url) in enumerate(filtered_courses):
                with cols[idx]:
                    st.image(image_url if image_url else 'https://via.placeholder.com/150', use_column_width=True)
                    st.write(course)
        else:
            st.write("No se encontraron cursos que coincidan con la búsqueda.")

    # Mostrar recomendaciones basadas en la carrera seleccionada automáticamente al cambiar de estudiante
    recommended_courses = get_courses_for_career(default_career)

    if recommended_courses:
        st.write(f'Cursos recomendados para {default_career}:')

        cols = st.columns(len(recommended_courses))
        for idx, (course_name, image_url) in enumerate(recommended_courses):
            with cols[idx]:
                st.image(image_url if image_url else 'https://via.placeholder.com/150', use_column_width=True)
                st.write(course_name)
    else:
        st.write(f'No hay recomendaciones disponibles para {default_career}.')

    # Mostrar cursos
    st.subheader('Todos los Cursos Disponibles:')

    all_courses = get_all_courses()

    if all_courses:
        cols = st.columns(len(all_courses))  # Dividir las columnas en base a la cantidad de cursos disponibles
        for idx, (course_name, image_url) in enumerate(all_courses):
            with cols[idx % len(cols)]:  # Mostrar cada curso en una columna
                st.image(image_url if image_url else 'https://via.placeholder.com/150', use_column_width=True)
                st.write(course_name)
    else:
        st.write("No hay cursos disponibles.")
