from functools import lru_cache

from django import template
from django.conf import settings
from django.forms import boundfield
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from crispy_forms.exceptions import CrispyError
from crispy_forms.utils import TEMPLATE_PACK, flatatt


@lru_cache()
def uni_formset_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/uni_formset.html" % template_pack)


@lru_cache()
def uni_form_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/uni_form.html" % template_pack)


register = template.Library()


@register.filter(name="crispy")
def as_crispy_form(form, template_pack=TEMPLATE_PACK):
    helper = getattr(form, "helper", None)
    c = Context(
        {
            "field_template": "%s/field.html" % template_pack,
            "form_show_errors": helper.form_show_errors if helper is not None else True,
            "form_show_labels": helper.form_show_labels if helper is not None else True,
            "label_class": helper.label_class if helper is not None else "",
            "field_class": helper.field_class if helper is not None else "",
        }
    ).flatten()

    if isinstance(form, BaseFormSet):
        _template = uni_formset_template(template_pack)
        c["formset"] = form
    else:
        _template = uni_form_template(template_pack)
        c["form"] = form

    return _template.render(c)


@register.filter(name="as_crispy_errors")
def as_crispy_errors(form, template_pack=TEMPLATE_PACK):
    if isinstance(form, BaseFormSet):
        _template = get_template("%s/errors_formset.html" % template_pack)
        c = Context({"formset": form}).flatten()
    else:
        _template = get_template("%s/errors.html" % template_pack)
        c = Context({"form": form}).flatten()

    return _template.render(c)


@register.filter(name="as_crispy_field")
def as_crispy_field(field, template_pack=TEMPLATE_PACK):
    if not isinstance(field, boundfield.BoundField) and settings.DEBUG:
        raise CrispyError("|as_crispy_field got passed an invalid or inexistent field")

    helper = getattr(field.form, "helper", None)
    attributes = {
        "field": field,
        "form_show_errors": True,
        "form_show_labels": bool(helper.form_show_labels) if helper else True,
        "label_class": helper.label_class if helper else "",
        "field_class": helper.field_class if helper else "",
    }

    template_path = None
    if helper is not None:
        attributes.update(helper.get_attributes(template_pack))
        template_path = helper.field_template
    if not template_path:
        template_path = "%s/field.html" % template_pack
    _template = get_template(template_path)

    c = Context(attributes).flatten()
    return _template.render(c)


@register.filter(name="flatatt")
def flatatt_filter(attrs):
    return mark_safe(flatatt(attrs))
