# coding utf-8

from wagtail.core.models import Page
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(Page)
class PageTR(TranslationOptions):
    pass
