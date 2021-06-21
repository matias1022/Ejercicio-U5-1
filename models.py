from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Usuario(db.Model):
    DNI=db.Column(db.Integer, unique=True, primary_key=True)
    nombre=db.Column(db.String(120), nullable=False)
    clave=db.Column(db.String(100), nullable=False)
    tipo=db.Column(db.String(90), nullable=False)
    viaje=db.relationship('Viaje',backref='usuario', cascade="all, delete-orphan", lazy='dynamic')

'''class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    usuario_dni=db.Column(db.Integer, db.ForeignKey('usuario.DNI')) '''
class Viaje(db.Model):
    IDViaje = db.Column(db.Integer,primary_key=True)
    origen = db.Column(db.String(80), nullable=False)
    destino = db.Column(db.String(80), nullable=False)
    fecha = db.Column(db.DateTime)
    demora = db.Column(db.Integer)
    duracion = db.Column(db.Integer)
    importe = db.Column(db.Float)
    DNICliente = db.Column(db.String(10),db.ForeignKey('usuario.DNI'))
    numMovil = db.Column(db.Integer,db.ForeignKey('movil.numero'), nullable = False) 
    Movil = db.relationship('Movil')
    
class Movil(db.Model):
    numero = db.Column(db.Integer,primary_key=True)
    patente = db.Column(db.String(9), unique=True, nullable=False)
    marca = db.Column(db.String(90), nullable=False)
    viaje = db.relationship('Viaje',backref='movil',cascade="all, delete-orphan",lazy='dynamic')
    viajeBool = db.Column(db.Integer)