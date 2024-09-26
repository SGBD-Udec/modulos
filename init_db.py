from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.create_all()  # Esto debería crear las tablas
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al inicializar la base de datos: {e}")
