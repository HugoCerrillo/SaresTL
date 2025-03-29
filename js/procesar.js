class GenerateSuccess {
    constructor(text, location) {
        this.text = text;
        this.location = location;
        this.generateCustomSuccess();
    }

    generateCustomSuccess() {
        Swal.fire({
            title: "¡Éxito!",
            text: this.text,
            icon: "success",
            background: "#1C1766",  // Fondo personalizado
            color: "#ffffff",       // Texto en color blanco
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Aceptar"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = this.location;
            }
        });
    }
}



class GenerateError {
    constructor(text, location) {
        this.text = text;
        this.location = location;
        this.generateCustomError();
    }

    generateCustomError() {
        Swal.fire({
            title: "¡Error!",
            text: this.text,
            icon: "error",
            background: "#1C1766",  // Fondo personalizado
            color: "#ffffff",       // Texto en color blanco
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Aceptar"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = this.location;
            }
        });
    }
}

function generateSuccess(text, location) {
    new GenerateSuccess(text, location);
}
function generateError(text, location) {
    new GenerateError(text, location);
}