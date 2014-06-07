# -*- coding: utf-8 -*-

import os
import sys
import copy

from jinja2 import Environment
from jinja2 import Template
from jinja2 import loaders
from jinja2 import TemplateSyntaxError
from jinja2 import FileSystemLoader

from django.conf import settings
from django.template.context import BaseContext
from django.template import TemplateDoesNotExist
from django.template import Origin
from django.template import InvalidTemplateLibrary
from django.template.loaders import app_directories
from django.utils.importlib import import_module

from . import builtins
from .library import Library


JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})
JINJA2_EXTENSIONS = getattr(settings, 'JINJA2_EXTENSIONS', [])
JINJA2_FILTERS = getattr(settings, 'JINJA2_FILTERS', {})
JINJA2_TESTS = getattr(settings, 'JINJA2_TESTS', {})
JINJA2_GLOBALS = getattr(settings, 'JINJA2_GLOBALS', {})
JINJA2_AUTOESCAPE = getattr(settings, 'JINJA2_AUTOESCAPE', False)


JINJA2_FILTERS.update({
    'reverseurl': builtins.filters.reverse,
    'addslashes': builtins.filters.addslashes,
    'capfirst': builtins.filters.capfirst,
    'escapejs': builtins.filters.escapejs_filter,
    'fix_ampersands': builtins.filters.fix_ampersands_filter,
    'floatformat': builtins.filters.floatformat,
    'iriencode': builtins.filters.iriencode,
    'linenumbers': builtins.filters.linenumbers,
    'make_list': builtins.filters.make_list,
    'slugify': builtins.filters.slugify,
    'stringformat': builtins.filters.stringformat,
    'title': builtins.filters.title,
    'truncatechars': builtins.filters.truncatechars,
    'truncatewords': builtins.filters.truncatewords,
    'truncatewords_html': builtins.filters.truncatewords_html,
    'upper': builtins.filters.upper,
    'lower': builtins.filters.lower,
    'urlencode': builtins.filters.urlencode,
    'urlize': builtins.filters.urlize,
    'urlizetrunc': builtins.filters.urlizetrunc,
    'wordcount': builtins.filters.wordcount,
    'wordwrap': builtins.filters.wordwrap,
    'ljust': builtins.filters.ljust,
    'rjust': builtins.filters.rjust,
    'center': builtins.filters.center,
    'cut': builtins.filters.cut,
    'linebreaksbr': builtins.filters.linebreaksbr,
    'linebreaks': builtins.filters.linebreaks_filter,
    'removetags': builtins.filters.removetags,
    'striptags': builtins.filters.striptags,
    'join': builtins.filters.join,
    'length': builtins.filters.length,
    'random': builtins.filters.random,
    'add': builtins.filters.add,
    'date': builtins.filters.date,
    'time': builtins.filters.time,
    'timesince': builtins.filters.timesince_filter,
    'timeuntil': builtins.filters.timeuntil_filter,
    'default': builtins.filters.default,
    'default_if_none': builtins.filters.default_if_none,
    'divisibleby': builtins.filters.divisibleby,
    'yesno': builtins.filters.yesno,
    'filesizeformat': builtins.filters.filesizeformat,
    'pprint': builtins.filters.pprint,
    'pluralize': builtins.filters.pluralize,
})

JINJA2_GLOBALS.update({
    'url': builtins.global_context.url,
    'static': builtins.global_context.static,
})


def dict_from_context(context):
    """
    Converts context to native python dict.
    """

    if isinstance(context, BaseContext):
        new_dict = {}
        for i in reversed(list(context)):
            new_dict.update(dict_from_context(i))
        return new_dict

    return dict(context)


class Template(Template):
    """
    Customized template class.
    Add correct handling django context objects.
    """

    def render(self, context={}):
        new_context = dict_from_context(context)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).render(new_context)


class Environment(Environment):
    def __init__(self, *args, **kwargs):
        super(Environment, self).__init__(*args, **kwargs)

        # install translations
        if settings.USE_I18N:
            from django.utils import translation
            self.install_gettext_translations(translation)
        else:
            self.install_null_translations(newstyle=False)

        self.template_class = Template

        # Add filters defined on settings + builtins
        for name, value in JINJA2_FILTERS.items():
            self.filters[name] = value

        # Add tests defined on settings + builtins
        for name, value in JINJA2_TESTS.items():
            self.tests[name] = value

        # Add globals defined on settings + builtins
        for name, value in JINJA2_GLOBALS.items():
            self.globals[name] = value

        mod_list = []
        for app_path in settings.INSTALLED_APPS:
            try:
                mod = import_module(app_path + '.templatetags')
                mod_list.append((app_path,os.path.dirname(mod.__file__)))
            except ImportError:
                pass

        for app_path, mod_path in mod_list:
            for filename in filter(lambda x: x.endswith(".py"), os.listdir(mod_path)):
                if filename == '__init__.py':
                    continue

                file_mod_path = "%s.templatetags.%s" % (app_path, filename.rsplit(".", 1)[0])
                try:
                    filemod = import_module(file_mod_path)
                except ImportError:
                    pass

        # Update current environment with app filters
        Library()._update_env(self)

        # Add builtin extensions.
        self.add_extension(builtins.extensions.CsrfExtension)
        self.add_extension(builtins.extensions.CacheExtension)

        if self.autoescape:
            from django.utils import safestring
            if hasattr(safestring, "SafeText"):
                if not hasattr(safestring.SafeText, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeText.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeText.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeString"):
                if not hasattr(safestring.SafeString, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeString.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeString.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeUnicode"):
                if not hasattr(safestring.SafeUnicode, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeUnicode.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeUnicode.__html__ = lambda self: str(self)

            if hasattr(safestring, "SafeBytes"):
                if not hasattr(safestring.SafeBytes, '__html__'):
                    if sys.version_info.major < 3:
                        safestring.SafeBytes.__html__ = lambda self: unicode(self)
                    else:
                        safestring.SafeBytes.__html__ = lambda self: str(self)


initial_params = {
    'autoescape': JINJA2_AUTOESCAPE,
    'loader': FileSystemLoader(app_directories.app_template_dirs + tuple(settings.TEMPLATE_DIRS)),
    'extensions': JINJA2_EXTENSIONS + ['jinja2.ext.i18n', 'jinja2.ext.autoescape'],
}

initial_params.update(JINJA2_ENVIRONMENT_OPTIONS)
env = Environment(**initial_params)
