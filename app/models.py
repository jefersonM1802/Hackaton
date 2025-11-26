from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin # <--- AGREGA ESTO ARRIBA
# Inicializamos la instancia (si ya la tienes en app.py, impórtala desde ahí)
db = SQLAlchemy()

# ========================================
# 1. MODELO: USUARIOS
# ========================================
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20))
    ruc = db.Column(db.String(20))
    negocio_nombre = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    imagen_perfil = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, server_default=func.now())

    # Relaciones (para acceder desde Python)
    documentos = db.relationship('Documento', backref='usuario', lazy=True)
    indicadores = db.relationship('IndicadorFinanciero', backref='usuario', lazy=True)
    riesgos = db.relationship('Riesgo', backref='usuario', lazy=True)
    proyecciones = db.relationship('Proyeccion', backref='usuario', lazy=True)
    comprobantes = db.relationship('Comprobante', backref='usuario', lazy=True)
    reportes = db.relationship('Reporte', backref='usuario', lazy=True)
    historial = db.relationship('Historial', backref='usuario', lazy=True)
    def get_id(self):
        return str(self.id_usuario)

# ========================================
# 2. MODELO: DOCUMENTOS
# ========================================
class Documento(db.Model):
    __tablename__ = 'documentos'

    id_documento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    
    # Enums se definen con las opciones permitidas
    tipo_documento = db.Column(db.Enum('foto', 'pdf', name='tipo_doc_enum'), default='foto')
    ruta_archivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'analizado', 'rechazado', name='estado_doc_enum'), default='pendiente')
    
    # 🔥🔥 NUEVO: Integridad
    hash_integridad = db.Column(db.Enum('pendiente', 'verificado', 'alterado', name='hash_int_enum'), default='pendiente')
    
    fecha_subida = db.Column(db.DateTime, server_default=func.now())

    # Relaciones
    clasificacion = db.relationship('IAClasificacion', backref='documento', uselist=False, lazy=True)
    blockchain_hash = db.relationship('BlockchainHash', backref='documento', uselist=False, lazy=True)

# ========================================
# 3. MODELO: IA CLASIFICACIÓN
# ========================================
class IAClasificacion(db.Model):
    __tablename__ = 'ia_clasificacion'

    id_clasificacion = db.Column(db.Integer, primary_key=True)
    id_documento = db.Column(db.Integer, db.ForeignKey('documentos.id_documento'), nullable=False)
    
    tipo_clasificacion = db.Column(db.Enum('venta', 'gasto', name='tipo_clas_enum'), nullable=False)
    
    # 🔥🔥 NUEVO: Categoría específica
    categoria = db.Column(db.String(50), default='General')
    
    monto = db.Column(db.Numeric(10, 2))
    
    # 🔥🔥 NUEVO: Moneda
    moneda = db.Column(db.String(5), default='PEN')
    
    fecha_operacion = db.Column(db.Date)
    descripcion = db.Column(db.String(255))
    precision_modelo = db.Column(db.Numeric(5, 2))
    confirmado = db.Column(db.Boolean, default=False)
    fecha_analisis = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 4. MODELO: BLOCKCHAIN HASH
# ========================================
class BlockchainHash(db.Model):
    __tablename__ = 'blockchain_hash'

    id_hash = db.Column(db.Integer, primary_key=True)
    id_documento = db.Column(db.Integer, db.ForeignKey('documentos.id_documento'), nullable=False)
    hash_generado = db.Column(db.String(255), nullable=False) # SHA-256
    fecha_registro = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 5. MODELO: INDICADORES FINANCIEROS
# ========================================
class IndicadorFinanciero(db.Model):
    __tablename__ = 'indicadores_financieros'

    id_indicador = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    ingresos = db.Column(db.Numeric(12, 2))
    gastos = db.Column(db.Numeric(12, 2))
    utilidad = db.Column(db.Numeric(12, 2))
    flujo = db.Column(db.Numeric(12, 2))
    razon_corriente = db.Column(db.Numeric(10, 2))
    liquidez = db.Column(db.Numeric(10, 2))
    margen = db.Column(db.Numeric(10, 2))
    roe = db.Column(db.Numeric(10, 2))
    ebitda = db.Column(db.Numeric(12, 2))
    fecha_registro = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 6. MODELO: RIESGOS CREDITICIOS
# ========================================
class Riesgo(db.Model):
    __tablename__ = 'riesgos'

    id_riesgo = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    score = db.Column(db.Integer)
    nivel = db.Column(db.Enum('bajo', 'medio', 'alto', name='nivel_riesgo_enum'))
    alerta_flujo = db.Column(db.Boolean)
    alerta_gastos_altos = db.Column(db.Boolean)
    alerta_estacionalidad = db.Column(db.Boolean)
    recomendaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 7. MODELO: PROYECCIONES
# ========================================
class Proyeccion(db.Model):
    __tablename__ = 'proyecciones'

    id_proyeccion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    escenario = db.Column(db.Enum('optimista', 'realista', 'critico', name='escenario_enum'))
    ingresos_proyectados = db.Column(db.Numeric(12, 2))
    gastos_proyectados = db.Column(db.Numeric(12, 2))
    utilidad_proyectada = db.Column(db.Numeric(12, 2))
    periodo_meses = db.Column(db.Integer)
    fecha_generacion = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 8. MODELO: COMPROBANTES ELECTRÓNICOS
# ========================================
class Comprobante(db.Model):
    __tablename__ = 'comprobantes'

    id_comprobante = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    numero_comprobante = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.Enum('boleta', 'factura', name='tipo_comp_enum'), nullable=False)
    ruc_emisor = db.Column(db.String(20))
    fecha_emision = db.Column(db.Date)
    monto = db.Column(db.Numeric(10, 2))
    estado_validacion = db.Column(db.Enum('valido', 'anulado', 'falso', 'duplicado', 'no_encontrado', name='estado_val_enum'))
    fecha_consulta = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 9. MODELO: REPORTES
# ========================================
class Reporte(db.Model):
    __tablename__ = 'reportes'

    id_reporte = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    titulo = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    ruta_archivo = db.Column(db.String(255))
    fecha_generacion = db.Column(db.DateTime, server_default=func.now())

# ========================================
# 10. MODELO: HISTORIAL
# ========================================
class Historial(db.Model):
    __tablename__ = 'historial'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    accion = db.Column(db.String(255))
    detalle = db.Column(db.Text)
    fecha = db.Column(db.DateTime, server_default=func.now())
