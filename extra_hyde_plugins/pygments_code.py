"""
Runs pygments on <code></code> blocks. Supports having the code language as a
class on the <code> block, eg. <code class="python"></code>.

Requires pygments, obviously.
"""

from hyde.plugin import Plugin

import re
import pygments
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

  def text_resource_complete( self, resource, text ):
    """
    """
    if not resource.source_file.is_text:
      return

    def replace_func( match_object ):
      language = match_object.group( 1 )
      content = match_object.group( 2 )
      lexer = ( lexers.get_lexer_by_name( language ) if language else
                lexers.guess_lexer( content ) )

      formatter = formatters.HtmlFormatter( nowrap=True )
      highlighted_code = pygments.highlight( content, lexer, formatter )
      return '<code class="{0}">{1}</code>'.format( language,
                                                    highlighted_code )

    return re.sub( self.pattern, replace_func, text )
