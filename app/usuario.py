import hashlib


class Usuario:
    def __init__(self, username, password_hash, rol):
        """
        Inicializa un usuario con nombre, contraseña cifrada y un rol.
        :param username: Nombre de usuario.
        :param password_hash: Contraseña cifrada (SHA-256).
        :param rol: Nombre del rol asociado al usuario.
        """
        self.username = username
        self.password_hash = password_hash
        self.rol = rol

    @staticmethod
    def hash_password(password):
        """Cifra la contraseña usando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verificar_password(password, password_hash):
        """Verifica si una contraseña coincide con la contraseña almacenada."""
        return Usuario.hash_password(password) == password_hash
