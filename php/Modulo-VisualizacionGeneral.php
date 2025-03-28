<?php
require_once 'procesar.php';
$ejecutar = new Modulo_VisualizacionGeneral();
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizacion General</title>
    <link href="../img/sares.jpeg" rel="icon">
    <!-- Styles -->
    <link rel="stylesheet" href="../css/Modulo-VisualizacionGeneral.css">

    <style>
        body {
            background-color:
                <?php $ejecutar->interface_color(); ?>
            ;
        }

        .menu-general,
        .contenidoBusqueda {
            background-color:
                <?php $ejecutar->interface_color(); ?>
            ;
            color:
                <?php $ejecutar->letter_color(); ?>
            ;
            font-family:
                <?php $ejecutar->font(); ?>
            ;
            font-size:
                <?php $ejecutar->font_size(); ?>
                px;
            margin-bottom: -2%;
        }
    </style>

    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/2.0.5/css/dataTables.bootstrap5.css" rel="stylesheet">
    <script defer src="https://code.jquery.com/jquery-3.7.1.js"></script>
    <script defer
        src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    <script defer src="https://cdn.datatables.net/2.0.5/js/dataTables.js"></script>
    <script defer src="https://cdn.datatables.net/2.0.5/js/dataTables.bootstrap5.js"></script>

    <script defer src="../js/Modulo-VisualizacionGeneral.js"></script>
    <script>
        function toggleSidebar() {
            var sidebar = document.getElementById('sideMenu');
            sidebar.classList.toggle('show');

            var menu = document.querySelector('.menu-general');
            menu.classList.toggle('menu-show');

            var menu = document.querySelector('.contenidoBusqueda');
            menu.classList.toggle('contenidoBusqueda-show');

            var menu = document.querySelector('.autorImg');
            menu.classList.toggle('autorImg-show');
        }

        function closeSidebar() {
            var sidebar = document.getElementById('sideMenu');
            sidebar.classList.remove('show');

            var menu = document.querySelector('.menu-general');
            menu.classList.remove('menu-show');

            var menu = document.querySelector('.contenidoBusqueda');
            menu.classList.remove('contenidoBusqueda-show');

            var menu = document.querySelector('.autorImg');
            menu.classList.remove('autorImg-show');
        }
        $(document).ready(function () {
            $('#VisualizacionGeneral').DataTable();
        });        
    </script>
    

</head>

