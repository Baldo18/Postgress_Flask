from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from connection import Database

# Modelo Puesto
class Puesto(Database):
    __tablename__ = 'puestos'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # Clave primaria
    nombre_puesto = Column(String(100), nullable=False)  # Nombre del puesto

    empleados = relationship('Empleado', back_populates='puesto')

# Modelo Empleado
class Empleado(Database):
    __tablename__ = 'empleados'  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True)  # Clave primaria
    nombre = Column(String(100), nullable=False)  # Nombre del empleado
    apellido_p = Column(String(100), nullable=False)  # Apellido paterno
    apellido_m = Column(String(100), nullable=False)  # Apellido materno
    fecha_nacimiento = Column(Date(), nullable=False)  # Fecha de nacimiento
    image = Column(String(100))  # Imagen del empleado (opcional)

    # Clave foránea que referencia al id de la tabla puestos
    puesto_id = Column(Integer, ForeignKey('puestos.id'), nullable=False)

    # Relación con la tabla Puesto
    puesto = relationship('Puesto', back_populates='empleados')
