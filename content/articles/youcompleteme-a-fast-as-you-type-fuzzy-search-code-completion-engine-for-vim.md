---
title: "YouCompleteMe, a Fast, As-You-Type, Fuzzy-Search Code Completion Engine
for Vim"
summary: "It has an identifier-based engine that works with every programming
language and a Clang-based engine that provides semantic code completion for
C and C++."
created: !!timestamp '2013-02-04 10:00:00'
---

[YouCompleteMe][ycm] is a fast, as-you-type, fuzzy-search code completion engine
for [Vim][]. It has two completion engines: an identifier-based engine that
works with every programming language and a semantic, [Clang][]-based engine
that provides semantic code completion for C/C++/Objective-C/Objective-C++ (from
now on referred to as "the C-family languages").

![YouCompleteMe GIF demo](http://i.imgur.com/0OP4ood.gif)

Here's an explanation of what happens in the short GIF demo above.

First, realize that **no keyboard shortcuts had to be pressed** to get the list
of completion candidates at any point in the demo. The user just types and the
suggestions pop up by themselves. If the user doesn't find the completion
suggestions relevant and/or just wants to type, he can do so; the completion
engine will not interfere.

When the user sees a useful completion string being offered, he presses the TAB
key to accept it. This inserts the completion string. Repeated presses of the
TAB key cycle through the offered completions.

If the offered completions are not relevant enough, the user can continue typing
to further filter out unwanted completions.

A critical thing to notice is that the completion **filtering is NOT based on
the input being a string prefix of the completion** (but that works too). The
input needs to be a _[subsequence][] match_ of a completion. This is a fancy way
of saying that any input characters need to be present in a completion string in
the order in which they appear in the input. So `abc` is a subsequence of
`xaybgc`, but not of `xbyxaxxc`. After the filter, a complicated sorting system
ranks the completion strings so that the most relevant ones rise to the top of
the menu (so you usually need to press TAB just once).

**All of the above works with any programming language** because of the
identifier-based completion engine. It collects all of the identifiers in the
current file and other files you visit and searches them when you type
(identifiers are put into per-filetype groups).

The demo also shows the semantic engine in use. The current semantic engine
supports only C-family languages. When the user presses `.`, `->` or `::` while
typing in insert mode, the semantic engine is triggered (it can also be
triggered with a keyboard shortcut; see the docs).

The last thing that you can see in the demo is YCM's integration with
[Syntastic][] (the little red X that shows up in the left gutter) if you are
editing a file with semantic engine support. As Clang compiles your file and
detects warnings or errors, they will be piped to Syntastic for display. You
don't need to save your file or press any keyboard shortcut to trigger this, it
"just happens" in the background.

In essence, YCM obsoletes the following Vim plugins because it has all of their
features plus extra:

- clang_complete
- AutoComplPop
- Supertab
- neocomplcache

Why Did You Build This?
-----------------------

Several reasons, but mostly because a long time ago, in a galaxy far, far away I
used to write C# code in Visual Studio. Its IntelliSense engine is a wonder to
behold, and I missed it in Vim. Don't get me wrong, Vim is a much better editor
than VS (that's why I switched to it), but Vim's various built-in code
completion systems are an absolute joke. As in, not-even-funny bad. I'm not
going to press some complicated keyboard shortcut every single time I'm typing
an identifier; no, screw that, the system should trigger _itself_ and
(unobtrusively) _offer_ me completions that I can then either use or ignore.

The awesome Vim community valiantly tries to make the best it can out of the
built-in "omni-completion", but these efforts boil down to putting lipstick on a
pig.

You could say that AutoComplPop (ACP) already offered us this type of completion
auto-triggering as the user types. Fair point, but there are several issues with
that plugin. First, it's dead. Last update was in 2009. Even worse, it's slow.
Last, there's no fuzzy search. I really, _really_ like fuzzy search. Oh, and
there's no semantic completion with ACP.

The plugin that really made me see the viability of the subsequence match
approach was the truly magnificent [Command-T][cmdt] plugin. It does
subsequence-based matching on file paths for easy file opening. This is probably
my favorite Vim plugin, right up there with [EasyMotion][]. I couldn't (and
wouldn't want to) imagine writing code without them.

We also want our completion system to be smart about ranking whatever completion
candidates survive the filtering step. In a perfect world, the candidate you
want is exactly at the top of the menu so you need to press TAB only once. The
whole point of a code completion system is to save you keystrokes and if you
have to cycle through the menu to get to your candidate the point is lost.

Usually, you know exactly _what_ string you want to type, but its long and you
don't want to type 10 characters if 3 plus a TAB will do the same job.

Well, that's _one_ use case for a code completion system. There's another.
That's if you _don't_ actually know what string you want to use. This is the
"API exploration" use case. You might have a vague idea of a function you want
to call, maybe you even called it a few times before, but you can't remember the
full name.

This is where semantic completion comes into play. It allows you to explore what
methods are available on the object you're handling, what functions are
accessible from the scope you're in etc. A really good semantic completion
engine will even help you with the function's parameters.

Oh and we also want our completion system to be lightning-fast. If we're waiting
for it to return a response... well it's hardly doing its job of speeding us up
then, is it?

So, let's see where we are now with requirements for a completion system:

1. Auto-triggers as you type.
2. Uses subsequence-based completion filtering.
3. Uses smart heuristics to intelligently rank whatever candidates survive the
   filtering step.
4. Offers semantic completions.
5. Fast, fast, _fast_!

clang_complete fails everything except #4 (for C-family languages), which it
excels at (it uses libclang, much like YCM). IMO it also fails #5 pretty badly
because it's both slow (lots of Python logic, whereas YCM only uses Python as
glue code) _and_ it blocks the GUI thread (something YCM does its best to
avoid[^gui-block]).

[^gui-block]: But sometimes YCM fails at this because Vim is profoundly
single-threaded and also does not provide an API for plugins to temporarily
return control to Vim's event loop. If such an API existed, plugins could make
sure to return control to the event loop every now and then while something slow
and complicated was being done in the background. But no such API exists. Also,
there's no way to perform a task asynchronously in VimScript. This limitation
forces YCM to block the GUI thread on occasion. But I try really hard to avoid
this whenever possible.

ACP as mentioned fails everything except #1. Neocomplcache can be configured to
provide #1 and it kinda sorta sometimes does a half-decent job at #4. I've used
neocomplcache for over eight months and my frustrations with it directly led to
the decision to build YCM.

SuperTab I have limited experience with, but from what I understand, it does a
half-decent job at #4, much like neocomplcache.

YCM fulfills all of these requirements. #4 is currently only fulfilled for
C-family languages, but YCM has an internal Completer API that is designed so
that completers for other filetypes can easily be implemented and hooked-up to
the rest of the system. A Python semantic completer will probably be built some
time in the future,[^rope] and others can help out with completers for other
languages. In the mean time, there will probably be a "generic" filetype
completer that queries Vim's omni-completion system for completions if a
specific completer has not yet been written. YCM would provide the other
components on top of the results coming from omni-complete. The "generic"
completer hasn't been built yet but it's on the roadmap.

[^rope]: Probably with [Rope][].


Things We Can't Build in Vim yet but Would Like to
--------------------------------------------------

I can't show a box with help text related to the function right next to the
completion menu in Vim. There's just no API for that. libclang can actually
extract doxygen information from function comment blocks, but there's no way to
spawn such a "sub-window" arbitrarily on the screen in Vim.

The best Vim offers is the "preview" window that can show up at the top of the
file.[^preview] YCM supports this, but it's just not the same. Your eyes have to
leave the small area of the screen where you're currently typing and on a 30
inch monitor this is annoying.

[^preview]: To enable this, add `preview` to `completeopt` in your vimrc, like
so: `set completeopt+=preview`.

So no, we can't build the full VS experience. I'll take what I've built so far
though.

Closing Words
-------------

I've been building YCM on-and-off for a year now in my spare time; I'd guess
about 4 months of work went into it. It's not a terribly complicated system to
build, the main causes of slowdowns were bugs in Vim I encountered while
building this. Those were incredibly annoying and put me off the whole thing for
months.

But it's reached a very releasable state. I've been using the identifier
completer for roughly eight months now and the semantic completer for about two
months (with C++ code). In my experience, they're both rock-solid. I've had
co-workers bang on YCM and lots of bugs were fixed as a result; hopefully it
will be pretty stable for a wider audience as well.

Enjoy the plugin and feel free to [report any issues][tracker] you encounter!


[Clang]: http://clang.llvm.org/
[vundle]: https://github.com/gmarik/vundle#about
[pathogen]: https://github.com/tpope/vim-pathogen#pathogenvim
[clang-download]: http://llvm.org/releases/download.html#3.2
[macvim]: http://code.google.com/p/macvim/#Download
[vimrc]: http://vimhelp.appspot.com/starting.txt.html#vimrc
[vim]: http://www.vim.org/
[syntastic]: https://github.com/scrooloose/syntastic
[subsequence]: http://en.wikipedia.org/wiki/Subsequence
[ycm]: http://valloric.github.com/YouCompleteMe/
[cmdt]: https://wincent.com/products/command-t
[easymotion]: https://github.com/Lokaltog/vim-easymotion
[rope]: http://rope.sourceforge.net/
[tracker]: https://github.com/Valloric/YouCompleteMe/issues?state=open
