import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al sistema
load_dotenv()

class Config:
    # --- Seguridad de Flask ---
    # Es vital para proteger formularios y sesiones de usuario
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-muy-dificil-de-adivinar'

    # --- Base de Datos (SQLAlchemy) ---
    # Busca la URL en el .env, si no la encuentra, crea una SQLite local por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mi_base_de_datos.db'
    
    # Desactiva una funcionalidad que consume memoria y no suele usarse
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Configuración de Google Gemini ---
    GOOGLE_API_KEY = os.environ.get('AIzaSyDg04SnsOstRd0K2gY_0vSBo5dMEH9gcvo')

    # --- Otras configuraciones (Opcional) ---
    # UPLOAD_FOLDER = 'static/uploads'g