<body>
    <div class="menu-general">
        <nav id="menu1" class="menu1">
            <!-- Contenido del menú 1 -->
            <img src="../img/sep.png" alt="Picture" class="Image">
            <img src="../img/tecnm.jpg" alt="Picture3" class="Image">
            <img src="../img/tec.png" alt="Picture2" class="Image1">
            <img src="<?php $ejecutar->photo(); ?>" alt="Perfil" class="Avatar-Perfil">
            <img src="../img/menu.png" id="show-sideMebu-btn" class="Menu-Icono" alt="IconoMenu"
                onclick="toggleSidebar()">
        </nav>


        <div id="sideMenu" class="sideMenu">
            <a class="close-btn" onclick="closeSidebar()">&times;</a>
            <img src="../img/sares.jpeg" alt="Imagen" class="sideLogotipo">
            <nav>
                <!-- Contenido del Menu -->
                <?php
                $ejecutar->menu_content();
                ?>
            </nav>
        </div>
    </div>
    <div class="contenidoBusqueda">
        <h2 class="textoActualizar">Visualización General</h2>
        <h3 class="textoAdministrador">Administrador de sistema</h3>
        <table id="VisualizacionGeneral" class="table table-striped" style="width:100%">
            <thead>
                <tr>
                    <th>idRegistro</th>
                    <th>clave</th>
                    <th>Nombre</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Tipo</th>
                    <th>Usuario</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>

                <?php
                $ejecutar->show_table();
                ?>

            </tbody>
            <tfoot>
                <tr>
                    <th>idRegistro</th>
                    <th>clave</th>
                    <th>Nombre</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Tipo</th>
                    <th>Usuario</th>
                    <th>Acciones</th>
                </tr>
            </tfoot>
        </table>


        <div class="position-absolute w-100 top translate" id="modal">
            <form class="form-control w-50" id="respuesta" method="post">
                <h1 class="text-center">Editar registros</h1>
                <div class="form-control border-white">
                    <label for="">idRegistro :</label>
                    <input type="text" class="form-control w-75" id="idReg" name="idReg">
                </div>
                <div class="form-c border-white">
                    <label for="">clave :</label>
                    <input type="text" class="form-control w-25" name="clave" id="clave">
                </div>
                <div class="form-control border-white">
                    <label for="">Nombre :</label>
                    <input type="text" class="form-control w-75" id="nombre" name="nombre">
                </div>
                <div class="form-control border-white">
                    <label for="">Fecha :</label>
                    <input type="date" class="form-control" name="fecha" id="fecha">
                </div>
                <div class="form-control border-white">
                    <label for="">Hora :</label>
                    <input type="text" class="form-control w-50" name="hr" id="=hr">
                </div>
                <div class="form-control border-white">
                    <label for="">Tipo :</label>
                    <input type="text" class="form-control w-50" name="type" id="type">
                </div>
                <div class="form-control border-white">
                    <button class="btn btn-primary" name="eliminar" id="eliminarButton" type="submit">Eliminar
                        <?php
                        if (isset($_POST['eliminar'])) {
                            if (
                                strlen($_POST['idReg']) >= 1
                            ) {
                                $idReg = $_POST['idReg'];
                                $consulta = "DELETE FROM Registro where idRegistro = '$idReg'";
                                $resultado = mysqli_query($conexion, $consulta);
                                ?>
                                <script>
                                    history.replaceState(null, null, location.pathname);
                                    location.reload();
                                </script>
                                <?php
                            }
                        }
                        ?>

                    </button>
                    <button class="btn btn-primary" name="enviarFormulario" id="enviarFormulario" type="submit"
                        onclick="recarga()">Save!
                        <?php
                        if (isset($_POST['enviarFormulario'])) {
                            if (
                                strlen($_POST['idReg']) >= 1 &&
                                strlen($_POST['clave']) >= 1 &&
                                strlen($_POST['nombre']) >= 1 &&
                                strlen($_POST['fecha']) >= 1 &&
                                strlen($_POST['hr']) >= 1 &&
                                strlen($_POST['type']) >= 1
                            ) {
                                $idReg = trim($_POST['idReg']);
                                $clave = trim($_POST['clave']);
                                $nombre = trim($_POST['nombre']);
                                $fecha = trim($_POST['fecha']);
                                $hr = trim($_POST['hr']);
                                $type = trim($_POST['type']);
                                $consulta = "UPDATE Registro set tipoR='$type' where idRegistro= $idReg";
                                $resultado = mysqli_query($conexion, $consulta);
                                ?>
                                <script>
                                    history.replaceState(null, null, location.pathname);
                                    location.reload();
                                </script>
                                <?php
                            }
                        }
                        ?>

                    </button>
                </div>
            </form>
            <button class="position-absolute btn btn-danger close" id="cerrar">Close</button>
        </div>

        <!-- Incia botonesInferiores -->
        <div class="d-sm-flex align-items-center justify-content-between mb-4" id="botonesInferiores">
            <a href="ExportPDF.php" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                id="reporte_boton"><i class="fas fa-download fa-sm text-white-50"></i> Generar
                Reporte</a>

        </div>
        <!-- Termina botonesInferiores-->

    </div>
    <footer class="autorImg">
        <h4 class="autor">&copy; Sares TL, 2024</h4>
        <img src="../img/sares.jpeg" alt="Logo" class="Logotipo">
    </footer>
    <!-- JavaScript -->
    <script defer src="js/VisualizacionGeneral.js"></script>
</body>

</html>