<?php
if (session_status() == PHP_SESSION_ACTIVE) {
    session_destroy();
}
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="../img/sares.jpeg" type="image/x-icon">
    <title>Inicio de Sesión</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #6ba1ff, #b3d1ff);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .login-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            /* Ajustado para que sea más ancho */
            text-align: center;
        }

        .login-container img {
            max-width: 50px;
            margin: 10px;
        }

        .login-container .logos img:last-child {
            margin-left: 30px;
            /* Ajustado para alejar más el último logo */
        }

        .login-container h1 {
            font-size: 1.5em;
            margin-bottom: 20px;
        }

        .login-container input[type="text"],
        .login-container input[type="password"] {
            width: calc(100% - 20px);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .login-container button {
            background: #2c3e50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }

        .login-container button:hover {
            background: #34495e;
        }

        .login-container a {
            display: block;
            margin: 10px 0;
            color: #3498db;
            text-decoration: none;
        }

        .login-container a:hover {
            text-decoration: underline;
        }

        .footer {
            margin-top: 20px;
            font-size: 0.8em;
            color: #777;
        }
    </style>
</head>

<body>
    <div class="login-container">
        <div class="logos">
            <img src="../img/sep.png" alt="Logo 1">
            <img src="../img/tecnm.jpg" alt="Logo 2">
            <img src="../img/tec.png" alt="Logo 3">
            <img src="../img/sares.jpeg" alt="Logo 4">
        </div>
        <h1>¡SaresTL, Construyendo un acceso seguro!</h1>
        <form action="../php/procesar.php" method="post">
            <input type="text" name = "user" id="user" placeholder="Usuario" required>
            <input type="password" name = "password" id="password" placeholder="Contraseña" required>
            <!--Hidden-->
            <div>
                <input type="hidden" id="formulario" name="formulario" value="login">
            </div>
            <button type="submit">Iniciar Sesión</button>
        </form>

        
        <a href="../php/Modulo-TipoUsuario.php">Registrarse</a>
        <a href="#">Manual de usuario</a>
        <a href="../php/Modulo-OlvidarContrasena.php">¿Olvidó su contraseña?</a>
        <div class="footer">© Sares TL, 2024</div>
    </div>
</body>

</html>