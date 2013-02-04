#!/usr/bin/env python
#
# Copyright (c) 2012, Val Markovic
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#    * Neither the name of the author nor the names of its contributors
#      may be used to endorse or promote products derived from this
#      software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Runs pygments on <code></code> blocks. Supports having the code language as a
class on the <code> block, eg. <code class="python"></code>.

Requires pygments, obviously.
"""

from hyde.plugin import Plugin

import re
import pygments
import HTMLParser
from pygments import lexers
from pygments import formatters


class PygmentsPlugin( Plugin ):
  """
  """

  def __init__( self, site ):
    super( PygmentsPlugin, self ).__init__( site )
    self.pattern = re.compile(
      r"""<code
          (?:     # either a <code> or <code class="foo"> tag
            \s*
            |
            (?:
              .*?                  # other things can precede the class
              class\s*=\s*"(.*?)"  # this will capture the class name
              .*?                  # other things can follow the class
            )
          )
          >
          (.*?)   # the actual content of the element
          </code>""",
      re.VERBOSE | re.DOTALL )
    self.html_parser = HTMLParser.HTMLParser()


  def text_resource_complete( self, resource, text ):
    """
    """
    if not resource.source_file.is_text:
      return

    def replace_func( match_object ):
      language = match_object.group( 1 )
      content = match_object.group( 2 )
      # We need to unescape the content first because it's already escaped, and
      # Pygments will escape it too, and we don't want it to be double-escaped.
      raw_content = self.html_parser.unescape( content )
      lexer = ( lexers.get_lexer_by_name( language ) if language else
                lexers.guess_lexer( raw_content ) )

      formatter = formatters.HtmlFormatter( nowrap=True )
      highlighted_code = pygments.highlight( raw_content, lexer, formatter )
      return '<code class="{0}">{1}</code>'.format( language,
                                                    highlighted_code.strip() )

    return re.sub( self.pattern, replace_func, text )
