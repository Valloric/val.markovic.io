---
title: YouCompleteMe as a Server
summary: "Why tie down YCM to Vim? Everyone deserves good code-completion, no
matter which editor they use."
created: !!timestamp '2014-08-04 17:00:00'
---

The [YouCompleteMe][] (YCM) code-completion plugin for Vim has been a resounding
success. It's one of the most popular Vim plugins, if not _the_ most popular
one.[^popular] The main YCM logic is now available as [ycmd][], an independent
HTTP+JSON server. Client plugins for different editors can easily be written.

[^popular]:
    At the time of writing, YCM has ~5300 stars on GitHub. We can search GitHub
    for [all VimScript repositories sorted by stars][vim-plugins]. YCM is not in
    that list because GitHub classifies it as a Python project (most YCM code is
    Python). The only two Vim plugins that can be considered popular enough to
    be in the top 20 and are not mainly written in VimScript are YCM and
    [UltiSnips] (great plugin!) which has ~1000 stars.

    The other items in the search results are (at the time of writing at least):

    1. Neovim, which is a new Vim build, so not a Vim plugin.
    2. Some dotfiles, so not a Vim plugin.
    3. Vundle, which is a plugin _manager_. IMO it shouldn't count since
       installed by itself it's pretty useless.
    4. Solarized, which is a color scheme for many different editors (including
       Vim), so not a plugin.
    5. Janus, which is a Vim plugin distribution, so not a Vim plugin itself.
    6. This is where YCM would be if it were categorized as a VimScript
       repository.

    Not that GitHub stars are some great ranking mechanism by any stretch of the
    imagination, but I don't have a better one.

Work on splitting YCM into a client-server model started about a year ago. [I've
written on this topic before][perf-post]; suffice it to say that the new
architecture brought extra performance, stability and fixes for long-standing
problems.

YCM switched to this new implementation back in October 2013. Ever since then
I've been tweaking ycmd to remove Vim-specific cruftiness so that it's more
generic. I've also added some docs and written the [example
client][example-client] which demonstrates how to talk to ycmd.

Why make the server generic?
----------------------------

I've learned a lot over the last two years since YCM came out. I've integrated
several different semantic engines into YCM, from libclang for C/C++/Objective-C
to Jedi for Python and OmniSharp for C# (more will be added with time). There's
a pretty simple ycmd-internal API for adding semantic support for other
languages. YCM has also moved past code-completion and is now targeting
code-comprehension features like GoTo and integrated diagnostic errors.

Of the things I've learned, an important lesson is that there's a _lot_ of
common ground between languages when it comes to tools that provide semantic
understanding of code. Much infrastructure is built over and over again for no
benefit.

For instance, there are many Vim plugins that provide semantic code-completion
for a specific language (like jedi-vim for Python, OmniSharp for C#, gocode for
Go etc). They _all_ need to have the following, even though some don't:

1. A semantic engine that can provide a list of available function/class names
   for a given location in a source code file.
2. A filtering system that can intelligently remove completion strings that
   aren't relevant.
3. A ranking system that will (hopefully) put the most useful completion
   at the top of the completion menu.
4. Process-level separation between the semantic engines and the editor so that
   engine crashes don't take down everything. Also makes it much harder to block
   the editor's GUI thread.
5. Vim integration that will provide a UI that auto-shows the relevant
   completions.
6. Vim integration for showing diagnostic messages (errors and warnings) that
   undoubtedly arise from their semantic engines.
7. Tons of other stuff too annoying to enumerate.

And then we repeat all of it not just across languages but also across editors
like Emacs and Sublime Text which have entirely different plugins that implement
(or fail to implement) all of the above as well.

This doesn't scale and is a _massive_ waste of effort.

In the above list, _everything but the first point is common infrastructure_.
This isn't a theoretical notion, this is how YCM already works. Integrating a
new semantic engine into ycmd is borderline _trivial_; don't take my word
for it, [take a look at how the Jedi engine for Python is integrated][ycm-jedi].
It's ~120 lines of code and provides both semantic code-completion and GoTo.
_Everything_ else is provided on top of that and is common to all the engines.

With ycmd now a server independent of Vim, a simple client can be written for
any editor; as soon as a new semantic engine is plugged into ycmd, the old
clients _Just Work™_ with it.

This is the point of ycmd: to **sit between the clients written for a specific
editor and the semantic engines written for a specific language** while
providing a simple API on both ends. The semantic engines don't have to worry
about anything beyond "which names are available at this line & column location
in this file," all the common plumbing is built on top of that. The clients on
the other hands don't have to worry about anything beyond "this is the line &
column location in the buffer the user is editing."

So what's ycmd's value-add?
--------------------------

It all comes from the shared infrastructure. Other than simplifying APIs for the
semantic engines and the editor clients, ycmd for instance also has an
identifier-based completion engine that's language-agnostic; it's triggered when
semantic engines aren't needed (more details in [ycmd docs][ycmd-docs]). There's
also smart caching so that the engines aren't queried too often (they can be
slow), a filepath completer, integration with snippet engines like UltiSnips and
the aforementioned completion filtering and ranking (which is neither simple nor
easy to implement right).

In case anyone is worried about the overhead of the client-server architecture,
[I've debunked that myth quite throughly][perf-post] (with benchmarks, no less).
Even better than benchmarks, this has been implemented for YCM and has been
battle-tested over the last 10 months. For a server running on localhost, the
communication overhead is effectively _zilch_.


Conclusion
----------

Let's stop reinventing the wheel.

**For semantic engine writers:** expose your engine as a server that talks
HTTP+JSON if at all possible; don't worry about anything beyond listing
completions at a specific location in the file. Plug the server into ycmd (it's
easy). All ycmd clients instantly work with your engine.

**For editor plugin developers:** implement a client for ycmd. Most code is
already written for you in the [example client][example-client], you just need
to write the editor-specific parts. Hell, since the example code is all licensed
under the [Apache License v2][apache2], you can copy-paste most of it.[^copy]
Enjoy good code-completion and code-comprehension features.

[^copy]: If your editor can be extended with Python. If not, it can certainly
  send HTTP requests. The example client even pretty-prints (and
  syntax-highlights!) the full HTTP chatter between it and ycmd so figuring out
  what's going on should be a piece of cake.


[YouCompleteMe]: http://valloric.github.io/YouCompleteMe/
[ycmd]: https://github.com/Valloric/ycmd
[example-client]: https://github.com/Valloric/ycmd/tree/master/examples/example_client.py
[example-readme]: https://github.com/Valloric/ycmd/blob/master/examples/README.md
[UltiSnips]: https://github.com/SirVer/ultisnips
[vim-plugins]: https://github.com/search?q=stars%3A%3E1&type=Repositories&ref=advsearch&l=VimL
[perf-post]: https://plus.google.com/u/1/+StrahinjaMarkovi%C4%87/posts/Zmr5uf2jCHm
[ycm-jedi]: https://github.com/Valloric/ycmd/blob/master/ycmd/completers/python/jedi_completer.py
[ycmd-docs]: https://github.com/Valloric/ycmd/blob/master/README.md
[apache2]: http://www.apache.org/licenses/LICENSE-2.0.html

