<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="../img/sares.jpeg" type="image/x-icon">
    <title>Registro</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #6ba1ff, #b3d1ff);
            margin: 0;
            padding: 0;
        }

        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }

        .form-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            text-align: center;
        }

        .form-container img {
            max-width: 50px;
            margin: 10px;
        }

        .form-container h1 {
            font-size: 1.5em;
            margin-bottom: 20px;
        }

        .form-container input[type="text"],
        .form-container input[type="password"],
        .form-container select,
        .form-container button {
            width: calc(100% - 40px);
            padding: 10px;
            margin: 10px 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 1em;
        }

        .form-container button {
            background: #2c3e50;
            color: white;
            cursor: pointer;
        }

        .form-container button:hover {
            background: #34495e;
        }

        .logos {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .logos img {
            margin: 0 10px;
        }

        .logos img:last-child {
            margin-left: 30px;
        }

        .footer {
            margin-top: 20px;
            font-size: 0.8em;
            color: #777;
        }

        img {
            width: 10%;
            height: 10%;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="form-container">
            <div class="logos">
                <img src="../img/sep.png" alt="SEP Logo">
                <img src="../img/tecnm.jpg" alt="TECNM logo">
                <img src="../img/tec.png" alt="ITL logo">
                <img src="../img/sares.jpeg" alt="SARES_logo">
            </div>
            <h1>¡SaresTL, Construyendo un acceso seguro!</h1>
            <img src="../img/person-circle.svg" alt="User Icon">
            <form action="../php/procesar.php" method="POST">
                <!--Hidden-->
                <div>
                    <input type="hidden" id="formulario" name="formulario" value="userType">
                </div>
                <label for="user-type">Tipo Usuario:</label>
                <select id="user_type" name="user_type">
                    <option value="" disabled selected>Seleccione una opción</option>
                    <option value="1">Estudiante</option>
                    <option value="2">Docente</option>
                    <option value="3">Administrador</option>
                    <option value="4">Administrativo</option>
                    <option value="5">Guardia</option>
                    <option value="6">Intendente</option>
                </select>
                <button type="submit">Continuar</button>
            </form>
        </div>
    </div>
</body>

</html>