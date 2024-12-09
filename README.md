# SE_P3_InjuryTracker

_El sistema experto InjuryTracker está diseñado para identificar posibles lesiones deportivas basadas en síntomas localizados en diferentes partes del cuerpo. Utiliza una base de datos relacional SQLite para almacenar las preguntas, diagnósticos y relaciones entre ellos. Este sistema guía al usuario a través de un cuestionario estructurado y brinda un diagnóstico probable con información sobre causas y tratamiento._

## Indicaciones 📋
* Inicio de Sesión -> Roles de usuario: Acceso al sistema para identificar lesiones. Usuario: 1 , Contraseña: 1
* Selección de Parte del Cuerpo ->El usuario selecciona el área donde presenta molestias. Cada parte está asociada a un conjunto de preguntas específicas.
* Cuestionario -> Serie de preguntas cerradas con respuestas "Sí" o "No".
* Navegación a través de un árbol de decisiones -> Respuesta "Sí": Avanza a una pregunta relacionada. -> Respuesta "No": Alternativamente avanza o finaliza con un diagnóstico.
* Diagnóstico -> Resultado basado en las respuestas del usuario. Incluye: Nombre del diagnóstico, Causas, Tratamiento sugerido y Recomendación de consultar a un médico.
* Modo Administrador - > Permite agregar: Nuevas preguntas relacionadas a una parte del cuerpo. Diagnósticos con sus causas y tratamientos.
* Toda la informacion se va guardando en el archivo [sintomas.b]([https://github.com/AlejandraRG57/SE_P3_InjuryTracker/blob/main/sintomas.db]) ya le deje bastantes padecimientos precargados pero tu lo puedes seguir nutriendo!

## Expresiones de Gratitud 🎁
* Gracias a el profesor Mauricio Alejandro Cabrera Arellano por siempre impulsarnos a aprender cosas nuevas.

## Enlace🔗
YouTube:
* https://youtu.be/keC2-Iu5ODo
Prototipado:
* https://www.figma.com/design/kryzysTSWCpdbd00mD6G4e/InjuryTracker?node-id=0-1&t=M2LdpVr9B4QxSdbf-1&authuser=0 
