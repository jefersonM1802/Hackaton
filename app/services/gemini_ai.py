import google.generativeai as genai
import json
import os
from PIL import Image
from datetime import datetime

# INTENTA OBTENER LA KEY DESDE VARIABLES DE ENTORNO O CONFIG
# (Asegúrate de que tu compañero del run.py haya configurado esto)
API_KEY = os.environ.get("AIzaSyDg04SnsOstRd0K2gY_0vSBo5dMEH9gcvo")

if API_KEY:
    genai.configure(api_key=API_KEY)

class GeminiService:
    @staticmethod
    def analyze_image(image_path):
        """
        Analiza una imagen (boleta/factura) y retorna un diccionario
        compatible con la tabla 'IAClasificacion'.
        """
        if not API_KEY:
            print("❌ ERROR: No se encontró GEMINI_API_KEY")
            return GeminiService._get_fallback_data()

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            img = Image.open(image_path)
            
            # PROMPT DE INGENIERÍA:
            # Le damos instrucciones estrictas para que coincida con tu Base de Datos.
            prompt = """
            Actúa como un contador auditor experto. Analiza esta imagen.
            Extrae la información en un JSON ESTRICTO (sin markdown, solo texto plano).
            
            Usa estas claves exactas para coincidir con mi base de datos:
            {
                "tipo_clasificacion": "venta" (si es ingreso de dinero) o "gasto" (si es compra/pago),
                "categoria": Clasifica en una de estas: "Alimentos", "Transporte", "Servicios", "Inventario", "Personal", "Otros",
                "monto": (número decimal, ej: 150.50),
                "moneda": "PEN" o "USD" (por defecto PEN),
                "fecha_operacion": "YYYY-MM-DD" (si no hay fecha, usa la de hoy),
                "descripcion": Resumen breve de 5 a 10 palabras,
                "precision_modelo": Un número del 1 al 100 indicando qué tan legible es el documento
            }
            """
            
            # Llamada a la API
            response = model.generate_content([prompt, img])
            
            # Limpieza de la respuesta (Gemini suele responder con ```json ... ```)
            text_response = response.text.replace('```json', '').replace('```', '').strip()
            
            data = json.loads(text_response)
            
            # Validación rápida de fecha (para que no rompa la base de datos)
            try:
                datetime.strptime(data.get('fecha_operacion', ''), '%Y-%m-%d')
            except ValueError:
                data['fecha_operacion'] = datetime.now().strftime('%Y-%m-%d')
                
            return data

        except Exception as e:
            print(f"⚠️ Error al procesar con Gemini: {e}")
            return GeminiService._get_fallback_data()

    @staticmethod
    def _get_fallback_data():
        """
        Datos por defecto si falla la IA o no hay internet.
        Esto evita que la aplicación se caiga durante la demo.
        """
        return {
            "tipo_clasificacion": "gasto",
            "categoria": "General",
            "monto": 0.00,
            "moneda": "PEN",
            "fecha_operacion": datetime.now().strftime('%Y-%m-%d'),
            "descripcion": "Documento procesado manualmente (Error IA)",
            "precision_modelo": 0.0
        }