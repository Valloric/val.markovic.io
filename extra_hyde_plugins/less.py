# -*- coding: utf-8 -*-
"""
Less css plugin
"""

from hyde.plugin import CLTransformer
from fswrap import File

import re
import subprocess


class LessCSSPlugin(CLTransformer):
    """
    The plugin class for less css
    """

    def __init__(self, site):
        super(LessCSSPlugin, self).__init__(site)

    @property
    def executable_name(self):
        return "lessc"

    def _should_parse_resource(self, resource):
        """
        Check user defined
        """
        try:
          return getattr(resource, 'meta', {}).get('parse', True)
        except AttributeError:
          return True

    def _should_replace_imports(self, resource):
        try:
          return getattr(resource, 'meta', {}).get('uses_template', True)
        except AttributeError:
          return True

    def begin_site(self):
        """
        Find all the less css files and set their relative deploy path.
        """
        for resource in self.site.content.walk_resources():
            if resource.source_file.kind == 'less' and \
                self._should_parse_resource(resource):
                new_name = resource.source_file.name_without_extension + ".css"
                target_folder = File(resource.relative_deploy_path).parent
                resource.relative_deploy_path = target_folder.child(new_name)

    def begin_text_resource(self, resource, text):
        """
        Replace @import statements with {% include %} statements.
        """

        if not resource.source_file.kind == 'less' or not \
            self._should_parse_resource(resource) or not \
            self._should_replace_imports(resource):
            return text

        import_finder = re.compile(
                            '^\\s*@import(-once)?\s+(?:\'|\")([^\'\"]*)(?:\'|\")\s*\;\s*$',
                            re.MULTILINE)

        # set of file paths that have already been included
        already_imported = set()

        def import_to_include(match):
            if not match.lastindex:
                return ''

            path = match.groups(1)[1]
            afile = File(resource.source_file.parent.child(path))
            if len(afile.kind.strip()) == 0:
                afile = File(afile.path + '.less')

            has_once = bool(match.groups()[0])
            if has_once and afile.path in already_imported:
              return ""

            ref = self.site.content.resource_from_path(afile.path)
            if not ref:
                raise self.template.exception_class(
                        "Cannot import from path [%s]" % afile.path)
            ref.is_processable = False
            already_imported.add( afile.path )
            return self.template.get_include_statement(ref.relative_path)
        text = import_finder.sub(import_to_include, text)
        return text


    @property
    def plugin_name(self):
        """
        The name of the plugin.
        """
        return "less"

    def text_resource_complete(self, resource, text):
        """
        Save the file to a temporary place and run less compiler.
        Read the generated file and return the text as output.
        Set the target path to have a css extension.
        """
        if not resource.source_file.kind == 'less' or not \
            self._should_parse_resource(resource):
            return

        supported = [
            "verbose",
            ("silent", "s"),
            ("compress", "x"),
            "O0",
            "O1",
            "O2",
            "include-path="
        ]

        less = self.app
        source = File.make_temp(text)
        target = File.make_temp('')
        args = [unicode(less)]
        args.extend(self.process_args(supported))
        args.extend([unicode(source), unicode(target)])
        try:
            self.call_app(args)
        except subprocess.CalledProcessError:
             raise self.template.exception_class(
                    "Cannot process %s. Error occurred when "
                    "processing [%s]" % (self.app.name, resource.source_file))
        return target.read_all()
