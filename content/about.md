---
title: About
extends: base.j2
default_block: markdown_content
---

About
=====

<section itemscope="" itemtype="http://data-vocabulary.org/Person">
  <img itemprop="image"
       id="headshot"
       src="{{ media_url('img/headshot.jpg') }}"
       alt="headshot" />
  <p>Hi, my name is
  <span itemprop="name">Strahinja <span itemprop="nickname">Val</span>
  Markovic</span> and I am a <span itemprop="title">Software Engineer</span>
  at <span itemprop="worksFor"><span itemprop="affiliation">Google</span></span>
  in the Search Quality division (roughly, the "Google Search" part). No, I
  can't make your website rank better.</p>

  <p>I grew up in Zagreb, Croatia and got my BS and MS
  (<em>magna cum laude</em>) in Computer Science from the
  <span itemprop="alumniOf">University of Zagreb,
  Faculty of Electrical Engineering and Computing</span>.</p>

  <p>I'm currently enjoying life in the heart of sunny Silicon Valley. I
  contribute to various <a href="{{ content_url('/projects') }}">open source
    projects</a> in my spare time and I've even started a few myself.</p>

  <p>If you need to contact me,
  <a href="mailto:val@markovic.io" itemprop="email" >email</a> is
  probably the best way to do it.</p>
</section>
