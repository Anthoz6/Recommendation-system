import streamlit as st
import pandas as pd
import os
from PIL import Image
from data_courses import add_course_to_db, get_courses_for_career, get_all_courses, delete_course
from data_students import create_student_database, add_student, get_students

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def save_uploaded_image(uploaded_image, course_name):
    # Crear la carpeta para guardar las imágenes si no existe
    images_dir = "course_images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Guardar la imagen con el nombre del curso
    image_path = os.path.join(images_dir, f"{course_name}.png")
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    
    return image_path

def app():
    # Aplicar CSS
    load_css('static/style.css')    

    # Crear la base de datos de estudiantes si no existe
    create_student_database()

    st.title('Sistema de Administración de Estudiantes y Cursos')

    # Mostrar la tabla de estudiantes
    st.subheader('Datos de Estudiantes')
    students = get_students()
    students_df = pd.DataFrame(students, columns=['ID', 'Nombre', 'Carrera'])
    st.dataframe(students_df)

    # Formulario para agregar un estudiante nuevo
    with st.expander("Agregar un estudiante nuevo"):
        with st.form(key="add_student_form"):
            new_student_name = st.text_input('Ingresa el nombre del estudiante:')
            new_student_career = st.selectbox('Selecciona la carrera', ["Ing Sistemas", "Medicina", "Contaduría"])
            submit_student = st.form_submit_button('Enviar')

            if submit_student:
                add_student(new_student_name, new_student_career)
                st.write(f'El estudiante "{new_student_name}" ha sido agregado correctamente.')

    # Formulario para agregar un curso nuevo con imagen y URL
    with st.expander("Agregar un curso nuevo"):
        with st.form(key="add_course_form"):
            selected_career_for_addition = st.selectbox('Selecciona la Carrera para el nuevo curso', ["Ing Sistemas", "Medicina", "Contaduría"])
            new_course = st.text_input('Ingresa el curso nuevo:')
            uploaded_image = st.file_uploader("Sube la imagen del curso", type=["png", "jpg", "jpeg"])
            course_url = st.text_input('Ingresa la URL del curso (opcional):')
            submit = st.form_submit_button('Enviar')

            if submit:
                image_path = None
                if uploaded_image is not None:
                    # Guardar la imagen y obtener la ruta
                    image_path = save_uploaded_image(uploaded_image, new_course)
                
                # Agregar curso, ruta de la imagen y URL del curso a la base de datos
                add_course_to_db(selected_career_for_addition, new_course, image_path, course_url)
                st.write(f'El curso "{new_course}" ha sido agregado correctamente para la carrera {selected_career_for_addition}.')
                
                # Mostrar los cursos actualizados
                updated_recommendations = get_courses_for_career(selected_career_for_addition)
                for course, image_url, url in updated_recommendations:
                    st.image(image_url if image_url else 'https://via.placeholder.com/150', caption=course)
                    st.markdown(f'[Ver curso]({url})', unsafe_allow_html=True)

    # Elegir el curso a eliminar
    all_courses = get_all_courses()

    course_names = [course[0] for course in all_courses]
    selected_course = st.selectbox('Selecciona un curso para eliminar', course_names)

    # Botón para eliminar el curso
    if st.button('Eliminar curso'):
        delete_course(course_name=selected_course)
        st.success(f'El curso "{selected_course}" ha sido eliminado exitosamente.')

        all_courses = get_all_courses()
        course_names = [course[0] for course in all_courses]