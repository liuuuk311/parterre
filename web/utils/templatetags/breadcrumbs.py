from django import template
from django.template import VariableDoesNotExist, Variable, Node
from django.template.defaulttags import url

register = template.Library()


@register.tag
def breadcrumb(parser, token):
    """
    Renders the breadcrumb.
    Examples:
        {% breadcrumb "Title of breadcrumb" url_var %}
        {% breadcrumb context_var  url_var %}
        {% breadcrumb "Just the title" %}
        {% breadcrumb just_context_var %}

    Parameters:
    -First parameter is the title of the crumb,
    -Second (optional) parameter is the url variable to link to, produced by url tag, i.e.:
        {% url person_detail object.id as person_url %}
        then:
        {% breadcrumb person.name person_url %}

    """
    return BreadcrumbNode(token.split_contents()[1:])


@register.tag
def breadcrumb_url(parser, token):
    """
    Same as breadcrumb
    but instead of url context variable takes in all the
    arguments URL tag takes.
        {% breadcrumb "Title of breadcrumb" person_detail person.id %}
        {% breadcrumb person.name person_detail person.id %}
    """

    bits = token.split_contents()
    if len(bits) == 2:
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return UrlBreadcrumbNode(title, url_node)


class BreadcrumbNode(Node):
    def __init__(self, _vars):
        """
        First var is title, second var is url context variable
        """
        self._vars = list(map(Variable, _vars))

    def render(self, context):
        title = self._vars[0].var

        if title.find("'") == -1 and title.find('"') == -1:
            title = self._vars[0].resolve(context)
        else:
            title = title.strip("'").strip('"')
        link = None

        if len(self._vars) > 1:
            val = self._vars[1]
            try:
                link = val.resolve(context)
            except VariableDoesNotExist:
                link = None

        return create_crumb(title, link)


class UrlBreadcrumbNode(Node):
    def __init__(self, title, url_node):
        self.title = Variable(title)
        self.url_node = url_node

    def render(self, context):
        title = self.title.var

        if title.find("'") == -1 and title.find('"') == -1:
            title = self.title.resolve(context)
        else:
            title = title.strip("'").strip('"')

        return create_crumb(title, self.url_node.render(context))


def create_crumb(title, link: str = None):
    crumb = """
        <span class="mx-2 text-gray-500 dark:text-gray-300 rtl:-scale-x-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
        </span>
    """
    return (
        f'{crumb}<a href="{link}" class=" hover:underline">{title.capitalize()}</a>'
        if link
        else f"{crumb}&nbsp;&nbsp;{title}"
    )
