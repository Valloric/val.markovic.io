---
title: "Picture Commander: Choose Images for Remote Screens"
summary: "Choose an image from a gallery on one device and have it automatically
pushed to a remote device screen."
created: !!timestamp '2014-11-08 22:00:00'
---

[Picture Commander][pc-github] provides a way to select an image from a gallery
on one device and have that image automatically displayed on the screen of a
remote device. No fancy apps are necessary, this is completely implemented with
modern web technology (hooray for [Server-Sent Events][sse]). All you need is a
browser.

[![Picture Commander screenshot](//i.imgur.com/VHwKSt0l.png)](//i.imgur.com/VHwKSt0.png)

The way it works is the following: there's one "admin" view (`/gallery` handler)
and one "display" view (`/viewer` handler). Clicking on images in the gallery
automatically replaces the displayed image on viewer screens (no page refresh
needed). You provide a path to an image folder on server startup. The server
will recursively collect all images in that folder hierarchy and present them in
the gallery.

This is super-useful when projecting one browser tab to a different screen with
say a [Chromecast][] since the gallery tab can then control the projected one. You
can also have multiple viewer devices/browsers connected at the same time and
they'll all be updated.

Example of running the server:

```bash
./server.py --images_folder=./test_images --port=8080 --host=localhost
```

Then go to [`http://localhost:8080/gallery`](http://localhost:8080/gallery) for
the admin view and to
[`http://localhost:8080/viewer`](http://localhost:8080/viewer) for the viewer
page. Tested with latest Chrome, Firefox and Safari across desktop, Nexus 5/7/9
and iPad.

I need this for running my local _Dungeons & Dragons_ game; as a DM, I want to
show the players pictures of maps, characters and other stuff without exposing
filenames or thumbnails of pictures that they aren't supposed to see yet. I was
surprised to find that there was no simple and easy way to do this so I wrote
Picture Commander.

Picture Commander is free and open-source under the [Apache v2
License][apache2]. Enjoy!

[pc-github]: https://github.com/Valloric/picture-commander
[apache2]: http://www.apache.org/licenses/LICENSE-2.0.html
[sse]: http://dev.w3.org/html5/eventsource/
[chromecast]: http://www.google.com/chrome/devices/chromecast/
