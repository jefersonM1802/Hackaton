class Usuario(db.Model):
    __tablename__ = "usuarios"

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
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

class Documento(db.Model):
    __tablename__ = "documentos"

    id_documento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    tipo_documento = db.Column(db.Enum("foto", "pdf"))
    ruta_archivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum("pendiente", "analizado", "rechazado"))
    fecha_subida = db.Column(db.DateTime, default=db.func.now())

class IAClasificacion(db.Model):
    __tablename__ = "ia_clasificacion"

    id_clasificacion = db.Column(db.Integer, primary_key=True)
    id_documento = db.Column(db.Integer, db.ForeignKey("documentos.id_documento"))
    tipo_clasificacion = db.Column(db.Enum("venta", "gasto"), nullable=False)
    monto = db.Column(db.Numeric(10,2))
    fecha_operacion = db.Column(db.Date)
    descripcion = db.Column(db.String(255))
    precision_modelo = db.Column(db.Numeric(5,2))
    confirmado = db.Column(db.Boolean, default=False)
    fecha_analisis = db.Column(db.DateTime, default=db.func.now())

class Comprobante(db.Model):
    __tablename__ = "comprobantes"

    id_comprobante = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    numero_comprobante = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.Enum("boleta", "factura"), nullable=False)
    ruc_emisor = db.Column(db.String(20))
    fecha_emision = db.Column(db.Date)
    monto = db.Column(db.Numeric(10,2))
    estado_validacion = db.Column(db.Enum("valido","anulado","falso","duplicado","no_encontrado"))
    fecha_consulta = db.Column(db.DateTime, default=db.func.now())
class IndicadorFinanciero(db.Model):
    __tablename__ = "indicadores_financieros"

    id_indicador = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    mes = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    ingresos = db.Column(db.Numeric(12,2))
    gastos = db.Column(db.Numeric(12,2))
    utilidad = db.Column(db.Numeric(12,2))
    flujo = db.Column(db.Numeric(12,2))
    razon_corriente = db.Column(db.Numeric(10,2))
    liquidez = db.Column(db.Numeric(10,2))
    margen = db.Column(db.Numeric(10,2))
    roe = db.Column(db.Numeric(10,2))
    ebitda = db.Column(db.Numeric(12,2))
    fecha_registro = db.Column(db.DateTime, default=db.func.now())
class Riesgo(db.Model):
    __tablename__ = "riesgos"

    id_riesgo = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    score = db.Column(db.Integer)
    nivel = db.Column(db.Enum("bajo","medio","alto"))
    alerta_flujo = db.Column(db.Boolean)
    alerta_gastos_altos = db.Column(db.Boolean)
    alerta_estacionalidad = db.Column(db.Boolean)
    recomendaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=db.func.now())
class Proyeccion(db.Model):
    __tablename__ = "proyecciones"

    id_proyeccion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    escenario = db.Column(db.Enum("optimista","realista","critico"))
    ingresos_proyectados = db.Column(db.Numeric(12,2))
    gastos_proyectados = db.Column(db.Numeric(12,2))
    utilidad_proyectada = db.Column(db.Numeric(12,2))
    periodo_meses = db.Column(db.Integer)
    fecha_generacion = db.Column(db.DateTime, default=db.func.now())
class Reporte(db.Model):
    __tablename__ = "reportes"

    id_reporte = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    titulo = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    ruta_archivo = db.Column(db.String(255))
    fecha_generacion = db.Column(db.DateTime, default=db.func.now())
class BlockchainHash(db.Model):
    __tablename__ = "blockchain_hash"

    id_hash = db.Column(db.Integer, primary_key=True)
    id_documento = db.Column(db.Integer, db.ForeignKey("documentos.id_documento"))
    hash_generado = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.now())
class Historial(db.Model):
    __tablename__ = "historial"

    id_historial = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    accion = db.Column(db.String(255))
    detalle = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=db.func.now())
