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
        database="HugoC$SaresTL",
    )


# Endpoint de Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

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

        if user and password == user["contraseñaR"]:
            return (
                jsonify(
                    {"status": "success", "message": "Login exitoso", "user": user}
                ),
                200,
            )
        else:
            return (
                jsonify({"status": "error", "message": "Credenciales incorrectas"}),
                401,
            )

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
    phoneNumber = data.get("phoneNumber")
    gender = data.get("gender")
    dateOfBirth = data.get("dateOfBirth")
    user = data.get("user")
    password = data.get("password")
    userType = data.get("userType")

    # Validación básica: asegurar que no falten parámetros
    if not all([name, email, department, phoneNumber, gender, dateOfBirth, user, password, userType]):
        return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verificar si el usuario ya existe
        cursor.execute("SELECT idUsuarioR FROM UsuarioR WHERE idUsuarioR = %s", (user,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"status": "error", "message": "El usuario ya existe"}), 409

        # Insertar nuevo usuario en la base de datos
        rol = 3 if userType == 'Administrador' else 2  # Rol predeterminado según el tipo de usuario
        cursor.execute(
            """
            INSERT INTO UsuarioR (idUsuarioR, contraseñaR, nombreR, correoR, telefonoR, generoR, fechaNacimientoR, idRol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (user, password, name, email, phoneNumber, gender, dateOfBirth, rol),
        )

        # Obtener el ID del usuario insertado
        idUsuarioR = cursor.lastrowid

        # Realizar las inserciones adicionales si es Administrador
        if userType == 'Administrador':
            cursor.execute(
                "INSERT INTO DocenteAdmin (departamento, idUsD) VALUES (%s, %s)",
                (department, idUsuarioR),
            )
            cursor.execute(
                "INSERT INTO es (idUsuario, clave) VALUES (%s, %s)",
                (user, user),
            )

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
    if not user:
        return jsonify({"status": "error", "message": "El parámetro 'user' es obligatorio"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Consulta para obtener tipo de usuario
        cursor.execute(
            """
            SELECT nombreR, idRol FROM UsuarioR WHERE idUsuarioR = %s
            """,
            (user,),
        )
        user_type = cursor.fetchone()

        if user_type:
            return jsonify({
                "status": "success",
                "message": "Tipo de usuario encontrado",
                "userName": user_type["nombreR"],
                "userRole": user_type["idRol"]
            }), 200
        else:
            return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": f"Error en la base de datos: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error inesperado: {str(e)}"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    app.run()
