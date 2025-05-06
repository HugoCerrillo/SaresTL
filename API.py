from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from flask import Flask
import datetime
from datetime import datetime, timedelta
import re



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
        cursor.execute("SELECT idUsuarioR, contraseñaR FROM UsuarioR WHERE idUsuarioR = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and password == user['contraseñaR']:
            return jsonify({"status": "success", "message": "Login exitoso", "user": user}), 200
        else:
            return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def validar_contraseña(password):
    if not (8 <= len(password) <= 12):
        return False, "La contraseña debe tener entre 8 y 12 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    if not re.search(r'[^A-Za-z0-9]$', password):  # carácter especial al final
        return False, "La contraseña debe terminar en un carácter especial"
    return True, ""


@app.route("/api/register", methods=["POST"])
def register():
    # Obtener los datos enviados en la solicitud
    data = request.get_json()

    # Verificar que todos los campos necesarios estén presentes y no vacíos
    required_fields = ["name", "email", "department", "semester", "phoneNumber", "gender",
                       "dateOfBirth", "user", "password", "userType"]

    if not all(data.get(field) and str(data.get(field)).strip() for field in required_fields):
        return jsonify({"status": "error", "message": "Faltan parámetros válidos"}), 400

    # Asignar variables
    name = data["name"].strip()
    email = data["email"].strip()
    department = data["department"].strip()
    semester = data["semester"]
    phoneNumber = data["phoneNumber"].strip()
    gender = data["gender"].strip()
    dateOfBirth = data["dateOfBirth"]
    user = data["user"].strip()
    password = data["password"].strip()
    userType = data["userType"].strip()

    # Asignar rol según tipo de usuario
    roles = {
        "Estudiante": 1,
        "Docente": 2,
        "Administrador": 3,
        "Administrativo": 4,
        "Intendente": 5,
        "Guardia": 6
    }
    rol = roles.get(userType, 0)
    if rol == 0:
        return jsonify({"status": "error", "message": "Tipo de usuario inválido"}), 400

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verificar si el usuario ya existe
        cursor.execute("SELECT idUsuarioR FROM UsuarioR WHERE idUsuarioR = %s", (user,))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "El usuario ya está registrado en el sistema SaresTL"}), 409

        # Verificar si el correo o contraseña ya están en uso
        cursor.execute("SELECT correoR, contraseñaR FROM UsuarioR")
        for u in cursor.fetchall():
            if u["correoR"] == email:
                return jsonify({"status": "error", "message": "El correo ya está en uso, verifícalo e intenta nuevamente."}), 409
            if u["contraseñaR"] == password:
                return jsonify({"status": "error", "message": "La contraseña ya está en uso, intenta con una nueva contraseña."}), 409

        # Verificar si el usuario es miembro de la institución
        cursor.execute("SELECT clave, estado, nombre, area FROM MiembroInstitucion WHERE clave = %s", (user,))
        member = cursor.fetchone()

        if not member:
            return jsonify({"status": "error", "message": "El usuario ingresado no es miembro de la institución"}), 409

        if member.get("estado") != "Activo":
            return jsonify({"status": "error", "message": "El usuario ingresado no es miembro activo de la institución"}), 409

        # Validar coincidencia de nombre y área
        #if name.lower() != member["nombre"].strip().lower():
        #    return jsonify({"status": "error", "message": "El nombre ingresado no coincide con ningún miembro de la institución"}), 409

        #if department.strip().lower() != member["area"].strip().lower():
        #    return jsonify({"status": "error", "message": "El área o carrera ingresada no coincide con ningún miembro de la institución"}), 409

        # Insertar el nuevo usuario en UsuarioR
        cursor.execute(
            """
            INSERT INTO UsuarioR (idUsuarioR, contraseñaR, nombreR, correoR, telefonoR, generoR, fechaNacimientoR, idRol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user, password, name, email, phoneNumber, gender, dateOfBirth, rol),
        )

        # Obtener el ID del nuevo usuario insertado
        idUsuarioR = cursor.lastrowid

        # Insertar en la tabla correspondiente dependiendo del tipo de usuario
        if userType == "Estudiante":
            cursor.execute(
                "INSERT INTO Alumno (carrera, semestre, idUsD) VALUES (%s, %s, %s)",
                (department, semester, idUsuarioR),
            )
        else:
            cursor.execute(
                "INSERT INTO DocenteAdmin (departamento, idUsD) VALUES (%s, %s)",
                (department, idUsuarioR),
            )

        # Relación en la tabla 'es'
        cursor.execute(
            "INSERT INTO es (idUsuario, clave) VALUES (%s, %s)",
            (user, user),
        )

        # Insertar foto de perfil predeterminada
        route = "../profile_pics/perfil.png"
        cursor.execute(
            "INSERT INTO Perfil (fotoPerfil, idUsuario) VALUES (%s, %s)",
            (route, user),
        )

        # Generar credencial con fecha de expiración (365 días a partir de hoy)
        expiration_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        cursor.execute(
            "INSERT INTO Credencial (codigoBarra, fechaVencimiento) VALUES (%s, %s)",
            (user, expiration_date),
        )

        # Relación con la tabla 'tiene'
        cursor.execute(
            "INSERT INTO tiene (clave) VALUES (%s)",
            (user,),
        )

        # Confirmar los cambios en la base de datos
        conn.commit()

        return jsonify({"status": "success", "message": "Usuario registrado exitosamente"}), 201

    except mysql.connector.Error as e:
        app.logger.error(f"Error en MySQL: {e}")
        return jsonify({"status": "error", "message": "Error en la base de datos"}), 500

    except Exception as e:
        app.logger.error(f"Error inesperado: {e}")
        return jsonify({"status": "error", "message": "Error interno del servidor"}), 500

    finally:
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
                #verificamos si el usuario existe o no para que no mande excepcion MySQL
                cursor.execute(
                """
                SELECT clave FROM MiembroInstitucion where clave = %s
                """,
                (clave,),
                )
                existing_member = cursor.fetchone()
                if existing_member:
                    return jsonify({"status": "error", "message": "La clave ingresada ya esta registrada en el sistema SaresTL"}), 409

                # Consulta SQL para insertar el miembro en la tabla MiembroInstitucion si es que no existe en el sistema
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





# Función para convertir posibles objetos no serializables
def convert_to_serializable(record):
    # Convertir campos 'horaR' y 'fechaR' si son objetos datetime o timedelta
    for key, value in record.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            record[key] = value.isoformat()  # Convertir a string ISO
        elif isinstance(value, datetime.timedelta):
            # Si es un timedelta, lo convertimos a segundos o minutos
            record[key] = value.total_seconds()
    return record

# Endpoint para obtener los registros
@app.route("/api/get_general_registration", methods=["GET"])
def get_general_registration():
    try:
        # Manejar la conexión y el cursor usando "with"
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Consulta para obtener todos los registros de la tabla Registro, UsuarioR y Rol
                cursor.execute("""
                    SELECT idRegistro, claveUsuario, nombreUsuario, fechaR, horaR, tipoR, tipoUsuario
                    FROM Registro
                    JOIN UsuarioR ON idUsuarioR = claveUsuario
                    JOIN Rol ON Rol.idRol = UsuarioR.idRol;
                """)

                # Obtener todos los registros
                records = cursor.fetchall()

                # Verificar si existen registros
                if records:
                    # Convertir todos los registros a un formato serializable
                    records = [convert_to_serializable(record) for record in records]

                    # Retornar la lista de registros en la respuesta
                    return jsonify({
                        "status": "success",
                        "message": "Registros encontrados",
                        "records": records
                    }), 200
                else:
                    return jsonify({"status": "error", "message": "No se encontraron registros"}), 404

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