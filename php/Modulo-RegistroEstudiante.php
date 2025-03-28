<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="../img/sares.jpeg" type="image/x-icon">
    <title>Registro Alumno</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #6ba1ff, #b3d1ff);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 900px;
            padding: 20px;
            margin: 20px;
        }

        .form-container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        .logos {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }

        .logos img {
            max-width: 80px;
            margin: 10px;
        }

        h1 {
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
        }

        .icon {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        label {
            text-align: left;
            font-weight: bold;
            margin: 0 5px;
            color: #34495e;
        }

        input,
        select,
        button {
            width: calc(100% - 10px);
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1em;
        }

        input:focus,
        select:focus {
            border-color: #3498db;
            outline: none;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
        }

        button {
            background: #2c3e50;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background: #34495e;
        }

        @media (max-width: 768px) {
            .logos img {
                max-width: 60px;
            }

            h1 {
                font-size: 1.5em;
            }

            .icon {
                width: 80px;
                height: 80px;
            }

            .form-container {
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="form-container">
            <div class="logos">
                <img src="../img/sep.png" alt="SEP Logo">
                <img src="../img/tecnm.jpg" alt="TECNM Logo">
                <img src="../img/tec.png" alt="ITL Logo">
                <img src="../img/sares.jpeg" alt="SARES Logo">
            </div>
            <h1>Registro de estudiantes</h1>
            <img src="../img/person-circle.svg" class="icon" alt="User Icon">
            <form action="../php/procesar.php" method="POST">
                <div>
                    <input type="hidden" id="formulario" name="formulario" value="studentType">
                </div>
                <label for="nombre">Nombre:</label>
                <input type="text" id="name" name="name" required>

                <label for="correo">Correo Institucional:</label>
                <input type="email" id="email" name="email" required>

                <label for="carrera">Carrera:</label>
                <select name="career" id="career" required>
                    <option value="">Seleccione una opción</option>
                    <option value="Ingeniería en Gestión Empresarial">Ingeniería en Gestión Empresarial</option>
                    <option value="Ingeniería Industrial">Ingeniería Industrial</option>
                    <option value="Ingeniería en Sistemas Computacionales">Ingeniería en Sistemas Computacionales
                    </option>
                    <option value="Ingeniería en Tecnologías de la Información y Comunicación">Ingeniería en
                        Tecnologías de la Información y Comunicación</option>
                    <option value="Ingeniería en Logística">Ingeniería en Logística</option>
                    <option value="Ingeniería en Electromecánica">Ingeniería en Electromecánica</option>
                    <option value="Ingeniería en Electrónica">Ingeniería en Electrónica</option>
                    <option value="Ingeniería en Mecatrónica">Ingeniería en Mecatrónica</option>
                </select>

                <label for="semestre">Semestre:</label>
                <input type="number" id="semester" name="semester" required min="1" max="14">

                <label for="telefono">Teléfono:</label>
                <input type="tel" id="phoneNumber" name="phoneNumber" required>

                <label for="genero">Género:</label>
                <select id="gender" name="gender" required>
                    <option value="">Seleccione una opción</option>
                    <option value="masculino">Masculino</option>
                    <option value="femenino">Femenino</option>
                    <option value="otro">Otro</option>
                </select>

                <label for="fecha_nacimiento">Fecha de Nacimiento:</label>
                <input type="date" id="dateOfBirth" name="dateOfBirth" required>

                <label for="usuario">Usuario:</label>
                <input type="text" id="user" name="user" required>

                
                <label for="contrasena">Contraseña:</label>
                <input type="password" id="password" name="password" required>

                <button type="submit">Continuar</button>
            </form>
        </div>
    </div>
</body>

</html>