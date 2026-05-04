# Despacho de Noé

Blog personal de Noé. Opiniones, Recomendaciones, Historias y Conversaciones.

---

## Estructura del proyecto

```
despacho-de-noe/
├── index.html              ← Portada (generada automáticamente por el build)
├── sobre-noe.html          ← Página estática "Sobre Noé"
├── contacto.html           ← Página estática de contacto
├── assets/
│   ├── style.css           ← Hoja de estilos Art Déco
│   ├── logo.svg            ← Logo horizontal
│   └── logo-square.svg     ← Logo cuadrado (redes sociales)
├── posts/                  ← Posts generados automáticamente en HTML
├── _posts/                 ← Aquí escribes tus artículos en Markdown ✍️
├── _templates/
│   ├── post.html           ← Plantilla para cada artículo
│   └── index.html          ← Plantilla para la portada
├── _scripts/
│   └── build.py            ← Script de conversión MD → HTML
└── .github/
    └── workflows/
        └── build.yml       ← GitHub Action automática
```

---

## Cómo publicar un artículo

### 1. Crea un archivo `.md` en `_posts/`

Nombra el archivo con el formato: `YYYY-MM-DD-titulo-del-articulo.md`

Ejemplo: `_posts/2025-02-01-mi-nuevo-articulo.md`

### 2. Añade el frontmatter al principio

```markdown
---
title: El título de tu artículo
category: opiniones
date: 2025-02-01
excerpt: Un resumen de una o dos frases que aparecerá en la portada y en el SEO.
slug: mi-nuevo-articulo
author: Noé
draft: false
---

Aquí empieza el contenido en Markdown...
```

### Categorías disponibles

| Valor              | Etiqueta         |
|--------------------|------------------|
| `opiniones`        | Opiniones        |
| `recomendaciones`  | Recomendaciones  |
| `historias`        | Historias        |
| `conversaciones`   | Conversaciones   |

### 3. Haz push a `main`

GitHub Actions se encargará del resto automáticamente. En 1-2 minutos el artículo estará en línea.

Si quieres guardar un borrador sin publicarlo, pon `draft: true` en el frontmatter.

---

## Sintaxis Markdown disponible

```markdown
# Título H1
## Título H2
### Título H3

Párrafo normal.

**Negrita** y *cursiva*

> Una cita destacada que aparecerá con formato especial

- Lista
- de elementos

[Texto del enlace](https://url.com)
```

---

## Setup inicial en GitHub

### GitHub Pages

1. Ve a **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Guarda — tu web estará en `https://TU_USUARIO.github.io/TU_REPO/`

### Dominio personalizado (despachodenoe.es)

1. En **Settings → Pages → Custom domain**, escribe `despachodenoe.es`
2. En tu proveedor de dominio, añade estos registros DNS:

```
Tipo    Nombre    Valor
A       @         185.199.108.153
A       @         185.199.109.153
A       @         185.199.110.153
A       @         185.199.111.153
CNAME   www       TU_USUARIO.github.io
```

3. Activa **Enforce HTTPS** una vez propagado.

### Formulario de contacto (Formspree)

1. Regístrate en [formspree.io](https://formspree.io) (plan gratuito funciona)
2. Crea un nuevo formulario y copia tu Form ID
3. En `contacto.html`, cambia esta línea:
   ```html
   <form ... action="https://formspree.io/f/YOUR_FORM_ID" ...>
   ```
   por tu ID real.

### URLs de redes sociales

Busca `https://instagram.com/` y `https://linkedin.com/` en los archivos HTML y reemplázalos con tus URLs reales.

---

## Logos

Los logos SVG están en `assets/`:

- **`logo.svg`** — Formato horizontal (600×180px). Para cabeceras web, banners.
- **`logo-square.svg`** — Formato cuadrado (500×500px). Para foto de perfil en Instagram, LinkedIn, etc.

Para exportarlos como PNG (para redes que no aceptan SVG):
- Abre el SVG en el navegador → botón derecho → Guardar imagen
- O usa [cloudconvert.com](https://cloudconvert.com) para convertir SVG → PNG a la resolución que necesites.

---

Hecho con calma y café. ☕
