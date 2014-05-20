---
title: A Vim Plugin That Always Highlights the Enclosing Tags
summary: "Always knowing what element you are in when editing HTML or XML is
very useful. Other Vim plugins highlight the other tag only when the cursor is
inside the angle brackets."
created: !!timestamp '2012-09-12 10:00:00'
---

Just recently I started editing HTML much more than I usually do[^html] and I
noticed Vim was missing an awesome feature Notepad++ had. The last time I used
Notepad++ was many years ago, but I still remember it used to highlight the
other tag in the pair when your cursor was inside one of them.

[^html]: I write it in bursts, but day-to-day I mostly write C++ or Python.

_[For those who want to skip to the end, the plugin I built is called
[MatchTagAlways][mta].]_

Sure enough, I wasn't [the only one][so] who noticed that Vim was missing this
awesome feature. [A kind soul][greg] even took it upon himself to implement said
missing functionality as [a Vim plugin][mt] that does exactly what it says on
the tin, and does it well.

But you know what? I want _more_ than that.

I don't want Vim to "just" highlight the other tag in the pair when my cursor is
inside the tag, I want it to _always_ highlight the tags that enclose the
cursor. I've seen Sublime Text 2 trying to point out the enclosing tags with a
dotted line, but I've also seen it fail in the face of unclosed tags common in
HTML5 syntax.[^tags]

[^tags]: Not that I'm saying that you should actually write code like this. I
always close my tags (even in HTML5), but not everyone does and sometimes I need
to edit that code.

Here's an animated GIF of what I'm talking about:

![MatchTagAlways screen shot](http://i.imgur.com/qAf0N.gif)

Do you see how the enclosing tags are always highlighted, even when you are
inside the element's content? That's what I wanted.

So I wrote a plugin that does it. The GIF you just saw is [MatchTagAlways][mta]
in action. It's plug & play, comes with sane defaults and should require no
configuration (although there are knobs to tweak if you want to do that).

Implementing this is actually surprisingly tricky to get right if you want to
support use-cases like templating languages and the aforementioned HTML5 syntax.
There's a ridiculous number of corner cases to handle, and MTA implements far
too much of an HTML parser for my liking.[^regex]

[^regex]: Quite a bit of it with regular expressions. Yes, I know, [I'm going to
hell][soreg]. But it still works in 99.99% of the use-cases and fuck me if I'm
going to write an _actual_ HTML parser that works from the "inside out"[^inout]
just for this, because that's what I need and it doesn't exist.

[^inout]: By "inside out" I mean it starts from a specific line and column
number and parses up and down. No, you can't use a "normal" parser. MTA only
looks at the HTML code that is on the screen for the sake of performance and
that won't parse sensibly with a normal parser, especially when you throw in the
"has to work with templates" requirement. No, not even Beautiful Soup.  Yes,
I've tried. The current solution is pretty damn robust.

Anyway, use it if you edit HTML or XML if this looks like a feature you'd like
to have. Note that your copy of Vim needs to come with Python support. More
details can be found in the plugin's docs.


[mta]: http://valloric.github.com/MatchTagAlways
[so]: http://stackoverflow.com/questions/8168320/can-vim-highlight-matching-html-tags-like-notepad
[greg]: http://www.gregsexton.org/
[mt]: https://github.com/gregsexton/MatchTag#readme
[soreg]: http://stackoverflow.com/a/1732454/146752
