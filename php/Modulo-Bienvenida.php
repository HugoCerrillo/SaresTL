<?php
require_once 'procesar.php';
$ejecutar = new ModuloBienvenida();
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="../img/sares.jpeg" type="image/x-icon">
    <title>Bienvenida</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #6ba1ff, #b3d1ff);
            margin: 0;
            padding: 0;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            padding: 10px 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            position: relative;
        }

        .header .logos {
            display: flex;
            align-items: center;
        }

        .header .logos img {
            max-width: 50px;
            margin-right: 10px;
        }

        .header .user-profile {
            display: flex;
            align-items: center;
            cursor: pointer;
        }

        .header .user-profile img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            object-fit: cover;
        }

        .header .menu-icon {
            font-size: 24px;
        }

        /* Menú desplegable */
        .menu-dropdown {
            position: absolute;
            top: 100%;
            right: 20px;
            background: #3478b3; /* Fondo azul */
            color: white;
            width: 200px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            display: none;
            flex-direction: column;
            z-index: 1;
        }

        .menu-dropdown.open {
            display: flex;
        }

        .menu-dropdown ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .menu-dropdown ul li {
            padding: 10px;
            border-bottom: 1px solid #1f4a71;
            cursor: pointer;
        }

        .menu-dropdown ul li:hover {
            background: #295a83;
        }

        .menu-dropdown ul li:last-child {
            border: none;
        }

        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: calc(100vh - 60px);
            padding: 20px;
            text-align: center;
        }

        .welcome-text h1 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .welcome-text p {
            font-size: 1.2em;
            color: #34495e;
            margin: 0 0 15px;
        }

        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        .action-buttons button {
            background: #2c3e50;
            color: white;
            font-size: 1em;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .action-buttons button:hover {
            background: #34495e;
        }

        .info-cards {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            width: 100%;
        }

        .info-card {
            background: white;
            width: 250px;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: left;
            color: #34495e;
        }

        .info-card h3 {
            margin: 0 0 10px;
            font-size: 1.2em;
            color: #2c3e50;
        }

        .info-card p {
            font-size: 1em;
            margin: 0;
        }

        .footer {
            text-align: center;
            padding: 10px 20px;
            color: #777;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .header .logos img {
                max-width: 40px;
            }

            .header .user-profile img {
                width: 30px;
                height: 30px;
            }

            .welcome-text h1 {
                font-size: 2em;
            }

            .info-cards {
                flex-direction: column;
                gap: 20px;
            }

            .info-card {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <div class="header">
        <div class="logos">
            <img src="../img/sep.png" alt="Logo SEP">
            <img src="../img/tecnm.jpg" alt="TECNM Logo">
            <img src="../img/tec.png" alt="ITL Logo">
            <img src="../img/sares.jpeg" alt="SARES Logo">
        </div>
        <div class="user-profile" onclick="toggleMenu()">
            <img src="<?php $ejecutar->photo(); ?>" alt="Foto de Perfil">
            <span class="menu-icon"><img src="../img/list.svg" ></span>
        </div>
        <div class="menu-dropdown" id="menuDropdown">
            <ul>
                <!-- Contenido del Menu -->
                <?php
                $ejecutar->menu_content();
                ?>
            </ul>
        </div>
    </div>
    <div class="container">
        <div class="welcome-text">
            <h1>Bienvenido(a): <?php $ejecutar->name_user(); ?> </h1>
            <p>Eres un: <?php $ejecutar->type_user(); ?> en TECNM Campus León Campus 1</p>
            <p>Con rol en nuestro sistema de: <?php $ejecutar->type_user_system(); ?></p>
        </div>
        <div class="action-buttons">
            <button>Ver Perfil</button>
            <button>Configuraciones</button>
        </div>
        <div class="info-cards">
            <div class="info-card">
                <h3>Noticias</h3>
                <p>Actualiza tus conocimientos con las últimas noticias del campus y el sistema.</p>
            </div>
            <div class="info-card">
                <h3>Accesos Rápidos</h3>
                <p>Accede rápidamente a los recursos más utilizados en el sistema.</p>
            </div>
            <div class="info-card">
                <h3>Eventos</h3>
                <p>No te pierdas los próximos eventos y reuniones importantes.</p>
            </div>
        </div>
    </div>
    <div class="footer">© Sares TL, 2024</div>

    <script>
        function toggleMenu() {
            const menu = document.getElementById('menuDropdown');
            menu.classList.toggle('open');
        }
    </script>
</body>

</html>
