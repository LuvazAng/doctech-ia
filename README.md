# Acerca del proyecto
---
**DocTech IA** es un proyecto _open-source_ enfocado en la generación automática de documentación técnica a partir del análisis de código fuente. Su funcionamiento se inspira en herramientas como _Deep Wiki_, y está diseñado para analizar un repositorio clonado desde su directorio raíz, recorriendo de manera recursiva todos sus archivos y subdirectorios.

El código del proyecto se fragmenta y transforma en _embeddings_, los cuales son utilizados por un modelo de lenguaje (LLM) para comprender el contenido del repositorio. Con esta información, el modelo genera documentación técnica precisa y coherente, alineada fielmente con la lógica y estructura del código.

DocTech IA será compatible con modelos LLM ejecutados localmente, como los soportados por **Ollama** o **LM Studio**, así como con modelos accesibles mediante API, como **ChatGPT de OpenAI** o **Gemini de Google**.

El proyecto está desarrollado en **Python 3.10 o superior**.