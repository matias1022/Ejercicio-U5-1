from datetime import datetime
from flask import Flask, redirect, request, render_template, flash,session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario,Viaje, Movil


@app.route('/')
def inicio():
	return render_template('inicio.html')


'''REGISTRO DE USUARIO'''

@app.route('/registro_usuario', methods= ['GET','POST'])
def registro_usuario():
    if request.method=='POST':
        if not request.form['DNI'] or not request.form['password']:
            return render_template('error.html', error="Los datos ingresados no son correctos...")
        else:
            usuario_actual = Usuario.query.filter_by(DNI = request.form['DNI']).first()
            if usuario_actual is not None:
                return render_template('error.html', error="ERROR: USUARIO CON DNI EXISTENTE")
            else:
                clave= request.form['password']
                Clave=hashlib.md5(bytes(clave, encoding='utf-8'))
                nuevo_usuario = Usuario(DNI=request.form['DNI'],nombre=request.form['nombre'], clave=Clave.hexdigest(), tipo=request.form['tipo'])
                db.session.add(nuevo_usuario)
                db.session.commit()
                return render_template('error.html', error="Usuario Registrado con exito...")
    return render_template('registro.html')

'''INICIAR SESION'''

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        if  not request.form['DNI'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            usuario_actual = Usuario.query.filter_by(DNI = request.form['DNI']).first()
            if usuario_actual is None:
                return render_template('error.html', error="El DNI no está registrado")
            else:
                verif=request.form['password']
                verificacion = hashlib.md5(bytes(verif, encoding='utf-8'))
                if verificacion.hexdigest() ==usuario_actual.clave:
                    if usuario_actual.tipo == 'cli':
                        return redirect(url_for('cliente', cliente_dni = usuario_actual.DNI))
                    elif usuario_actual.tipo == 'op':
                        return redirect(url_for('operador',operador_dni=usuario_actual.DNI))
                    else: return render_template('error.html', error="El tipo no es Valido")
                else:
                    return render_template('error.html', error="La contraseña no es válida")
    else:
        return render_template('login.html')


'''FUNCIONALIDADES CLIENTE'''

@app.route('/cliente/<cliente_dni>',methods=['GET','POST'])
def cliente(cliente_dni):
    usuario_actual = Usuario.query.filter_by(DNI = cliente_dni).first()
    return render_template('vistaCliente.html',usuario=usuario_actual)

@app.route('/cliente/<cliente_dni>/solicitarMovil/', methods = ['POST', 'GET'])
def solicitarMovil(cliente_dni):
    usuario_actual = Usuario.query.filter_by(DNI = cliente_dni).first()
    if request.method == 'POST':
            listadeviajes = Viaje.query.all()
            id = int(len(listadeviajes)) + 1
            fecha1=datetime.now()
            fecha = datetime.strftime(fecha1, '%Y-%m-%d %H:%M:%S') 
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            importe = 0 # sin calcular
            origen = request.form['origen']
            destino = request.form['destino']
            numeromovil = 0
            demora = 0
            duracion = 0
            viaje = Viaje(IDViaje = id, origen = origen, destino = destino, fecha = fecha, demora = demora, duracion = duracion, importe = importe, DNICliente = cliente_dni, numMovil = numeromovil)
            db.session.add(viaje)
            db.session.commit()
            usuario_actual = Usuario.query.filter_by(DNI = cliente_dni).first()
            return render_template('alerta_cli.html', error='Se ha solicitado el movil de forma correcta', usuario=usuario_actual)
    return render_template('solicitarMovil.html',usuario=usuario_actual)

@app.route('/cliente/<cliente_dni>/consultar_movil/', methods = ['POST', 'GET'])
def consultar_movil(cliente_dni):
        usuario_actual = Usuario.query.filter_by(DNI = cliente_dni).first()
        lista = Viaje.query.filter_by(importe = 0).all()
        listaMoviles = Movil.query.all()
        listaViajes=[]
        for viaje in lista:
            if viaje.duracion==0:
                listaViajes.append(viaje)
        longitud=len(listaViajes)
        return render_template('consultar_movil.html', usuario=usuario_actual,viajes=listaViajes,moviles=listaMoviles,len=longitud)





'''FUNCIONALIDADES OPERADOR'''

@app.route('/operador/<operador_dni>')
def operador(operador_dni):
    usuario_actual = Usuario.query.filter_by(DNI = operador_dni).first()
    return render_template('vistaOperador.html',usuario=usuario_actual)

@app.route('/operador/<operador_dni>/asigno', methods = ['POST', 'GET'])
def asigno(operador_dni):
        usuario_actual = Usuario.query.filter_by(DNI = operador_dni).first()
        listadeviajes = Viaje.query.filter_by(numMovil = 0).all()
        longitud=len(listadeviajes)
        return render_template('asignar_movil.html', usuario=usuario_actual,viajes = listadeviajes,len=longitud)

@app.route('/operador/<operador_dni>/asigno/<viajeID>/elegirMovil', methods = ['POST', 'GET'])
def elegirMovil(operador_dni,viajeID):
    usuario_actual = Usuario.query.filter_by(DNI = operador_dni).first()
    viaje_actual= Viaje.query.filter_by(IDViaje=int(viajeID)).first()
    lista=Movil.query.all()
    listademoviles=[]
    for movil in lista:
        if movil.viajeBool==0:
            listademoviles.append(movil)
    longitud=len(listademoviles)
    if request.method == 'POST':
        num=int(request.form['MovilNum'])
        movil_actual =Movil.query.filter_by(numero = request.form['MovilNum']).first()
        movil_actual.viajeBool = int(viajeID)
        demora=int(request.form['espera'])
        viaje_actual.numMovil=num
        viaje_actual.demora=demora
        db.session.commit()
        return render_template('alerta_op.html', error='MOVIL ASIGNADO',usuario=usuario_actual)
    else:
        
        return render_template('elegirMovil.html',moviles=listademoviles,usuario=usuario_actual,viaje=viaje_actual,len=longitud)

@app.route('/operador/<operador_dni>/finalizar_viaje', methods = ['POST', 'GET'])
def finalizar_viaje(operador_dni):
    usuario_actual = Usuario.query.filter_by(DNI = operador_dni).first()
    if request.method == 'POST':
        viaje = Viaje.query.filter_by(IDViaje = int(request.form['finalizar'])).first()
        duracion=int(request.form['duracion'])
        movil = Movil.query.filter_by(numero = str(viaje.numMovil)).first()
        movil.viajeBool = int(0)
        importe=100.0+(duracion*5)
        if viaje.demora>15:
            importe+=importe*0.10
        viaje.duracion=duracion
        viaje.importe=importe
        db.session.commit()
        return render_template ('alerta_op.html',usuario=usuario_actual ,error='Viaje Finalizado',aviso=('Importe final:{}'.format(importe)))
    else:
        listaViajes = Viaje.query.filter_by(duracion = 0).all()
        listaDef=[]
        print(listaViajes)
        for viaje in listaViajes:
             if viaje.numMovil != 0:
                     listaDef.append(viaje)
        longitud=len(listaDef)
        return render_template('finalizar_viaje.html',usuario=usuario_actual,viajes=listaDef,len=longitud)

@app.route('/operador/<operador_dni>/consultar_viaje_movil', methods = ['POST', 'GET'])
def consultar_viaje_movil(operador_dni):
    usuario_actual = Usuario.query.filter_by(DNI = operador_dni).first()
    if request.method == 'POST':
        impTotal=0
        movilNum=int(request.form['ElegirMovil'])
        fecha=request.form['fecha_elegir']
        listademoviles = Movil.query.all()
        listaViajes = Viaje.query.all()
        listaViajesFinalizados=[]
        for viaje in listaViajes:
            if viaje.duracion>0:
                listaViajesFinalizados.append(viaje)
        listaViajesDeMovil=[]
        for viaje in listaViajesFinalizados:
            if int(viaje.numMovil)==movilNum:
                fechaSinHORA=datetime.strftime(viaje.fecha, '%Y-%m-%d')
                if fechaSinHORA==fecha:
                     impTotal=impTotal+viaje.importe
                     listaViajesDeMovil.append(viaje)
        longitud=len(listaViajesDeMovil)
        return render_template('consultar_viaje2.html',usuario=usuario_actual,viajes=listaViajesDeMovil,importe=impTotal,len=longitud )

    else:
          listademoviles = Movil.query.all()
          return render_template('consultar_viaje.html',usuario=usuario_actual,moviles=listademoviles)
           
if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
