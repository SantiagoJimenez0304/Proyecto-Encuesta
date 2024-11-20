import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.usuario import Usuario  

def test_inicializacion_usuario():
    """
    Prueba la inicialización de un usuario.
    """
    username = "test_user"
    password_hash = Usuario.hash_password("secure_password")
    rol = "Administrador"

    usuario = Usuario(username, password_hash, rol)

    assert usuario.username == username
    assert usuario.password_hash == password_hash
    assert usuario.rol == rol


def test_hash_password():
    """
    Prueba el método hash_password para cifrar una contraseña.
    """
    password = "secure_password"
    hashed = Usuario.hash_password(password)

    # Verificar que el hash sea de tipo str
    assert isinstance(hashed, str)

    # Asegurar que dos contraseñas iguales generen el mismo hash
    assert hashed == Usuario.hash_password(password)

    # Asegurar que hashes diferentes no coincidan
    assert hashed != Usuario.hash_password("different_password")


def test_verificar_password():
    """
    Prueba el método verificar_password para comparar contraseñas.
    """
    password = "secure_password"
    password_hash = Usuario.hash_password(password)

    # Verificar contraseñas correctas
    assert Usuario.verificar_password(password, password_hash)

    # Verificar contraseñas incorrectas
    assert not Usuario.verificar_password("wrong_password", password_hash)


def test_verificar_password_empty():
    """
    Prueba el método verificar_password con contraseñas vacías.
    """
    empty_password = ""
    empty_hash = Usuario.hash_password(empty_password)

    # Verificar contraseñas vacías coinciden con su hash
    assert Usuario.verificar_password(empty_password, empty_hash)

    # Verificar contraseñas incorrectas no coinciden
    assert not Usuario.verificar_password("not_empty", empty_hash)
