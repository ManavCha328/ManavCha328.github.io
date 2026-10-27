/* Manav Chandaka · portfolio behaviour. No dependencies; every page works
   without this script (links open images directly, videos keep controls). */
(function(){
  'use strict';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- links from the old single-page site (#project/<slug>) ----------
  var old = location.hash.match(/^#project\/([\w-]+)$/);
  if (old && document.body.hasAttribute('data-home')) {
    location.replace('projects/' + old[1] + '.html');
    return;
  }

  // ---------- mobile menu ----------
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    function setMenu(open){
      nav.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    menuBtn.addEventListener('click', function(){ setMenu(!nav.classList.contains('open')); });
    nav.addEventListener('click', function(e){ if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') setMenu(false); });
  }

  // ---------- muted preview loops: play only while on screen, one frame at a
  // time (clips sharing a frame play together), never under reduced motion
  // (the poster frame stays instead) ----------
  var loops = Array.prototype.slice.call(document.querySelectorAll('video[data-loop]'));
  if (loops.length && !reduceMotion && 'IntersectionObserver' in window) {
    var visible = new Map();
    var playing = null;
    function groupOf(v){ return v.closest('.feature-media') || v; }
    function clipsIn(g){ return g.tagName === 'VIDEO' ? [g] : Array.prototype.slice.call(g.querySelectorAll('video[data-loop]')); }
    function pick(){
      var best = null, bestRatio = 0;
      visible.forEach(function(r, v){ if (r > bestRatio) { best = groupOf(v); bestRatio = r; } });
      if (playing && playing !== best) clipsIn(playing).forEach(function(v){ v.pause(); });
      if (best) clipsIn(best).forEach(function(v){
        if (!v.paused) return;
        var p = v.play();
        if (p && p.catch) p.catch(function(){});
      });
      playing = best;
    }
    var vo = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting && e.intersectionRatio >= 0.5) visible.set(e.target, e.intersectionRatio);
        else visible.delete(e.target);
      });
      pick();
    }, { threshold:[0, 0.5, 0.75, 1] });
    loops.forEach(function(v){
      v.muted = true;
      if (v.preload === 'none') v.preload = 'metadata';
      vo.observe(v);
    });
    document.addEventListener('visibilitychange', function(){
      if (document.hidden && playing) clipsIn(playing).forEach(function(v){ v.pause(); }); else pick();
    });
  }
  // A video the visitor starts pauses every other video on the page.
  document.addEventListener('play', function(e){
    if (e.target.hasAttribute('data-loop')) return;
    document.querySelectorAll('video').forEach(function(v){ if (v !== e.target) v.pause(); });
  }, true);

  // ---------- annotated images: legend and pins highlight together ----------
  document.querySelectorAll('.m-anno').forEach(function(block){
    var pins = block.querySelectorAll('.pin');
    var items = block.querySelectorAll('.legend li');
    function on(i, state){
      if (pins[i]) pins[i].classList.toggle('on', state);
      if (items[i]) items[i].classList.toggle('on', state);
    }
    items.forEach(function(li, i){
      li.addEventListener('mouseenter', function(){ on(i, true); });
      li.addEventListener('mouseleave', function(){ on(i, false); });
    });
    pins.forEach(function(p, i){
      p.addEventListener('mouseenter', function(){ on(i, true); });
      p.addEventListener('mouseleave', function(){ on(i, false); });
    });
  });

  // ---------- streaming video facade: the third-party player only loads
  // when someone asks for it ----------
  document.querySelectorAll('.stream[data-embed]').forEach(function(box){
    var btn = box.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function(){
      var f = document.createElement('iframe');
      f.src = box.getAttribute('data-embed');
      f.title = box.getAttribute('data-title') || 'Video';
      f.allow = 'autoplay; fullscreen';
      f.setAttribute('allowfullscreen', '');
      box.innerHTML = '';
      box.appendChild(f);
    });
  });

  // ---------- lightbox: every a.lb on the page forms one browsable set ----------
  var links = Array.prototype.slice.call(document.querySelectorAll('a.lb'));
  var dlg = document.getElementById('lightbox');
  if (links.length && dlg && typeof dlg.showModal === 'function') {
    var img = dlg.querySelector('.lb-img-wrap img');
    var cap = dlg.querySelector('.lb-cap');
    var count = dlg.querySelector('.lb-count');
    var cur = 0, opener = null;
    function captionFor(a){
      if (a.getAttribute('data-cap')) return a.getAttribute('data-cap');
      var fig = a.closest('figure');
      var fc = fig && fig.querySelector('figcaption');
      if (fc) return fc.textContent.trim();
      var im = a.querySelector('img');
      return im ? im.alt : '';
    }
    function show(i){
      cur = (i + links.length) % links.length;
      var a = links[cur];
      var im = a.querySelector('img');
      img.src = a.getAttribute('href');
      img.alt = im ? im.alt : '';
      cap.textContent = captionFor(a);
      count.textContent = (cur + 1) + ' / ' + links.length;
    }
    function open(i, from){
      opener = from || null;
      dlg.classList.toggle('single', links.length < 2);
      show(i);
      dlg.showModal();
      document.documentElement.style.overflow = 'hidden';
    }
    function close(){ if (dlg.open) dlg.close(); }
    dlg.addEventListener('close', function(){
      document.documentElement.style.overflow = '';
      img.removeAttribute('src');
      if (opener) opener.focus();
    });
    links.forEach(function(a, i){
      a.addEventListener('click', function(e){
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
        e.preventDefault();
        open(i, a);
      });
    });
    dlg.querySelector('.lb-close').addEventListener('click', close);
    dlg.querySelector('.lb-prev').addEventListener('click', function(){ show(cur - 1); });
    dlg.querySelector('.lb-next').addEventListener('click', function(){ show(cur + 1); });
    dlg.addEventListener('click', function(e){
      if (e.target === dlg || e.target.classList.contains('lb-img-wrap') || e.target.classList.contains('lb-stage')) close();
    });
    dlg.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
    });
    var tx = null;
    dlg.addEventListener('touchstart', function(e){ tx = e.changedTouches[0].clientX; }, { passive:true });
    dlg.addEventListener('touchend', function(e){
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx; tx = null;
      if (Math.abs(dx) > 50) show(dx < 0 ? cur + 1 : cur - 1);
    }, { passive:true });
  }

  // ---------- homepage slideshow: arrows, dots, swipe; auto-advances every
  // 5 s except under reduced motion, pausing on hover, focus, or a hidden tab ----------
  var show = document.getElementById('hero-slides');
  if (show) {
    var slides = Array.prototype.slice.call(show.querySelectorAll('.slide'));
    var dotsBox = document.querySelector('.show-dots');
    var dots = [], cur = 0, timer = null;
    function go(i){
      cur = (i + slides.length) % slides.length;
      slides.forEach(function(s, j){
        var on = j === cur;
        s.classList.toggle('on', on);
        if (on) { s.removeAttribute('aria-hidden'); s.removeAttribute('tabindex'); }
        else { s.setAttribute('aria-hidden', 'true'); s.setAttribute('tabindex', '-1'); }
      });
      // Warm the next slide's image so the crossfade never shows a blank frame.
      var nx = slides[(cur + 1) % slides.length].querySelector('img');
      if (nx) nx.loading = 'eager';
      dots.forEach(function(d, j){ d.setAttribute('aria-pressed', j === cur ? 'true' : 'false'); });
    }
    function start(){ if (!reduceMotion && !timer) timer = setInterval(function(){ go(cur + 1); }, 5000); }
    function stop(){ clearInterval(timer); timer = null; }
    function restart(){ stop(); start(); }
    slides.forEach(function(s, i){
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Show slide ' + (i + 1) + ' of ' + slides.length);
      b.addEventListener('click', function(){ go(i); restart(); });
      dotsBox.appendChild(b);
      dots.push(b);
    });
    show.querySelector('.show-arrow.prev').addEventListener('click', function(){ go(cur - 1); restart(); });
    show.querySelector('.show-arrow.next').addEventListener('click', function(){ go(cur + 1); restart(); });
    show.addEventListener('mouseenter', stop);
    show.addEventListener('mouseleave', start);
    show.addEventListener('focusin', stop);
    show.addEventListener('focusout', start);
    var sx = null;
    show.addEventListener('touchstart', function(e){ sx = e.changedTouches[0].clientX; stop(); }, { passive:true });
    show.addEventListener('touchend', function(e){
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 48) { e.preventDefault(); go(dx < 0 ? cur + 1 : cur - 1); }
      start();
    }, { passive:false });
    document.addEventListener('visibilitychange', function(){ if (document.hidden) stop(); else start(); });
    go(0);
    start();
  }

  // ---------- About: read more ----------
  var aboutBtn = document.getElementById('about-toggle');
  var aboutMore = document.getElementById('about-more');
  if (aboutBtn && aboutMore) {
    aboutBtn.addEventListener('click', function(){
      var open = aboutMore.hidden;
      aboutMore.hidden = !open;
      aboutBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      aboutBtn.textContent = open ? 'Read less' : 'Read more';
    });
  }

  // ---------- case studies: highlight the section in view in the sticky bar ----------
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var tocBar = document.querySelector('.toc');
    var to = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        tocLinks.forEach(function(a){
          var on = a.getAttribute('href') === '#' + e.target.id;
          a.classList.toggle('on', on);
          if (on && tocBar) tocBar.scrollTo({ left: a.offsetLeft - 16, behavior: reduceMotion ? 'auto' : 'smooth' });
        });
      });
    }, { rootMargin:'-30% 0px -60% 0px' });
    tocLinks.forEach(function(a){
      var sec = document.getElementById(a.getAttribute('href').slice(1));
      if (sec) to.observe(sec);
    });
  }

  // ---------- homepage: mark the nav link for the section in view ----------
  if (document.body.hasAttribute('data-home') && 'IntersectionObserver' in window) {
    var navLinks = document.querySelectorAll('.site-nav a[href^="#"]');
    var so = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        navLinks.forEach(function(a){
          if (a.getAttribute('href') === '#' + e.target.id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin:'-45% 0px -50% 0px' });
    ['work','experience','about','contact'].forEach(function(id){
      var el = document.getElementById(id);
      if (el) so.observe(el);
    });
  }
})();
