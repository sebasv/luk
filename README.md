# luk

Create static HTML inside Python. No templates, no dependencies, just Python. Create objects directly or use the context manager to use control flow like `if/else`, add objects in loops, etcetera. Examples below 👇

## Why luk?

* Luk lets you write HTML from within python. You don't have to learn the DSL of a template engine like `jinja` to build a html page.
* Luk is lightweight. Just some very simple python, no bells or whistles.
* Luk is friendly to static type checkers
* Luk is idiomatic Python. `htpy` does a similar thing but they use a trick on the index operator (`[]`). I understand they did it to separate attributes and children, but I prefer a more pythonic feel.

## Installation

```bash
pip install luk
```

## Quick Start

```python
import luk

page = luk.Html(
    luk.Head(luk.Title("My Page")),
    luk.Body(
        luk.H1("Welcome"),
        luk.Div(
            luk.P("Hello, ", luk.A("world", href="https://example.com"), "!"),
            class_="container",
        ),
    ),
)

print(page.serialize())

# or serve from a fastapi/flask/whatever endpoint!
import flask

app = flask.Flask(__name__)

@app.route("/hello/<name>")
def hello_name_page(name):
    page = luk.Html(
        luk.Head(luk.Title(f"Hello, {name}!")),
        luk.Body(
            luk.H1(f"Welcome, {name}!"),
            luk.P("This page was generated using luk and a Flask route parameter."),
        ),
    )
    return page.serialize()
```

Output:

```html
<!DOCTYPE html><html><head><title>My Page</title></head><body><h1>Welcome</h1><div class="container"><p>Hello, <a href="https://example.com">world</a>!</p></div></body></html>
```

## Features

### Nested Elements

Pass child elements as positional arguments:

```python
import luk

menu = luk.Ul(
    luk.Li("Home"),
    luk.Li("About"),
    luk.Li("Contact"),
)
```

### Attributes

Pass attributes as keyword arguments:

```python
import luk

# Use trailing underscore for reserved words (class, for, etc.)
luk.Div(class_="container", id="main")

# Underscores in names become hyphens
luk.Div(data_user_id="123")  # renders as data-user-id="123"

# Boolean attributes
luk.Input(type="checkbox", checked=True)   # renders: <input type="checkbox" checked />
luk.Input(type="checkbox", checked=False)  # renders: <input type="checkbox" />
```

### Context Manager

Build nested structures using `with` statements. Elements created inside a `with` block are automatically appended as children:

```python
import luk

with luk.Html() as page:
    with luk.Head():
        luk.Title("My Page")
    with luk.Body():
        with luk.Div(class_="header"):
            luk.H1("Welcome")
        with luk.Div(class_="content"):
            luk.P("Here are some items:")
            with luk.Ul():
                for e in ["First", "Second", "Third"]:
                luk.Li(f"{e} item")

print(page.serialize())
```

This produces the same output as the nested constructor style, but can be more readable for complex structures.

### Self-Closing Elements

Void elements like `<br>`, `<img>`, `<input>`, and `<meta>` are self-closing and cannot have children:

```python
import luk

luk.Img(src="photo.jpg", alt="A photo")  # <img src="photo.jpg" alt="A photo" />
luk.Br()                                  # <br />
luk.Input(type="text", name="email")      # <input type="text" name="email" />
luk.Meta(charset="utf-8")                 # <meta charset="utf-8" />
```

### Script and Style Elements

Content inside `<script>` and `<style>` tags is not escaped:

```python
import luk

luk.Script("console.log('Hello, world!');")
# <script>console.log('Hello, world!');</script>

luk.Style("body { margin: 0; }")
# <style>body { margin: 0; }</style>
```

### Trusted Content

Use `Trusted` to insert pre-built HTML without escaping:

```python
import luk

# Useful for embedding HTML from trusted sources (e.g., markdown renderers)
luk.Div(luk.Trusted("<strong>Already formatted</strong> content"))
```

**Warning:** Only use `Trusted` with content you control. Never use it with user input.

### HTML Escaping

Text content and attribute values are automatically escaped to prevent XSS:

```python
import luk

luk.Span("<script>alert('xss')</script>")
# <span>&lt;script&gt;alert('xss')&lt;/script&gt;</span>

luk.Div(title='He said "hello"')
# <div title="He said &quot;hello&quot;"></div>
```

### Writing to Files

Save the rendered HTML directly to a file:

```python
import luk

page = luk.Html(
    luk.Head(luk.Title("My Page")),
    luk.Body(luk.H1("Hello!")),
)

page.write("index.html")
```

### Serialization Options

```python
page.serialize()                    # Includes <!DOCTYPE html> prefix
page.serialize(prepend_doctype=False)  # Without doctype
```

## Available Elements

### Document
`Html`, `Head`, `Body`, `Title`, `Meta`, `Link`, `Script`, `Style`

### Sections
`Div`, `Section`, `Article`, `Nav`, `Header`, `Footer`, `Main`, `Aside`

### Headings
`H1`, `H2`, `H3`, `H4`, `H5`, `H6`

### Text
`P`, `Span`, `A`, `Strong`, `Em`, `B`, `I`, `Br`, `Hr`, `Pre`, `Code`, `Blockquote`

### Lists
`Ul`, `Ol`, `Li`

### Tables
`Table`, `Thead`, `Tbody`, `Tr`, `Th`, `Td`

### Forms
`Form`, `Input`, `Button`, `Label`, `Select`, `Option`, `Textarea`

### Media
`Img`, `Video`, `Audio`, `Source`

### Interactive
`Details`, `Summary`
