# htmpy

Create static HTML inside Python. No templates, just Python. Create objects directly or use the context manager to use control flow like `if/else`, add objects in loops, etcetera.

## Installation

```bash
pip install htmpy
```

## Quick Start

```python
import htmpy as hp

page = hp.Html(
    hp.Head(hp.Title("My Page")),
    hp.Body(
        hp.H1("Welcome"),
        hp.Div(
            hp.P("Hello, ", hp.A("world", href="https://example.com"), "!"),
            class_="container",
        ),
    ),
)

print(page.serialize())
```

Output:

```html
<!DOCTYPE html><html><head><title>My Page</title></head><body><h1>Welcome</h1><div class="container"><p>Hello, <a href="https://example.com">world</a>!</p></div></body></html>
```

## Features

### Nested Elements

Pass child elements as positional arguments:

```python
import htmpy as hp

menu = hp.Ul(
    hp.Li("Home"),
    hp.Li("About"),
    hp.Li("Contact"),
)
```

### Attributes

Pass attributes as keyword arguments:

```python
import htmpy as hp

# Use trailing underscore for reserved words (class, for, etc.)
hp.Div(class_="container", id="main")

# Underscores in names become hyphens
hp.Div(data_user_id="123")  # renders as data-user-id="123"

# Boolean attributes
hp.Input(type="checkbox", checked=True)   # renders: <input type="checkbox" checked />
hp.Input(type="checkbox", checked=False)  # renders: <input type="checkbox" />
```

### Context Manager

Build nested structures using `with` statements. Elements created inside a `with` block are automatically appended as children:

```python
import htmpy as hp

with hp.Html() as page:
    with hp.Head():
        hp.Title("My Page")
    with hp.Body():
        with hp.Div(class_="header"):
            hp.H1("Welcome")
        with hp.Div(class_="content"):
            hp.P("Here are some items:")
            with hp.Ul():
                for e in ["First", "Second", "Third"]:
                hp.Li(f"{e} item")

print(page.serialize())
```

This produces the same output as the nested constructor style, but can be more readable for complex structures.

### Self-Closing Elements

Void elements like `<br>`, `<img>`, `<input>`, and `<meta>` are self-closing and cannot have children:

```python
import htmpy as hp

hp.Img(src="photo.jpg", alt="A photo")  # <img src="photo.jpg" alt="A photo" />
hp.Br()                                  # <br />
hp.Input(type="text", name="email")      # <input type="text" name="email" />
hp.Meta(charset="utf-8")                 # <meta charset="utf-8" />
```

### Script and Style Elements

Content inside `<script>` and `<style>` tags is not escaped:

```python
import htmpy as hp

hp.Script("console.log('Hello, world!');")
# <script>console.log('Hello, world!');</script>

hp.Style("body { margin: 0; }")
# <style>body { margin: 0; }</style>
```

### Trusted Content

Use `Trusted` to insert pre-built HTML without escaping:

```python
import htmpy as hp

# Useful for embedding HTML from trusted sources (e.g., markdown renderers)
hp.Div(hp.Trusted("<strong>Already formatted</strong> content"))
```

**Warning:** Only use `Trusted` with content you control. Never use it with user input.

### HTML Escaping

Text content and attribute values are automatically escaped to prevent XSS:

```python
import htmpy as hp

hp.Span("<script>alert('xss')</script>")
# <span>&lt;script&gt;alert('xss')&lt;/script&gt;</span>

hp.Div(title='He said "hello"')
# <div title="He said &quot;hello&quot;"></div>
```

### Writing to Files

Save the rendered HTML directly to a file:

```python
import htmpy as hp

page = hp.Html(
    hp.Head(hp.Title("My Page")),
    hp.Body(hp.H1("Hello!")),
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
