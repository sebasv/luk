"""Tests for the html_builder package."""

import pytest

from htmpy import (
    H1,
    A,
    Body,
    Br,
    Button,
    Div,
    Head,
    Hr,
    Html,
    Img,
    Input,
    Li,
    Link,
    Meta,
    P,
    Script,
    Source,
    Span,
    Style,
    Table,
    Td,
    Th,
    Title,
    Tr,
    Trusted,
    Ul,
)

# ------------------------------------------------------------------
# Basic serialisation
# ------------------------------------------------------------------


class TestBasicSerialisation:
    def test_empty_div(self) -> None:
        assert Div().serialize(prepend_doctype=False) == "<div></div>"

    def test_div_with_text(self) -> None:
        assert Div("hello").serialize(prepend_doctype=False) == "<div>hello</div>"

    def test_span_with_text(self) -> None:
        assert Span("world").serialize(prepend_doctype=False) == "<span>world</span>"

    def test_nested_elements(self) -> None:
        result = Div(Span("inner")).serialize(prepend_doctype=False)
        assert result == "<div><span>inner</span></div>"

    def test_multiple_children(self) -> None:
        result = Div("one", Span("two"), "three").serialize(prepend_doctype=False)
        assert result == "<div>one<span>two</span>three</div>"

    def test_deeply_nested(self) -> None:
        result = Div(Div(Div("deep"))).serialize(prepend_doctype=False)
        assert result == "<div><div><div>deep</div></div></div>"


# ------------------------------------------------------------------
# Attributes
# ------------------------------------------------------------------


class TestAttributes:
    def test_single_attribute(self) -> None:
        assert (
            Div(id="main").serialize(prepend_doctype=False) == '<div id="main"></div>'
        )

    def test_class_attribute_with_trailing_underscore(self) -> None:
        result = Div(class_="container").serialize(prepend_doctype=False)
        assert result == '<div class="container"></div>'

    def test_data_attribute_underscore_to_hyphen(self) -> None:
        result = Div(data_value="42").serialize(prepend_doctype=False)
        assert result == '<div data-value="42"></div>'

    def test_boolean_true_attribute(self) -> None:
        result = Input(type="text", disabled=True).serialize(prepend_doctype=False)
        assert result == '<input type="text" disabled />'

    def test_boolean_false_attribute_omitted(self) -> None:
        result = Input(type="text", disabled=False).serialize(prepend_doctype=False)
        assert result == '<input type="text" />'

    def test_none_attribute_omitted(self) -> None:
        result = Div(id=None).serialize(prepend_doctype=False)
        assert result == "<div></div>"

    def test_multiple_attributes(self) -> None:
        result = A("click", href="/page", class_="link").serialize(
            prepend_doctype=False
        )
        assert result == '<a href="/page" class="link">click</a>'


# ------------------------------------------------------------------
# Self-closing (void) elements
# ------------------------------------------------------------------


class TestSelfClosing:
    def test_br(self) -> None:
        assert Br().serialize(prepend_doctype=False) == "<br />"

    def test_hr(self) -> None:
        assert Hr().serialize(prepend_doctype=False) == "<hr />"

    def test_img(self) -> None:
        result = Img(src="pic.png", alt="a picture").serialize(prepend_doctype=False)
        assert result == '<img src="pic.png" alt="a picture" />'

    def test_input(self) -> None:
        result = Input(type="text", name="q").serialize(prepend_doctype=False)
        assert result == '<input type="text" name="q" />'

    def test_meta(self) -> None:
        result = Meta(charset="utf-8").serialize(prepend_doctype=False)
        assert result == '<meta charset="utf-8" />'

    def test_link(self) -> None:
        result = Link(rel="stylesheet", href="style.css").serialize(
            prepend_doctype=False
        )
        assert result == '<link rel="stylesheet" href="style.css" />'

    def test_source(self) -> None:
        result = Source(src="video.mp4", type="video/mp4").serialize(
            prepend_doctype=False
        )
        assert result == '<source src="video.mp4" type="video/mp4" />'

    def test_self_closing_rejects_children(self) -> None:
        with pytest.raises(ValueError, match="self-closing"):
            Br("oops")


# ------------------------------------------------------------------
# HTML escaping
# ------------------------------------------------------------------


class TestEscaping:
    def test_text_content_escaped(self) -> None:
        result = Span("<script>alert('xss')</script>").serialize(prepend_doctype=False)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_attribute_value_escaped(self) -> None:
        result = Div(title='a "quoted" value').serialize(prepend_doctype=False)
        assert result == '<div title="a &quot;quoted&quot; value"></div>'

    def test_script_content_not_escaped(self) -> None:
        result = Script("console.log('hi');").serialize(prepend_doctype=False)
        assert result == "<script>console.log('hi');</script>"

    def test_style_content_not_escaped(self) -> None:
        css = "a[href*='?q=1&x=2']::before { content: '<&>'; }"
        result = Style(css).serialize(prepend_doctype=False)
        assert result == f"<style>{css}</style>"


