import tensorflow as tf
import numpy as np

# Datos ficticios para estudiantes y carreras
student_ids = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
career_ids = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])  # 0: Ing Sistemas, 1: Medicina, 2: Contaduría
course_ids = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

# Cursos por carrera (ordenado por índice)
career_courses = {
    0: [0, 1, 2],  # Ing Sistemas: Desarrollo de software, Java, Python
    1: [3, 4, 5],  # Medicina: Anatomía y Fisiología, Bioquímica, Patología
    2: [6, 7, 8]   # Contaduría: Contabilidad Financiera, Contabilidad de Costos, Contabilidad Forense
}

# Asignar calificaciones ficticias
ratings = np.array([5, 4, 3, 5, 4, 4, 5, 3, 4])

# Construir embeddings para estudiantes y cursos
student_input = tf.keras.layers.Input(shape=(1,))
course_input = tf.keras.layers.Input(shape=(1,))

student_embedding = tf.keras.layers.Embedding(input_dim=len(student_ids), output_dim=5)(student_input)
course_embedding = tf.keras.layers.Embedding(input_dim=len(course_ids), output_dim=5)(course_input)

# Aplanar las capas de embeddings
student_vec = tf.keras.layers.Flatten()(student_embedding)
course_vec = tf.keras.layers.Flatten()(course_embedding)

# Calcular el producto punto
dot_product = tf.keras.layers.Dot(axes=1)([student_vec, course_vec])

# Crear el modelo
model = tf.keras.Model(inputs=[student_input, course_input], outputs=dot_product)
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(x=[student_ids, course_ids], y=ratings, epochs=50)

# Guardar el modelo entrenado
model.save('career_recommender_model.h5')
