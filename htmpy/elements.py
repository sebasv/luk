"""HTML element classes for building HTML documents programmatically."""

from __future__ import annotations

import html
from contextvars import ContextVar, Token
from pathlib import Path
from types import TracebackType

# Context variable to track the current parent element in a `with` block
_current_parent: ContextVar[Element | None] = ContextVar(
    "_current_parent", default=None
)


class Element:
    """Base class for all HTML elements.

    Children are passed as positional arguments and can be ``Element`` instances
    or plain strings (text nodes).  Attributes are passed as keyword arguments.

    Attribute name conventions:
    - A trailing underscore is stripped so Python reserved words can be used
      (e.g. ``class_="container"`` renders as ``class="container"``).
    - Interior underscores are converted to hyphens
      (e.g. ``data_id="5"`` renders as ``data-id="5"``).
    - A boolean ``True`` value renders the attribute as a bare/boolean attribute.
    - ``False`` and ``None`` values cause the attribute to be omitted.
    """

    tag: str = ""
    self_closing: bool = False
    raw_text: bool = False
    _parent_token: Token[Element | None]

    def __init__(
        self, *children: Element | Trusted | str, **attributes: str | bool | None
    ) -> None:
        if self.self_closing and children:
            raise ValueError(
                f"<{self.tag}> is a self-closing (void) element and cannot have children."
            )
        self.children: list[Element | Trusted | str] = list(children)
        self.attributes = attributes

        # If created inside a `with` block, append self to the parent
        parent = _current_parent.get()
        if parent is not None:
            parent.children.append(self)

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------

    def __enter__(self) -> Element:
        """Enter a context where new elements are appended as children."""
        if self.self_closing:
            raise ValueError(
                f"<{self.tag}> is a self-closing (void) element and cannot have children."
            )
        self._parent_token = _current_parent.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Restore the previous parent context."""
        _current_parent.reset(self._parent_token)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalise_attr_name(name: str) -> str:
        """Convert a Python-friendly attribute name to its HTML equivalent."""
        # Strip trailing underscore (allows class_, for_, etc.)
        if name.endswith("_"):
            name = name[:-1]
        # Convert interior underscores to hyphens
        return name.replace("_", "-")

    def _serialize_attributes(self) -> str:
        parts: list[str] = []
        for key, value in self.attributes.items():
            if value is None or value is False:
                continue
            attr_name = self._normalise_attr_name(key)
            if value is True:
                parts.append(attr_name)
            else:
                escaped = html.escape(str(value), quote=True)
                parts.append(f'{attr_name}="{escaped}"')
        if not parts:
            return ""
        return " " + " ".join(parts)

    def _serialize_children(self) -> str:
        pieces: list[str] = []
        for child in self.children:
            if isinstance(child, (Element, Trusted)):
                pieces.append(child._serialize())  # pyright: ignore
            else:
                if self.raw_text:
                    pieces.append(str(child))
                else:
                    pieces.append(html.escape(str(child)))
        return "".join(pieces)

    def _serialize(self) -> str:
        """Return the HTML string for this element and all its descendants."""
        attrs = self._serialize_attributes()
        if self.self_closing:
            return f"<{self.tag}{attrs} />"
        inner = self._serialize_children()
        return f"<{self.tag}{attrs}>{inner}</{self.tag}>"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def serialize(self, prepend_doctype: bool = True) -> str:
        if prepend_doctype:
            return "<!DOCTYPE html>" + self._serialize()
        return self._serialize()

    def write(self, path: str | Path) -> None:
        """Serialize this element and write the result to a file at *path*."""
        Path(path).write_text(self.serialize())


# ======================================================================
# Concrete element classes
# ======================================================================

# -- Document ----------------------------------------------------------


class Html(Element):
    tag = "html"


class Head(Element):
    tag = "head"


class Body(Element):
    tag = "body"


class Title(Element):
    tag = "title"


class Meta(Element):
    tag = "meta"
    self_closing = True


class Link(Element):
    tag = "link"
    self_closing = True


class Script(Element):
    tag = "script"
    raw_text = True


class Style(Element):
    tag = "style"
    raw_text = True


# -- Sections / Layout ------------------------------------------------


class Div(Element):
    tag = "div"


class Section(Element):
    tag = "section"


class Article(Element):
    tag = "article"


class Nav(Element):
    tag = "nav"


class Header(Element):
    tag = "header"


class Footer(Element):
    tag = "footer"


class Main(Element):
    tag = "main"


class Aside(Element):
    tag = "aside"


# -- Headings ----------------------------------------------------------


class H1(Element):
    tag = "h1"


class H2(Element):
    tag = "h2"


class H3(Element):
    tag = "h3"


class H4(Element):
    tag = "h4"


class H5(Element):
    tag = "h5"


class H6(Element):
    tag = "h6"


# -- Inline text -------------------------------------------------------


class Span(Element):
    tag = "span"


class A(Element):
    tag = "a"


class Strong(Element):
    tag = "strong"


class Em(Element):
    tag = "em"


class B(Element):
    tag = "b"


class I(Element):  # noqa
    tag = "i"


class Br(Element):
    tag = "br"
    self_closing = True


class Hr(Element):
    tag = "hr"
    self_closing = True


# -- Text / preformatted ----------------------------------------------


class P(Element):
    tag = "p"


class Pre(Element):
    tag = "pre"


class Code(Element):
    tag = "code"


class Blockquote(Element):
    tag = "blockquote"


# -- Lists -------------------------------------------------------------


class Ul(Element):
    tag = "ul"


class Ol(Element):
    tag = "ol"


class Li(Element):
    tag = "li"


# -- Table -------------------------------------------------------------


class Table(Element):
    tag = "table"


class Thead(Element):
    tag = "thead"


class Tbody(Element):
    tag = "tbody"


class Tr(Element):
    tag = "tr"


class Th(Element):
    tag = "th"


class Td(Element):
    tag = "td"


# -- Forms -------------------------------------------------------------


class Form(Element):
    tag = "form"


class Input(Element):
    tag = "input"
    self_closing = True


class Button(Element):
    tag = "button"


class Label(Element):
    tag = "label"


class Select(Element):
    tag = "select"


class Option(Element):
    tag = "option"


class Textarea(Element):
    tag = "textarea"


# -- Media -------------------------------------------------------------


class Img(Element):
    tag = "img"
    self_closing = True


class Video(Element):
    tag = "video"


class Audio(Element):
    tag = "audio"


class Source(Element):
    tag = "source"
    self_closing = True


# -- Media -------------------------------------------------------------


class Summary(Element):
    tag = "summary"


class Details(Element):
    tag = "details"


# -- Trusted (no escaping) --------------------------------------------


class Trusted:
    """A container for pre-built HTML that is inserted verbatim (no escaping).

    Unlike ``Element``, ``Trusted`` does **not** represent an HTML tag.  It
    simply wraps one or more raw strings that are concatenated as-is during
    serialisation.  This is useful for injecting HTML that has already been
    escaped or generated by a trusted source (e.g. a plotting library).

    Only plain strings are accepted as children – passing an ``Element``
    instance will raise a ``TypeError``.
    """

    def __init__(self, *children: str) -> None:
        for child in children:
            if not isinstance(child, str):  # pyright: ignore
                raise TypeError(
                    f"Trusted only accepts str children, got {type(child).__name__}"
                )
        self.children = children

    def _serialize(self) -> str:
        """Return the concatenated raw strings without any HTML escaping."""
        return "".join(self.children)
