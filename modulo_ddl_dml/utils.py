# instance/modulo_ddl_dml/utils.py
def validar_nombre(nombre):
    """Valida que el nombre no esté vacío."""
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")
