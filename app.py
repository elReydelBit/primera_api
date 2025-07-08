# Importamos los módulos necesarios de Flask
from flask import Flask, request, jsonify

# Flask es el framework principal
# request nos permite acceder a los datos enviados por el cliente
# jsonify convierte datos de Python a formato JSON para las respuestas API

# Creamos una instancia de la aplicación Flask
# __name__ es una variable especial que toma el nombre del módulo actual
app = Flask(__name__)

# Creamos una "base de datos" simple usando una lista de diccionarios en memoria
# En un caso real, usaríamos una base de datos como PostgreSQL, MySQL o MongoDB
tareas = [
    {"id": 1, "titulo": "Aprender APIs", "completada": False},
    {"id": 2, "titulo": "Hacer ejercicio", "completada": False}
]


# ----- RUTAS DE LA API -----

# Ruta para obtener todas las tareas (método HTTP: GET)
# El decorador @app.route define la URL y los métodos HTTP permitidos
@app.route('/api/tareas', methods=['GET'])
def obtener_tareas():
    # Simplemente devolvemos todas las tareas en formato JSON
    # jsonify convierte el diccionario Python a JSON
    return jsonify({"tareas": tareas})


# Ruta para obtener una tarea específica por su ID (método HTTP: GET)
# <int:tarea_id> es un parámetro de ruta, donde Flask extraerá el valor
# y lo pasará a la función como parámetro
@app.route('/api/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    # Buscamos la tarea con el ID especificado
    # next() con una expresión generadora nos da el primer elemento que cumple la condición
    # Si no hay coincidencias, devuelve None
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)

    # Si encontramos la tarea, la devolvemos
    if tarea:
        return jsonify({"tarea": tarea})

    # Si no encontramos la tarea, devolvemos un error 404 (No encontrado)
    # El segundo valor (404) es el código de estado HTTP
    return jsonify({"error": "Tarea no encontrada"}), 404


# Ruta para crear una nueva tarea (método HTTP: POST)
@app.route('/api/tareas', methods=['POST'])
def crear_tarea():
    # Verificamos que la solicitud contiene datos JSON y tiene el campo 'titulo'
    # request.json contiene los datos enviados en formato JSON
    if not request.json or not 'titulo' in request.json:
        # Si falta información, devolvemos un error 400 (Solicitud incorrecta)
        return jsonify({"error": "El título es requerido"}), 400

    # Creamos la nueva tarea
    # - Generamos un nuevo ID (el último ID + 1, o 1 si no hay tareas)
    # - Tomamos el título del JSON recibido
    # - Por defecto, la tarea está como no completada
    nueva_tarea = {
        "id": tareas[-1]["id"] + 1 if tareas else 1,
        "titulo": request.json["titulo"],
        "completada": False
    }

    # Añadimos la nueva tarea a nuestra "base de datos"
    tareas.append(nueva_tarea)

    # Devolvemos la tarea creada con código 201 (Creado)
    return jsonify({"tarea": nueva_tarea}), 201


# Ruta para actualizar una tarea existente (método HTTP: PUT)
@app.route('/api/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    # Buscamos la tarea que queremos actualizar
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)

    # Si no encontramos la tarea, devolvemos error 404
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Verificamos que la solicitud contiene datos JSON
    if not request.json:
        return jsonify({"error": "No hay datos para actualizar"}), 400

    # Actualizamos el título si viene en la solicitud
    if 'titulo' in request.json:
        tarea['titulo'] = request.json['titulo']

    # Actualizamos el estado de completado si viene en la solicitud
    if 'completada' in request.json:
        tarea['completada'] = request.json['completada']

    # Devolvemos la tarea actualizada
    return jsonify({"tarea": tarea})


# Ruta para eliminar una tarea (método HTTP: DELETE)
@app.route('/api/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    # Buscamos la tarea a eliminar
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)

    # Si no encontramos la tarea, devolvemos error 404
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Eliminamos la tarea de nuestra "base de datos"
    tareas.remove(tarea)

    # Devolvemos confirmación de eliminación
    return jsonify({"resultado": "Tarea eliminada"})


# Punto de entrada de la aplicación
# Este bloque se ejecuta solo cuando ejecutamos este archivo directamente
if __name__ == '__main__':
    # app.run inicia el servidor web local de Flask
    # debug=True activa el modo de depuración:
    # - Muestra errores detallados en el navegador
    # - Recarga automáticamente cuando hay cambios en el código
    app.run(debug=True)