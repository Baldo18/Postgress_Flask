from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from connection import db_session, init_db, engine
from models import Empleado, Puesto, Database
import os

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PROFILE_PICTURES_FOLDER'] = 'static/archivos'
app.config['ALLOWED_IMAGE_TYPES'] = ['png', 'jpg', 'jpeg', 'JPEG', 'JPG']
app.config['SECRET_KEY'] = 'dmo5S4DxuD^9IWK1k33o7Xg88J&D8fq!'

os.makedirs(app.config['PROFILE_PICTURES_FOLDER'], exist_ok=True)
Database.metadata.create_all(engine)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_TYPES']

def lista_archivos():
    return os.listdir(app.config['PROFILE_PICTURES_FOLDER'])

@app.before_request
def initialize():
    init_db()

@app.get('/')
def index():
    empleados = db_session.query(Empleado).all()
    puestos = db_session.query(Puesto).all() 
    return render_template('index.html', empleados=empleados, puestos=puestos)

@app.get('/agregar')
def agregar():
    puestos = db_session.query(Puesto).all()  # Obtener todos los puestos
    return render_template('agregar.html', puestos=puestos)

@app.post('/agregar')
def agregar_empleado():
    nombre = request.form['nombre'].upper()
    apellido_p = request.form['apellido_p'].upper()
    apellido_m = request.form['apellido_m'].upper()
    fecha_nacimiento = request.form['fecha_nacimiento']
    puesto_id = request.form['puesto']  # ID del puesto seleccionado
    
    imagen_file = request.files['imagen']
    imagen_filename = None

    if imagen_file and allowed_file(imagen_file.filename):
        imagen_filename = secure_filename(imagen_file.filename)
        imagen_file.save(os.path.join(app.config['PROFILE_PICTURES_FOLDER'], imagen_filename))
    
    nuevo_empleado = Empleado(
        nombre=nombre,
        apellido_p=apellido_p,
        apellido_m=apellido_m,
        fecha_nacimiento=fecha_nacimiento,
        image=imagen_filename,
        puesto_id=puesto_id  # Relacionar el puesto
    )

    db_session.add(nuevo_empleado)
    db_session.commit()

    return redirect(url_for('index'))



@app.post('/eliminar/<int:empleado_id>')
def eliminar_empleado(empleado_id):
    # Buscar al empleado por ID
    empleado = db_session.query(Empleado).get(empleado_id)
    if empleado:
        # Eliminar la imagen asociada si existe
        if empleado.image:
            imagen_path = os.path.join(app.config['PROFILE_PICTURES_FOLDER'], empleado.image)
            if os.path.exists(imagen_path):
                os.remove(imagen_path)
        # Eliminar al empleado de la base de datos
        db_session.delete(empleado)
        db_session.commit()
    return redirect(url_for('index'))



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



@app.get('/editar/<int:empleado_id>')
def editar_empleado(empleado_id):
    empleado = db_session.query(Empleado).get(empleado_id)
    puestos = db_session.query(Puesto).all()
    return render_template('editar.html', empleado=empleado, puestos=puestos)

@app.post('/editar/<int:empleado_id>')
def actualizar_empleado(empleado_id):
    empleado = db_session.query(Empleado).get(empleado_id)
    
    if not empleado:
        return redirect(url_for('index'))  # Redirigir si no se encuentra el empleado
    
    empleado.nombre = request.form['nombre'].upper()
    empleado.apellido_p = request.form['apellido_p'].upper()
    empleado.apellido_m = request.form['apellido_m'].upper()
    empleado.fecha_nacimiento = request.form['fecha_nacimiento']
    empleado.puesto_id = request.form['puesto']
    
    imagen_file = request.files['imagen']
    
    if imagen_file and allowed_file(imagen_file.filename):
        # Eliminar la imagen anterior si existe
        if empleado.image:
            imagen_path = os.path.join(app.config['PROFILE_PICTURES_FOLDER'], empleado.image)
            if os.path.exists(imagen_path):
                os.remove(imagen_path)
        
        imagen_filename = secure_filename(imagen_file.filename)
        imagen_file.save(os.path.join(app.config['PROFILE_PICTURES_FOLDER'], imagen_filename))
        empleado.image = imagen_filename  # Actualizar la imagen
    
    db_session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
