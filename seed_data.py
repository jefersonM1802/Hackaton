from run import app
from app.models import db, Usuario, IndicadorFinanciero, Riesgo, Documento
from werkzeug.security import generate_password_hash
from datetime import datetime, date

print("--- INICIANDO CARGA DE DATOS ---")

with app.app_context():
    # 1. ¿Hay algún usuario registrado?
    usuario = Usuario.query.first()
    
    if not usuario:
        print("No existe ningún usuario. Creando uno de prueba...")
        usuario = Usuario(
            nombres='Usuario', 
            apellidos='Prueba', 
            correo='admin@finansight.com',
            password_hash=generate_password_hash('123456'),
            dni='12345678', 
            negocio_nombre='Mi Negocio SAC',
            telefono='999888777'
        )
        db.session.add(usuario)
        db.session.commit()
        print(f"Usuario creado: {usuario.correo} (Pass: 123456)")
    else:
        print(f"Usando el usuario existente: {usuario.correo}")

    # 2. Borrar datos antiguos de este usuario (para no duplicar si lo corres 2 veces)
    IndicadorFinanciero.query.filter_by(id_usuario=usuario.id_usuario).delete()
    Riesgo.query.filter_by(id_usuario=usuario.id_usuario).delete()
    Documento.query.filter_by(id_usuario=usuario.id_usuario).delete()
    
    # 3. Insertar INDICADORES FINANCIEROS (Lo que se ve en las tarjetas de colores)
    kpi = IndicadorFinanciero(
        id_usuario=usuario.id_usuario,
        mes=11, 
        anio=2024,
        ingresos=25430.50,    # S/ 25k
        gastos=12100.00,      # S/ 12k
        utilidad=13330.50,    # La resta
        flujo=5000.00,
        razon_corriente=1.5,
        liquidez=1.2,
        margen=0.35,
        roe=0.15,
        ebitda=8000.00,
        fecha_registro=datetime.now()
    )
    db.session.add(kpi)

    # 4. Insertar RIESGO (El velocímetro)
    riesgo = Riesgo(
        id_usuario=usuario.id_usuario,
        score=780,            # Puntaje alto (verde)
        nivel='bajo',
        alerta_flujo=False,
        alerta_gastos_altos=False,
        alerta_estacionalidad=False,
        recomendaciones='Tu salud financiera es excelente. Mantén el control de gastos.',
        fecha_registro=datetime.now()
    )
    db.session.add(riesgo)

    # 5. Insertar DOCUMENTOS (La lista de abajo)
    docs = [
        Documento(id_usuario=usuario.id_usuario, tipo_documento='pdf', ruta_archivo='docs/factura_luz.pdf', estado='analizado', fecha_subida=datetime.now()),
        Documento(id_usuario=usuario.id_usuario, tipo_documento='foto', ruta_archivo='docs/boleta_agua.jpg', estado='pendiente', fecha_subida=datetime.now()),
        Documento(id_usuario=usuario.id_usuario, tipo_documento='foto', ruta_archivo='docs/ticket_compra.jpg', estado='rechazado', fecha_subida=datetime.now())
    ]
    db.session.add_all(docs)

    # Guardar todo
    db.session.commit()
    print("✅ ¡DATOS INSERTADOS EXITOSAMENTE!")
    print(f"👉 Inicia sesión con: {usuario.correo}")