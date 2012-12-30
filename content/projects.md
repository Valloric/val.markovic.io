---
title: Projects
extends: base.j2
default_block: markdown_content
summary: "Various projects (past and present) of Val Markovic, creator of
          squishy bits made of software."
---

Projects
========

I contribute to various open-source projects in my spare time as can be seen
from my [GitHub profile][ghprof].

This page displays a list of some of the projects that I have personally
created, in mostly random order.

[Sigil][sigil]
--------------

Sigil started as an open-source, cross-platform WYSIWYG editor for ebooks in the
EPUB format and pretty much grew to a full EPUB IDE. It became incredibly
popular and by the time I left the project it had reached 40 _thousand_
downloads a month (all platforms combined).

This was written in C++ using the [Qt Framework][qt]; Sigil works on Windows,
Mac and Linux.

This was my first really big project.[^big] I started it while I was still in
college and worked on it almost full-time for two years.[^gpa] By mid-2011, I
had been working 12-14 hours a day for nearly two years and reached the point of
_massive_ burn-out. I learned a valuable lesson here, and these days I make damn
sure to work reasonable hours and get plenty of rest.

I transitioned Sigil to a new maintainer near the end of 2011 and today I'm not
involved with its development anymore.

[^big]: When I say big, I mean 35k LOC big. And I rewrote it from scratch _twice_.
No, I am not proud of that in the slightest.
[^gpa]: Whilst maintaining a near-flawless GPA. Apparently I enjoy pain.


[FlightCrew][flightcrew]
------------------------

FlightCrew is an open-source EPUB validator. You give it an EPUB file and it
spews out errors and warnings. This was also a big, complicated project
involving tens of thousands of C++ LOC. Also, cross-platform. This time I didn't
have the luxury of the Qt Framework abstracting away platform-specific
differences since I didn't want to burden other users of FlightCrew with such a
large dependency. So the cross-platformnessyness[^word] was achieved through
lots of pain, hardship and [Boost][boost].

[^word]: I am fully aware that this is not a word.

I wrote this for Sigil to power its EPUB validation features.
Also, the only other EPUB validator out there was EpubCheck [which was
crap][crap].

FlightCrew is written as a C++ library and also comes with separate GUI and CLI
clients.

I transitioned FlightCrew to a new maintainer near the end of 2011 and today I'm not
involved with its development anymore.

[MatchTagAlways][mta]
--------------------

A Vim plugin that always highlights the enclosing HTML/XML tags. This is
actually surprisingly difficult to get right if you want to support use-cases
like templating languages and HTML5 syntax where some tags can be left unclosed.

[ListToggle][lt]
-----------------

A fairly simple Vim plugin that provides commands for easy toggling of Vim's
QuickFix and LocationList windows. There's no command in Vim for toggling these
by default.

[ghprof]: https://github.com/Valloric
[mta]: http://valloric.github.com/MatchTagAlways
[lt]: https://github.com/Valloric/ListToggle
[sigil]: http://code.google.com/p/sigil/
[qt]: http://qt.nokia.com/
[flightcrew]: http://code.google.com/p/flightcrew/
[crap]: http://sigildev.blogspot.com/2010/10/introducing-flightcrew-epub-validator.html
[boost]: http://www.boost.org/
