class Rol:
    def __init__(self, nombre, descripcion, permisos=None):
        """
        Inicializa un rol con un nombre, descripción y una lista de permisos.
        :param nombre: Nombre del rol (ejemplo: "Administrador").
        :param descripcion: Breve descripción del rol.
        :param permisos: Lista de permisos asociados al rol.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.permisos = permisos or []

    def agregar_permiso(self, permiso):
        """Agrega un permiso al rol."""
        if permiso not in self.permisos:
            self.permisos.append(permiso)

    def eliminar_permiso(self, permiso):
        """Elimina un permiso del rol."""
        if permiso in self.permisos:
            self.permisos.remove(permiso)

    def tiene_permiso(self, permiso):
        """Verifica si el rol tiene un permiso específico."""
        return permiso in self.permisos
