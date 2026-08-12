from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///personas.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Persona(Base):  
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)
# no sale esta vaina
class animal(Base):  
    __tablename__ = "animales"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)
#samuel ayudame 
Base.metadata.create_all(engine)

def interpretar_texto(texto):
    palabras = texto.lower().split()
    if palabras[0] == "agrega" and palabras[1] == "persona":  # <- espacios alrededor de and
        nombre = palabras[2]
        edad = int(palabras[3])
        nueva = Persona(nombre=nombre, edad=edad)
        session.add(nueva)
        session.commit()
        return f"Persona '{nombre}' agregada con edad {edad}"

    elif texto == "muestra todas las personas":
        personas = session.query(Persona).all()
        if personas:
            return "\n".join([f"{p.id}. {p.nombre} - {p.edad} años" for p in personas])  # <- espacio antes de for
        else:
            return "No hay personas registradas."
    elif texto.startswith("borra persona"):
        nombre = palabras[2]
        persona = session.query(Persona).filter_by(nombre=nombre).first()
        if persona:
            session.delete(persona)
            session.commit()
            return f"Persona '{nombre}' eliminada."
        else:
            return f"No se encontró la persona '{nombre}'."
    else:
        return "Instrucción no reconocida."

if __name__ == "__main__":
    print("=== Sistema Text-to-SQL Básico ===")
    print("Ejemplos:")
    print("- agrega persona Juan 25")
    print("- muestra todas las personas")
    print("- borra persona Juan")
    print("- salir\n")
    while True:
        comando = input("Escribe tu instrucción: ")
        if comando.lower() == "salir":
            break
        resultado = interpretar_texto(comando)  # <- procesa dentro del bucle
        print(resultado)