# ------------------------------------------------------------------
# Realistic composite examples
# ------------------------------------------------------------------


class TestComposite:
    def test_simple_page(self) -> None:
        page = Html(
            Head(Title("My Page")),
            Body(
                H1("Welcome"),
                P("Hello, world!"),
            ),
        )
        result = page.serialize()
        assert result == (
            "<!DOCTYPE html>"
            "<html>"
            "<head><title>My Page</title></head>"
            "<body><h1>Welcome</h1><p>Hello, world!</p></body>"
            "</html>"
        )

    def test_unordered_list(self) -> None:
        result = Ul(Li("one"), Li("two"), Li("three")).serialize(prepend_doctype=False)
        assert result == "<ul><li>one</li><li>two</li><li>three</li></ul>"

    def test_table(self) -> None:
        result = Table(
            Tr(Th("Name"), Th("Age")),
            Tr(Td("Alice"), Td("30")),
        ).serialize(prepend_doctype=False)
        assert result == (
            "<table><tr><th>Name</th><th>Age</th></tr><tr><td>Alice</td><td>30</td></tr></table>"
        )

    def test_form(self) -> None:
        result = Div(
            Input(type="text", name="user"),
            Button("Submit", type="submit"),
        ).serialize(prepend_doctype=False)
        assert result == (
            '<div><input type="text" name="user" /><button type="submit">Submit</button></div>'
        )

    def test_trusted_inside_element(self) -> None:
        result = Div(Trusted("<b>bold</b>")).serialize(prepend_doctype=False)
        assert result == "<div><b>bold</b></div>"

    def test_page_with_css_and_js(self) -> None:
        page = Html(
            Head(
                Meta(charset="utf-8"),
                Title("Styled"),
                Link(rel="stylesheet", href="s.css"),
                Style("body { margin: 0; }"),
                Script("console.log('hi');"),
            ),
        )
        result = page.serialize(prepend_doctype=False)
        assert '<meta charset="utf-8" />' in result
        assert "<style>body { margin: 0; }</style>" in result
        assert "<script>console.log('hi');</script>" in result


# ------------------------------------------------------------------
# Trusted (no-escape container)
# ------------------------------------------------------------------


class TestTrusted:
    def test_single_string(self) -> None:
        assert Trusted("<b>bold</b>")._serialize() == "<b>bold</b>"

    def test_multiple_strings_concatenated(self) -> None:
        result = Trusted("<em>a</em>", "<em>b</em>")._serialize()
        assert result == "<em>a</em><em>b</em>"

    def test_no_escaping(self) -> None:
        raw = "<script>alert('xss')</script>"
        result = Trusted(raw)._serialize()
        assert result == raw

    def test_empty(self) -> None:
        assert Trusted()._serialize() == ""

    def test_rejects_element_children(self) -> None:
        with pytest.raises(TypeError, match="Trusted only accepts str children"):
            Trusted(Div())  # type: ignore[arg-type]

    def test_rejects_int_children(self) -> None:
        with pytest.raises(TypeError, match="Trusted only accepts str children"):
            Trusted(42)  # type: ignore[arg-type]

    def test_nested_in_element(self) -> None:
        result = Div("safe", Trusted("<hr />"), "also safe").serialize(
            prepend_doctype=False
        )
        assert result == "<div>safe<hr />also safe</div>"


# ------------------------------------------------------------------
# Context manager
# ------------------------------------------------------------------


