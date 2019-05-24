# coding: utf-8

from django.core.management.base import NoArgsCommand
from django.conf import settings

from wagtail.core.models import Page


class Command(NoArgsCommand):
    def set_subtree(self, root, root_path, lang=None):
        update_fields = ['url_path_'+lang] if hasattr(root.specific, 'url_path_'+lang) else ['url_path']

        if hasattr(root.specific, 'url_path_'+lang):
            setattr(root.specific, 'url_path_'+lang, root_path)
        else:
            setattr(root, 'url_path', root_path)

        if lang == settings.LANGUAGE_CODE:
            setattr(root, 'url_path', root_path)
            update_fields.append('url_path')
        root.specific.save(update_fields=update_fields)
        for child in root.get_children():
            slug = getattr(
                child.specific, 'slug_'+lang) if hasattr(
                    child.specific, 'slug_'+lang) else getattr(child, 'slug')
            if not slug or slug == '':
                slug = getattr(
                    child.specific, 'slug_'+settings.LANGUAGE_CODE) if hasattr(child.specific, 'slug_'+settings.LANGUAGE_CODE) and getattr(child.specific, 'slug_'+settings.LANGUAGE_CODE) else getattr(child, 'slug')

            self.set_subtree(child, root_path + slug + '/', lang)

    def handle_noargs(self, **options):
        for node in Page.get_root_nodes():
            for lang in settings.LANGUAGES:
                self.set_subtree(node, '/', lang=lang[0])
