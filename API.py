from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from flask import Flask

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen

# Conectar a MySQL en PythonAnywhere
def get_db_connection():
    return mysql.connector.connect(
        host="HugoC.mysql.pythonanywhere-services.com",
        user="HugoC",
        password="Contrasena123*",
        database="HugoC$SaresTL"
    )

# Endpoint de Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Buscar usuario en la base de datos
        cursor.execute("SELECT * FROM UsuarioR WHERE idUsuarioR = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and password == user['contraseñaR']:
            return jsonify({"status": "success", "message": "Login exitoso", "user": user}), 200
        else:
            return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/register", methods=["POST"])
def register():
    # Obtener los datos enviados en la solicitud
    data = request.get_json()

    # Extraer los parámetros necesarios
    name = data.get("name")
    email = data.get("email")
    department = data.get("department")
    semester = data.get("semester")
    phoneNumber = data.get("phoneNumber")
    gender = data.get("gender")
    dateOfBirth = data.get("dateOfBirth")
    user = data.get("user")
    password = data.get("password")
    userType = data.get("userType")

    # Validación básica: asegurar que no falten parámetros
    if not all([name, email, department, semester, phoneNumber, gender, dateOfBirth, user, password, userType]):
        return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

    # Mapear los tipos de usuario a roles
    user_roles = {
        'Estudiante': 1,
        'Docente': 2,
        'Administrador': 3,
        'Administrativo': 4,
        'Intendente': 5,
        'Guardia': 6
    }

    # Obtener el rol basado en el tipo de usuario
    rol = user_roles.get(userType)
    if rol is None:
        return jsonify({"status": "error", "message": "Tipo de usuario inválido"}), 400

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verificar si el usuario ya existe
        cursor.execute("SELECT idUsuarioR FROM UsuarioR WHERE idUsuarioR = %s", (user,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"status": "error", "message": "El usuario ya existe"}), 409

        # Insertar el nuevo usuario
        cursor.execute(
            """
            INSERT INTO UsuarioR (idUsuarioR, contraseñaR, nombreR, correoR, telefonoR, generoR, fechaNacimientoR, idRol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user, password, name, email, phoneNumber, gender, dateOfBirth, rol),
        )

        # Obtener el ID del usuario insertado
        idUsuarioR = cursor.lastrowid

        # Insertar datos adicionales según el tipo de usuario
        if userType == 'Estudiante':
            cursor.execute(
                "INSERT INTO Alumno (carrera, semestre, idUsD) VALUES (%s, %s, %s)",
                (department, semester, idUsuarioR),
            )
        else:
            cursor.execute(
                "INSERT INTO DocenteAdmin (departamento, idUsD) VALUES (%s, %s)",
                (department, idUsuarioR),
            )

        # Insertar datos en la tabla 'es' para la relación de usuario y clave
        cursor.execute(
            "INSERT INTO es (idUsuario, clave) VALUES (%s, %s)",
            (user, user),
        )

        # Insertar la foto de perfil predeterminada
        route = "../profile_pics/perfil.png"
        cursor.execute(
            "INSERT INTO Perfil (fotoPerfil, idUsuario) VALUES (%s, %s)",
            (route, user),
        )

        # Confirmar los cambios en la base de datos
        conn.commit()

        return jsonify({"status": "success", "message": "Usuario registrado exitosamente"}), 201

    except mysql.connector.Error as e:
        # Log del error en la base de datos
        app.logger.error(f"Error en MySQL: {e}")
        return jsonify({"status": "error", "message": "Error en la base de datos"}), 500

    except Exception as e:
        # Log de errores generales
        app.logger.error(f"Error inesperado: {e}")
        return jsonify({"status": "error", "message": "Error interno del servidor"}), 500

    finally:
        # Cerrar conexión y cursor (asegurarse de que siempre se cierren)
        try:
            cursor.close()
            conn.close()
        except:
            pass


@app.route("/api/usertype", methods=["POST"])
def usertype():
    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.get_json()
    user = data.get("user")

    # Validar parámetro
    if not user or not str(user).strip():
        return jsonify({"status": "error", "message": "El parámetro 'user' es obligatorio y debe ser válido"}), 400

    try:
        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Consulta para obtener el tipo de usuario
                cursor.execute("""
                    SELECT nombreR, idRol, tipo FROM UsuarioR inner join MiembroInstitucion on MiembroInstitucion.clave = UsuarioR.idUsuarioR WHERE UsuarioR.idUsuarioR = %s
                """, (user,))
                user_type = cursor.fetchone()

                # Validar si el usuario fue encontrado
                if user_type:
                    return jsonify({
                        "status": "success",
                        "message": "Tipo de usuario encontrado",
                        "userName": str(user_type["nombreR"]).strip(),
                        "userRole": user_type["idRol"],
                        "userTypeInst": user_type["tipo"]
                    }), 200
                else:
                    return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/userPicture", methods=["POST"])
def userPicture():
    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.get_json()
    user = data.get("user")

    # Validar parámetro
    if not user or not str(user).strip():
        return jsonify({"status": "error", "message": "El parámetro 'user' es obligatorio y debe ser válido"}), 400

    try:
        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Consulta para obtener el tipo de usuario
                cursor.execute("""
                    SELECT fotoPerfil FROM Perfil WHERE idUsuario = %s
                """, (user,))
                user_profile = cursor.fetchone()

                # Validar si el usuario fue encontrado
                if user_profile:
                    return jsonify({
                        "status": "success",
                        "message": "Tipo de usuario encontrado",
                        "userPicture": str(user_profile["fotoPerfil"]).strip()
                    }), 200
                else:
                    return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500



@app.route("/api/verifyEmail", methods=["POST"])
def verify_email():
    data = request.get_json()
    email = data.get("email")

    # Validación
    if not email or not str(email).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'email' es obligatorio y debe ser válido"
        }), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT correoR, idUsuarioR FROM UsuarioR WHERE correoR = %s
                """, (email,))
                result = cursor.fetchone()

                if result:
                    return jsonify({
                        "status": "success",
                        "message": "Correo de usuario encontrado",
                        "userMail": result["correoR"],
                        "userId": result["idUsuarioR"]
                    }), 200
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Usuario no encontrado"
                    }), 404

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/resetPassword", methods=["POST"])
def reset_password():
    data = request.get_json()
    user_id = data.get("idUsuarioR")
    new_password = data.get("newPassword")

    # Validación de parámetros
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "El parámetro 'idUsuarioR' es obligatorio"
         }), 400

    if not new_password or len(new_password.strip()) < 6:
        return jsonify({
            "status": "error",
            "message": "El parámetro 'newPassword' es obligatorio y debe tener al menos 6 caracteres"
        }), 400

    # Aquí podrías añadir más validaciones de seguridad para la contraseña (como longitud mínima, caracteres especiales, etc.)

    try:
        # Conexión a la base de datos
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Actualizar la contraseña
                cursor.execute("""
                    UPDATE UsuarioR
                    SET contraseñaR = %s
                    WHERE idUsuarioR = %s
                """, (new_password, user_id))

                # Cometer los cambios a la base de datos
                conn.commit()

                # Verificar si se actualizó alguna fila
                if cursor.rowcount > 0:
                    return jsonify({
                        "status": "success",
                        "message": "Contraseña actualizada correctamente"
                    }), 200
                else:
                    return jsonify({
                        "status": "error",
                        "message": "No se encontró un usuario con ese ID"
                    }), 404

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/obtain_institution_members", methods=["POST"])
def obtain_institution_members():
    try:
        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Consulta para obtener todos los miembros de la institución
                cursor.execute("""
                    SELECT clave, nombre, correo, genero, tipo, edad, area, estado
                    FROM MiembroInstitucion
                """)
                # Obtener todos los miembros
                members = cursor.fetchall()

                # Verificar si existen miembros
                if members:
                    # Retornar la lista de miembros en la respuesta
                    return jsonify({
                        "status": "success",
                        "message": "Miembros de la institución encontrados",
                        "members": members  # Esto contiene una lista de todos los miembros
                    }), 200
                else:
                    return jsonify({"status": "error", "message": "No se encontraron miembros"}), 404

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/register_members_institution", methods=["POST"])
def register_members_institution():
    try:
        # Obtener los datos del cuerpo de la solicitud (request)
        data = request.get_json()

        # Verificar que todos los campos necesarios estén presentes en la solicitud
        required_fields = ["clave", "nombre", "correo", "genero", "tipo", "edad", "area", "estado"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Falta el campo requerido: {field}"
                }), 400

        # Extraer los valores del cuerpo de la solicitud
        clave = data["clave"]
        nombre = data["nombre"]
        correo = data["correo"]
        genero = data["genero"]
        tipo = data["tipo"]
        edad = data["edad"]
        area = data["area"]
        estado = data["estado"]

        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Consulta SQL para insertar el miembro en la tabla MiembroInstitucion
                query = """
                    INSERT INTO MiembroInstitucion (clave, nombre, correo, genero, tipo, edad, area, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (clave, nombre, correo, genero, tipo, edad, area, estado)

                # Ejecutar la consulta
                cursor.execute(query, values)

                # Confirmar los cambios en la base de datos
                conn.commit()

        return jsonify({
            "status": "success",
            "message": "Miembro registrado exitosamente"
        }), 201

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/edit_member_institution", methods=["POST"])
def edit_member_institution():
    try:
        # Obtener los datos del cuerpo de la solicitud (request)
        data = request.get_json()

        # Verificar que todos los campos necesarios estén presentes en la solicitud
        required_fields = ["clave", "nombre", "correo", "genero", "tipo", "edad", "area", "estado"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Falta el campo requerido: {field}"
                }), 400

        # Extraer los valores del cuerpo de la solicitud
        clave = data["clave"]
        nombre = data["nombre"]
        correo = data["correo"]
        genero = data["genero"]
        tipo = data["tipo"]
        edad = data["edad"]
        area = data["area"]
        estado = data["estado"]

        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Consulta SQL para actualizar el miembro en la tabla MiembroInstitucion
                query = """
                    UPDATE MiembroInstitucion
                    SET nombre = %s, correo = %s, genero = %s, tipo = %s, edad = %s, area = %s, estado = %s
                    WHERE clave = %s
                """
                values = (nombre, correo, genero, tipo, edad, area, estado, clave)

                # Ejecutar la consulta
                cursor.execute(query, values)

                # Confirmar los cambios en la base de datos
                conn.commit()

                # Verificar si la actualización fue exitosa
                if cursor.rowcount == 0:
                    return jsonify({
                        "status": "error",
                        "message": "No se encontró un miembro con la clave proporcionada"
                    }), 404

        return jsonify({
            "status": "success",
            "message": "Miembro actualizado exitosamente"
        }), 200

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500


@app.route("/api/register_entries", methods=["POST"])
def register_entries():
    data = request.get_json()

    # Obtener parámetros
    clave = data.get("clave")
    hr = data.get("hr")
    date = data.get("date")
    typeR = data.get("typeR")
    message = data.get("message")

    # Validación de parámetros
    if not clave or not str(clave).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'clave' es obligatorio y debe ser válido"
        }), 400

    if not hr or not str(hr).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'hr' (hora de registro) es obligatorio y debe ser válido"
        }), 400

    if not date or not str(date).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'date' (fecha) es obligatorio y debe ser válido"
        }), 400

    if not typeR or not str(typeR).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'typeR' (tipo de registro) es obligatorio y debe ser válido"
        }), 400

    if not message or not str(message).strip():
        return jsonify({
            "status": "error",
            "message": "El parámetro 'message' (mensaje) es obligatorio y debe ser válido"
        }), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Comprobamos si el miembro está activo
                cursor.execute("""
                    SELECT estado, nombre FROM MiembroInstitucion WHERE clave = %s
                """, (clave,))
                result = cursor.fetchone()

                if not result:
                    return jsonify({
                        "status": "error",
                        "message": "Usuario no encontrado"
                    }), 404

                estado = result["estado"]
                name = result["nombre"]

                if estado != "Activo":
                    return jsonify({
                        "status": "error",
                        "message": "Usuario no activo"
                    }), 403  # Usar 403 para indicar que la acción no está permitida para usuarios inactivos

                # Obtener correo del usuario
                cursor.execute("""
                    SELECT correoR FROM UsuarioR WHERE idUsuarioR = %s
                """, (clave,))
                email_result = cursor.fetchone()
                if not email_result:
                    return jsonify({
                        "status": "error",
                        "message": "Correo no encontrado para el usuario"
                    }), 404
                email = email_result["correoR"]

                # Obtener la credencial
                cursor.execute("""
                    SELECT idCredencial FROM tiene WHERE clave = %s
                """, (clave,))
                cred_result = cursor.fetchone()
                if not cred_result:
                    return jsonify({
                        "status": "error",
                        "message": "Credencial no encontrada para el usuario"
                    }), 404
                idCredencial = cred_result["idCredencial"]

                # Realizar el registro de entrada
                cursor.execute("""
                    INSERT INTO Registro (claveUsuario, nombreUsuario, fechaR, horaR, idCredencial, tipoR)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (clave, name, date, hr, idCredencial, typeR))
                conn.commit()  # Commit para asegurar que se persista el registro

                # Registrar la notificación
                cursor.execute("""
                    INSERT INTO Notificaciones (fechaNotificacion, horaNotificacion, contenido, idUsuario)
                    VALUES (%s, %s, %s, %s)
                """, (date, hr, message, clave))
                conn.commit()  # Commit para asegurar que se persista la notificación

                return jsonify({
                    "status": "success",
                    "message": "Registro de acceso exitoso",
                    "clave": clave,
                    "email": email,
                    "hr": hr,
                    "date": date,
                    "message": message,
                    "name": name,
                    "typeR": typeR
                }), 200

    except mysql.connector.Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la base de datos: {str(e)}"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500



if __name__ == '__main__':
    app.run()