class TestContextManager:
    """Tests for the Element context manager functionality."""

    def test_basic_context_manager(self) -> None:
        """Elements created inside a with block are appended as children."""
        with Div() as container:
            Span("hello")

        assert len(container.children) == 1
        assert container._serialize() == "<div><span>hello</span></div>"

    def test_multiple_children_in_context(self) -> None:
        """Multiple elements created in context are all appended."""
        with Div(class_="container") as container:
            Span("first")
            P("second")
            Span("third")

        assert len(container.children) == 3
        assert container._serialize() == (
            '<div class="container">'
            "<span>first</span>"
            "<p>second</p>"
            "<span>third</span>"
            "</div>"
        )

    def test_nested_context_managers(self) -> None:
        """Nested with blocks create nested element hierarchies."""
        with Div(class_="outer") as outer:
            Span("outer-child")
            with Div(class_="inner") as inner:
                Span("inner-child")
            P("after-inner")

        assert len(outer.children) == 3
        assert len(inner.children) == 1
        assert outer._serialize() == (
            '<div class="outer">'
            "<span>outer-child</span>"
            '<div class="inner"><span>inner-child</span></div>'
            "<p>after-inner</p>"
            "</div>"
        )

    def test_deeply_nested_context_managers(self) -> None:
        """Three levels of nesting work correctly."""
        with Div(id="level1") as level1:
            with Div(id="level2") as level2:
                with Div(id="level3") as level3:
                    Span("deep")

        assert len(level1.children) == 1
        assert len(level2.children) == 1
        assert len(level3.children) == 1
        assert level1._serialize() == (
            '<div id="level1">'
            '<div id="level2">'
            '<div id="level3">'
            "<span>deep</span>"
            "</div></div></div>"
        )

    def test_context_restored_after_exit(self) -> None:
        """After exiting a with block, elements are not appended to the old parent."""
        with Div() as container:
            Span("inside")

        # This element should NOT be appended to container
        orphan = P("outside")

        assert len(container.children) == 1
        assert orphan not in container.children

    def test_sibling_context_managers(self) -> None:
        """Sequential with blocks at the same level are independent."""
        with Div() as first:
            Span("first-child")

        with Div() as second:
            Span("second-child")

        assert len(first.children) == 1
        assert len(second.children) == 1
        assert first.children[0] not in second.children
        assert second.children[0] not in first.children

    def test_empty_context_manager(self) -> None:
        """A with block with no elements created inside produces no children."""
        with Div() as container:
            pass

        assert len(container.children) == 0
        assert container._serialize() == "<div></div>"

    def test_mixing_positional_children_and_context(self) -> None:
        """Positional children and context-created children coexist."""
        with Div("initial", Span("also-initial")) as container:
            P("added-via-context")

        assert len(container.children) == 3
        assert container._serialize() == (
            "<div>initial<span>also-initial</span><p>added-via-context</p></div>"
        )

    def test_self_closing_element_rejects_context_manager(self) -> None:
        """Self-closing elements raise ValueError when used as context managers."""
        with pytest.raises(ValueError, match="self-closing"):
            with Br():
                pass

    def test_self_closing_img_rejects_context_manager(self) -> None:
        """Img element raises ValueError when used as context manager."""
        with pytest.raises(ValueError, match="self-closing"):
            with Img(src="test.png"):
                pass

    def test_self_closing_input_rejects_context_manager(self) -> None:
        """Input element raises ValueError when used as context manager."""
        with pytest.raises(ValueError, match="self-closing"):
            with Input(type="text"):
                pass

    def test_context_manager_returns_self(self) -> None:
        """The with statement's 'as' clause receives the element itself."""
        div = Div(id="test")
        with div as ctx:
            pass

        assert ctx is div

    def test_context_restored_on_exception(self) -> None:
        """Context is properly restored even when an exception occurs."""
        with Div() as outer:
            try:
                with Div() as inner:
                    Span("before-error")
                    raise RuntimeError("test error")
            except RuntimeError:
                pass
            # This should be added to outer, not inner
            P("after-error")

        assert len(outer.children) == 2  # inner div and P
        assert len(inner.children) == 1  # just the span

    def test_element_created_outside_context_not_appended(self) -> None:
        """Elements created outside any context have no automatic parent."""
        before = Span("before")

        with Div() as container:
            Span("inside")

        after = Span("after")

        assert len(container.children) == 1
        assert before not in container.children
        assert after not in container.children

    def test_context_manager_with_text_children(self) -> None:
        """Text nodes can be mixed with element children in context."""
        with Div() as container:
            Span("element")

        # Note: raw strings cannot be auto-appended since they aren't Elements
        # Only Element instances get auto-appended
        assert len(container.children) == 1

    def test_realistic_page_structure(self) -> None:
        """Build a realistic page structure using context managers."""
        with Html() as page:
            with Head():
                Title("Test Page")
                Meta(charset="utf-8")
            with Body():
                with Div(class_="header"):
                    H1("Welcome")
                with Div(class_="content"):
                    P("Hello, world!")
                    with Ul():
                        Li("Item 1")
                        Li("Item 2")
                        Li("Item 3")

        result = page.serialize()
        assert "<html>" in result
        assert "<head>" in result
        assert "<title>Test Page</title>" in result
        assert '<meta charset="utf-8" />' in result
        assert "<body>" in result
        assert '<div class="header">' in result
        assert "<h1>Welcome</h1>" in result
        assert '<div class="content">' in result
        assert "<ul>" in result
        assert "<li>Item 1</li>" in result

    def test_context_with_different_element_types(self) -> None:
        """Various element types work correctly as context managers."""
        with Ul() as ul:
            Li("one")
            Li("two")

        with Table() as table:
            with Tr():
                Th("Header")
            with Tr():
                Td("Data")

        assert len(ul.children) == 2
        assert ul._serialize() == "<ul><li>one</li><li>two</li></ul>"

        assert len(table.children) == 2
        assert table._serialize() == (
            "<table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>"
        )
