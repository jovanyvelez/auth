# Evaluación: Taller de Autenticación con FastAPI
## Javiera 11_3

> **Objetivo:** Verificar la comprensión del proyecto de autenticación implementado en el repositorio `auth`.
>
> **Repositorio:** https://github.com/jovanyvelez/auth
>
> **Tecnologías:** FastAPI + Jinja2 + Sesiones con Cookie

---

## 📐 Arquitectura y Estructura del Proyecto

**1.** ¿Cuál es la responsabilidad específica de cada archivo Python (`main.py`, `rutas.py`, `seguridad.py`, `usuarios.py`) y por qué se considera una buena práctica separarlos de esta manera?

**2.** ¿Qué significa "separación de responsabilidades" en el contexto de este proyecto y cómo se manifiesta en la estructura de archivos?

**3.** ¿Por qué el archivo `main.py` es tan breve (apenas 29 líneas) y qué indica esto sobre el diseño de la aplicación?

---

## 🔐 Mecanismo de Autenticación y Sesiones

**4.** Explica el concepto de "sesión" tal como se implementa en este proyecto. ¿Por qué HTTP necesita sesiones si cada petición es independiente?

**5.** ¿Qué es el token de sesión, cómo se genera específicamente en el código (`secrets.token_hex(16)`) y por qué es importante que sea aleatorio e impredecible?

**6.** Describe el flujo completo cuando un usuario ingresa credenciales válidas: desde el POST al `/login` hasta que se redirige a la página home (menciona los "PASOS" del diagrama).

**7.** ¿Qué diferencia hay entre las rutas públicas (`/login`, `/logout`) y las privadas (`/`, `/perfil`, `/objetos`)? ¿Por qué el login debe ser necesariamente público?

**8.** ¿Cómo funciona la dependencia `UsuarioDep` en FastAPI y qué hace exactamente la función `get_current_user` cuando se ejecuta en cada ruta protegida?

---

## 🍪 Cookies y Gestión de Estado

**9.** ¿Cuál es el propósito de la cookie `COOKIE_SESION` y qué parámetros se configuran cuando se establece (`max_age=VIDA_SESION_SEGUNDOS`)? ¿Qué pasaría si no se configurara `max_age`?

**10.** El proyecto guarda las sesiones en un archivo `sesiones.json` en disco. Explica el flujo de lectura y escritura de este archivo: ¿cuándo se lee, cuándo se escribe y qué sucede si el disco es de solo lectura (como en Vercel)?

**11.** Compara el comportamiento de las sesiones en desarrollo local vs. despliegue en Vercel. ¿Por qué en Vercel las sesiones "se pierden" cuando la función se enfría (cold start)?

**Curiosidad.**: Por qué se les llama cookies en el mundo de la informática a esos fragmentos de texto?

---

## 🛡️ Seguridad y Mejores Prácticas

**12.** El README advierte que este proyecto **deliberadamente no usa** OAuth2, JWT ni hashes de contraseña. Explica qué son estos tres conceptos y por qué NO se usan en este proyecto didáctico.

**13.** Las contraseñas en `usuarios.py` están en **texto plano** (`"password": "1234"`). ¿Qué riesgo de seguridad representa esto en producción y qué solución se usaría en un proyecto real?

**14.** ¿Qué es el "sesion hijacking" (secuestro de sesión) y qué medidas adicionales podrían implementarse para prevenirlo que este proyecto no incluye?

---

## 🌐 Flujo HTTP y Códigos de Estado

**15.** El código usa `status_code=303` en las redirecciones después del login y logout. ¿Por qué se usa específicamente 303 (See Other) en lugar de 302 (Found) o 301 (Moved Permanently)?

**16.** Explica la diferencia semántica entre usar `GET /login` (mostrar formulario) y `POST /login` (enviar credenciales). ¿Por qué no se envían las credenciales por GET?

---

## 🚀 Despliegue y Configuración

**17.** El proyecto utiliza `Path(__file__).parent` para ubicar las plantillas y el archivo de sesiones. ¿Por qué es importante usar rutas absolutas basadas en la ubicación del archivo en lugar de rutas relativas a la carpeta de trabajo actual?

---

## 💡 finalmete: Pensamiento Crítico

**18. Bonus Extra:** Si tuvieras que convertir este proyecto didáctico en una aplicación real para producción, enumera al menos **5 cambios** que harías y justifica cada uno desde el punto de vista de seguridad, escalabilidad y mantenibilidad.

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


### 💡 Consejo para el estudiante:
> No intentes memorizar todo. Usa esta webgrafía como un **mapa**. Si al leer el código de `seguridad.py` no entiendes qué hace `request.cookies.get()`, ve a la sección de **MDN Web Docs**. Si al leer el `GUIA_PROFESOR.md` ves que habla de "Hashes", ve a la sección de **OWASP**. ¡La habilidad de buscar en la documentación oficial es la más importante de un desarrollador!
