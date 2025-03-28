<html>

<head>
    <link rel="icon" href="img/icono.png" type="image/png" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <title>SaresTL</title>
    <style>
        body {
            background-color: #5C92FF;
            /*background: url("img/fondo.jpg") no-repeat center center fixed;*/
            background-size: cover;
            color: azure;
        }
    </style>
</head>

</html>

<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $formulario = $_POST['formulario'] ?? null ?? '';
    switch ($formulario) {
        case 'login':
            $user = $_POST['user'] ?? null ?? '';
            $password = $_POST['password'] ?? null ?? '';
            $login = new LoginModule($user, $password);
            break;
        case 'administratorType':
            $userType = "Administrador";
            $register = new RegistrationModule($_POST['name'], $_POST['email'], $_POST['department'], $_POST['phoneNumber'], $_POST['gender'], $_POST['dateOfBirth'], $_POST['user'], $_POST['password'], $userType);
            break;
        case 'userType':
            $userChoice = $_POST['user_type'] ?? null ?? '';
            $userType = new UserTypeModule($userChoice);
            break;
        default:        
            //new GenerateError('Error al procesar el formulario', '../php/Modulo-InicioSesion.php');
            break;
    }
}

class RegistrationModule
{
    private $name;
    private $email;
    private $department;
    private $phoneNumber;
    private $gender;
    private $dateOfBirth;
    private $user;
    private $password;

    private $userType;
    public function __construct($name, $email, $department, $phoneNumber, $gender, $dateOfBirth, $user, $password, $userType)
    {
        $this->name = $name ?? null ?? '';
        $this->email = $email ?? null ?? '';
        $this->department = $department ?? null ?? '';
        $this->phoneNumber = $phoneNumber ?? null ?? '';
        $this->gender = $gender ?? null ?? '';
        $this->dateOfBirth = $dateOfBirth ?? null ?? '';
        $this->user = $user ?? null ?? '';
        $this->password = $password ?? null ?? '';
        $this->userType = $userType ?? null ?? '';
        $this->register();
    }
    private function register()
    {
        try {
            // URL de la API Flask (cambia esta URL según corresponda)
            $url = "https://hugoc.pythonanywhere.com/api/register";

            //Los datos que enviaremos a la API
            $data = array(
                "name" => $this->name,
                "email" => $this->email,
                "department" => $this->department,
                "phoneNumber" => $this->phoneNumber,
                "gender" => $this->gender,
                "dateOfBirth" => $this->dateOfBirth,
                "user" => $this->user,
                "password" => $this->password,
                "userType" => $this->userType
            );

            // configurar los parametros para la soliucutd POST
            $options = array(
                'http' => array(
                    'method' => 'POST',
                    'header' => 'Content-Type: application/json',
                    'content' => json_encode($data)
                )
            );
            $context = stream_context_create($options);

            error_log(json_encode($data));

            // Hacer la solicitud a la API
            $result = @file_get_contents($url, false, $context);

            if ($result === FALSE) {
                $error = error_get_last(); // Captura el último error registrado
                echo "Error en la conexión con la API: " . $error['message']; // Imprime el mensaje del error
                return;
            }
                        
            // Decodifica la respuesta JSON de la API
            $response = json_decode($result, true);

            // Comprobar si la respuesta de la API indica que el registro fue exitoso
            if (isset($response['status']) && $response['status'] === "success") {
                new GenerateSuccess('Registro exitoso', '../php/Modulo-InicioSesion.php');
                return;
            } else {
                new GenerateError('Error en el registro', '../php/Modulo-RegistroAdministrador.php');
                return;
            }
        } catch (Exception $e) {
            new GenerateError('Error en la conexión con el servidor', '../php/Modulo-RegistroAdministrador.php');
            return;
        }
    }
}

class UserTypeModule
{
    private $userChoice;
    public function __construct($userChoice)
    {
        $this->userChoice = $userChoice;
        $this->show_page();

    }
    private function show_page()
    {
        switch ($this->userChoice) {
            case '1':
                header("Location: Modulo-RegistroEstudiante.php?");
                break;
            case '2':
                header("Location: Modulo-RegistroDocente.php?");
                break;
            case '3':
                header("Location: Modulo-RegistroAdministrador.php?");
                break;
            case '4':
                header("Location: Modulo-RegistroPersonalAdministrativo.php?");
                break;
            case '5':
                header("Location: Modulo-RegistroGuardia.php?");
                break;
            case '6':
                header("Location: Modulo-RegistroIntendencia.php?");
                break;
            default:
                // Manejo de caso de opción no válida
                header("Location: Modulo-TipoUsuario.php?");
                break;
        }
    }
}
class LoginModule
{
    private $user;
    private $password;
    public function __construct($user, $password)
    {
        $this->user = $user ?? null ?? '';
        $this->password = $password ?? null ?? '';
        $this->login();
    }

    private function login()
    {
        try {
            // URL de la API Flask (cambia esta URL según corresponda)
            $url = "https://hugoc.pythonanywhere.com/api/login";

            //Los datos que enviaremos a la API
            $data = array(
                "username" => $this->user,
                "password" => $this->password
            );

            // configurar los parametros para la soliucutd POST
            $options = array(
                'http' => array(
                    'method' => 'POST',
                    'header' => 'Content-Type: application/json',
                    'content' => json_encode($data)
                )
            );
            $context = stream_context_create($options);

            // Hacer la solicitud a la API
            $result = @file_get_contents($url, false, $context);

            // Verifica si la solicitud fue exitosa
            if ($result === FALSE) {
                new GenerateError('Credenciales incorrectas.', '../php/Modulo-InicioSesion.php');
                return;
            }

            // Decodifica la respuesta JSON de la API
            $response = json_decode($result, true);


            // Comprobar si la respuesta de la API indica que las credenciales son correctas
            if (isset($response['status']) && $response['status'] === "success") {
                $_SESSION['user'] = $this->user;
                new GenerateSuccess('Inicio de sesión exitoso', '../php/Modulo-Bienvenida.php');
                return;
            } else {
                new GenerateError('No se ha encontrado el usuario en el sistema', '../php/Modulo-InicioSesion.php');
                return;
            }
        } catch (Exception $e) {
            new GenerateError('Error en la conexión con el servidor', '../php/Modulo-InicioSesion.php');
            return;
        }


    }
}

class GenerateSuccess
{
    private $text;
    private $location;

    public function __construct($text, $location)
    {
        $this->text = $text;
        $this->location = $location;
        $this->generate_custom_success();
    }

    private function generate_custom_success()
    {
        echo ('<script>
            Swal.fire({
                title: "¡Éxito!",
                text: "' . $this->text . '",
                icon: "success",
                background: "#1C1766",  // Fondo personalizado 
                color: "#ffffff",       // Texto en color blanco
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Aceptar"
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "' . $this->location . '";
                }
            });
        </script>');
    }
}

class GenerateError
{
    private $text;
    private $location;
    public function __construct($text, $location)
    {
        $this->text = $text;
        $this->location = $location;
        $this->generate_custom_error();
    }
    private function generate_custom_error()
    {
        echo ('<script>
            Swal.fire({
                title: "¡Error!",
                text: "' . $this->text . '",
                icon: "error",
                background: "#1C1766",  // Fondo personalizado 
                color: "#ffffff",       // Texto en color blanco
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Aceptar"
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "' . $this->location . '";
                }
            });
        </script>');
    }
}
?>