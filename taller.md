# 📚 Webgrafía y Recursos de Estudio

Para resolver el cuestionario y comprender a profundidad el proyecto, se recomienda consultar los siguientes recursos oficiales. Están divididos entre las tecnologías que **usa** el proyecto y los conceptos de seguridad que el proyecto **omite a propósito** (y que deberán investigar para la pregunta bonus).

---

## 🚀 1. FastAPI y Desarrollo Web (El motor del proyecto)
*Estos enlaces explican cómo el código logra mostrar páginas, manejar formularios y proteger rutas.*

*   **[Documentación Oficial: Plantillas (Jinja2)](https://fastapi.tiangolo.com/es/advanced/templates/)**
    *   *Para qué sirve:* Entender cómo FastAPI se conecta con Jinja2 para renderizar archivos `.html` usando `TemplateResponse`.
*   **[Documentación Oficial: Formularios (Form Fields)](https://fastapi.tiangolo.com/es/tutorial/request-forms/)**
    *   *Para qué sirve:* Comprender cómo `Annotated[str, Form()]` extrae los datos que el usuario escribe en el login (Pregunta 16).
*   **[Documentación Oficial: Dependencias](https://fastapi.tiangolo.com/es/tutorial/dependencies/)**
    *   *Para qué sirve:* El corazón de la protección de rutas. Explica qué es `Depends()` y cómo se inyecta el `UsuarioDep` antes de cargar una página (Pregunta 8).
*   **[Documentación Oficial: Respuestas Personalizadas y RedirectResponse](https://fastapi.tiangolo.com/es/advanced/custom-response/#redirectresponse)**
    *   *Para qué sirve:* Entender por qué usamos redirecciones después de un login exitoso.

---

## 🍪 2. Protocolo HTTP, Cookies y Sesiones (La memoria de la web)
*HTTP no tiene memoria por defecto. Estos recursos explican cómo "engañamos" al protocolo para recordar al usuario.*

*   **[MDN Web Docs: Cookies en HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Cookies)**
    *   *Para qué sirve:* La biblia de las cookies. Explica qué son, cómo viajan en los Headers, y qué significa `max_age` (Pregunta 9).
*   **[MDN Web Docs: Código de estado HTTP 303 (See Other)](https://developer.mozilla.org/es/docs/Web/HTTP/Status/303)**
    *   *Para qué sirve:* Resuelve la Pregunta 15. Explica por qué 303 es el código correcto tras enviar un formulario POST, obligando al navegador a hacer un GET seguro.
*   **[MDN Web Docs: Métodos de Petición HTTP (GET vs POST)](https://developer.mozilla.org/es/docs/Web/HTTP/Methods)**
    *   *Para qué sirve:* Entender la semántica de por qué las contraseñas NUNCA deben viajar por la URL (GET) sino en el cuerpo de la petición (POST).

---

## 🛡️ 3. Seguridad Informática (Lo que NO hace este proyecto)
*El proyecto guarda contraseñas en texto plano y usa sesiones simples. Estos recursos son **obligatorios** para responder las preguntas de seguridad y el "Bonus" de pensamiento crítico.*

*   **[OWASP: Guía de Almacenamiento de Contraseñas (Password Storage Cheat Sheet)](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)**
    *   *Para qué sirve:* Responde a la Pregunta 13. Explica por qué usar hashes (como bcrypt o Argon2) y "salts" es obligatorio en la vida real.
*   **[OWASP: Guía de Gestión de Sesiones (Session Management Cheat Sheet)](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)**
    *   *Para qué sirve:* Responde a la Pregunta 14. Explica cómo prevenir el *Session Hijacking*, la fijación de sesiones y por qué los tokens deben ser fuertes.
*   **[JWT.io: Introducción a los JSON Web Tokens](https://jwt.io/introduction)**
    *   *Para qué sirve:* Responde a la Pregunta 12. Explica qué es un JWT, sus tres partes y por qué las APIs modernas prefieren JWTs sobre sesiones con cookies y bases de datos.
*   **[Auth0: ¿Qué es OAuth 2.0?](https://auth0.com/intro-to-iam/what-is-oauth-2)**
    *   *Para qué sirve:* Responde a la Pregunta 12. Permite entender cómo funciona "Iniciar sesión con Google/GitHub" y por qué es un estándar de la industria.

---

## ☁️ 4. Despliegue y Serverless (Vercel)
*Por qué el proyecto se comporta distinto en la nube que en tu computadora.*

*   **[Vercel Docs: Python Runtime y Serverless Functions](https://vercel.com/docs/functions/runtimes/python)**
    *   *Para qué sirve:* Entender cómo Vercel empaqueta un proyecto de Python.
*   **[Artículo: ¿Qué es un "Cold Start" en Serverless?](https://www.serverless.com/blog/cold-start-latency)** *(Nota: puedes buscar "What is a serverless cold start" en YouTube o Medium)*
    *   *Para qué sirve:* Responde a la Pregunta 11. Explica por qué las funciones en la nube se "duermen" y por qué el archivo `sesiones.json` en memoria se pierde cuando esto ocurre.

---

### 💡 Consejo para el estudiante:
> No intentes memorizar todo. Usa esta webgrafía como un **mapa**. Si al leer el código de `seguridad.py` no entiendes qué hace `request.cookies.get()`, ve a la sección de **MDN Web Docs**. Si al leer el `GUIA_PROFESOR.md` ves que habla de "Hashes", ve a la sección de **OWASP**. ¡La habilidad de buscar en la documentación oficial es la más importante de un desarrollador!
