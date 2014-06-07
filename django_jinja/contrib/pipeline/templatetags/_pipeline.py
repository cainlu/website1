# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import render_to_string

from pipeline.conf import settings
from pipeline.utils import guess_type
from pipeline.packager import Packager, PackageNotFound

from django_jinja import library

lib = library.Library()


@lib.global_function
def compressed_css(name):
    package = settings.PIPELINE_CSS.get(name, {})
    if package:
        package = {name: package}

    packager = Packager(css_packages=package, js_packages={})

    try:
        package = packager.package_for('css', name)
    except PackageNotFound:
        return ""

    def _render_css(path):
        template_name = package.template_name or "pipeline/css.jinja"

        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/css'),
            'url': staticfiles_storage.url(path)
        })

        return render_to_string(template_name, context)

    if not settings.DEBUG:
        return _render_css(package.output_filename)

    paths = packager.compile(package.paths)
    tags = [_render_css(path) for path in paths]

    return '\n'.join(tags)


@lib.global_function
def compressed_js(name):
    package = settings.PIPELINE_JS.get(name, {})
    if package:
        package = {name: package}

    packager = Packager(css_packages={}, js_packages=package)
    try:
        package = packager.package_for('js', name)
    except PackageNotFound:
        return ""

    def _render_js(path):
        template_name = package.template_name or "pipeline/js.jinja"
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/javascript'),
            'url': staticfiles_storage.url(path),
        })
        return render_to_string(template_name, context)

    def _render_inline_js(js):
        context = package.extra_context
        context.update({
            'source': js
        })
        return render_to_string("pipeline/inline_js.jinja", context)

    if not settings.DEBUG:
        return _render_js(package.output_filename)

    paths = packager.compile(package.paths)
    templates = packager.pack_templates(package)
    tags = [_render_js(js) for js in paths]

    if templates:
        tags.append(_render_inline(templates))

    return '\n'.join(tags)



