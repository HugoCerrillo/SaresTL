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