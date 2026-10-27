"""Builds index.html and projects/*.html from tools/content.py.

    python tools/build.py

The generated HTML is committed, so GitHub Pages serves plain static files.
Needs Pillow (only to read image sizes for width/height attributes).
Set SHOW_PLACEHOLDERS = False to hide "media pending" boxes.
"""
import os, sys, html
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content import PROJECTS, ALT, BENCH, EXPERIENCE, SKILLS, SLIDES  # noqa: E402

SHOW_PLACEHOLDERS = True
SITE = 'https://manavcha328.github.io/'
EMAIL = 'manavcha328@gmail.com'
FEATURE_ORDER = ['climbing-robot', 'lekiwi', 'ti-showerhead', 'terratrek']
PHONE = '(630) 310-1851'
PHONE_TEL = '+16303101851'
LINKEDIN = 'https://www.linkedin.com/in/manavchandaka/'
GITHUB = 'https://github.com/SIGRobotics-UIUC/LeKiwi'
RESUME = 'assets/Manav_Chandaka_Resume.pdf'
FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap'

_dims = {}
def dims(name):
    if name not in _dims:
        with Image.open(os.path.join(ROOT, 'assets', 'img', name + '.webp')) as im:
            _dims[name] = im.size
    return _dims[name]

def esc(s):
    return html.escape(s, quote=True)

def strip_tags(s):
    import re
    return html.unescape(re.sub(r'<[^>]+>', '', s))

ARROW = '<span class="ar" aria-hidden="true">→</span>'
EXT = '<span aria-hidden="true">↗</span>'

def img(r, name, cls='', eager=False, sizes=None, alt=None):
    w, h = dims(name)
    a = ALT.get(name, '') if alt is None else alt
    attrs = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img src="{r}assets/img/{name}.webp" width="{w}" height="{h}" alt="{esc(a)}"{attrs}{load} decoding="async" />'

def lb(r, name, inner, cap=''):
    c = f' data-cap="{esc(strip_tags(cap))}"' if cap else ''
    return f'<a class="lb" href="{r}assets/img/{name}.webp"{c}>{inner}</a>'

# --------------------------------------------------------------------------- shell
def head(r, title, desc, canonical, og_image='assets/img/og-card.jpg'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<!-- Kept out of search results by choice: anyone with the link can view the site. Remove this line to allow indexing. -->
<meta name="robots" content="noindex, nofollow" />
<link rel="canonical" href="{SITE}{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{SITE}{canonical}" />
<meta property="og:image" content="{SITE}{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#f4f4f1" media="(prefers-color-scheme: light)" />
<meta name="theme-color" content="#0e0f11" media="(prefers-color-scheme: dark)" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%23111315'/%3E%3Cpath d='M7 23V9h3l6 8 6-8h3v14h-3v-9l-6 8-6-8v9z' fill='%23f4f4f1'/%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="{FONTS}" />
<link rel="stylesheet" href="{r}assets/css/site.css" />
'''

def header(r, home):
    h = '' if home else f'{r}index.html'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{r}index.html"><span class="brand-name">Manav Chandaka</span></a>
    <button type="button" class="menu-btn" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"></span>Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="{h}#work"{'' if home else ' aria-current="true"'}>Work</a>
      <a href="{h}#experience">Experience</a>
      <a href="{h}#about">About</a>
      <a href="{h}#contact">Contact</a>
      <a class="btn btn-sm" href="{r}{RESUME}" target="_blank" rel="noopener">Résumé</a>
    </nav>
  </div>
</header>
'''

LIGHTBOX = '''<dialog class="lightbox" id="lightbox" aria-label="Image viewer">
  <div class="lb-stage">
    <div class="lb-top"><span class="lb-count"></span><button type="button" class="lb-btn lb-close" aria-label="Close viewer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
    <div class="lb-img-wrap">
      <button type="button" class="lb-btn lb-prev" aria-label="Previous image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
      <img alt="" />
      <button type="button" class="lb-btn lb-next" aria-label="Next image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
    </div>
    <p class="lb-cap"></p>
  </div>
</dialog>
'''

def footer(r, dark=False):
    return f'''<footer class="site-footer">
  <div class="wrap foot">
    <span>© 2026 Manav Chandaka</span>
    <span class="sp"></span>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    <a href="{GITHUB}" target="_blank" rel="noopener nofollow">GitHub</a>
    <a href="{r}{RESUME}" target="_blank" rel="noopener">Résumé</a>
  </div>
</footer>
{LIGHTBOX}<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
'''

def metric_value(v, unit):
    if unit == 'word':
        return esc(v)
    return f'{v}<span>{esc(unit)}</span>' if unit else v

# --------------------------------------------------------------------------- homepage
def feature_media(p, r):
    s = p['slug']
    if s == 'lekiwi':
        # The portrait demo clip fills the frame's height, uncropped, over a
        # blurred copy of its own poster frame.
        poster = f'{r}assets/img/lekiwi-loop-poster.webp'
        return (f'<div class="feature-media video-fill"><span class="vf-bg" style="background-image:url({poster})" aria-hidden="true"></span><span class="badge live">Real-time demo</span>'
                f'<video data-loop muted loop playsinline preload="none" poster="{poster}" '
                f'aria-label="LeKiwi V2 driving up to an object and picking it up"><source src="{r}assets/video/lekiwi-loop.mp4" type="video/mp4" /></video></div>')
    if s == 'terratrek':
        # The CAD walking over the stairs beside the real leg being cranked.
        return (f'<div class="feature-media"><span class="badge live">CAD vs. hardware</span><div class="split cad-hw">'
                f'<video data-loop muted loop playsinline preload="none" poster="{r}assets/img/terratrek-cad-walk-poster.webp" '
                f'aria-label="CAD animation of TerraTrek stepping over the stair rack"><source src="{r}assets/video/terratrek-cad-walk.mp4" type="video/mp4" /></video>'
                f'<video data-loop muted loop playsinline preload="none" poster="{r}assets/img/terratrek-gait-poster.webp" '
                f'aria-label="TerraTrek leg linkage stepping as the crank is turned by hand"><source src="{r}assets/video/terratrek-gait.mp4" type="video/mp4" /></video>'
                f'</div></div>')
    badge = f'<span class="badge">{p["tile_badge"]}</span>' if p.get('tile_badge') else ''
    if s == 'climbing-robot':
        # The robot beside its chain drive running: suction cups riding the track.
        return (f'<div class="feature-media"><span class="badge live">Chain drive running</span><div class="split photo-clip">'
                f'{img(r, "climber-robot")}'
                f'<video data-loop muted loop playsinline preload="none" poster="{r}assets/img/climber-chain-drive-poster.webp" '
                f'aria-label="Top view of the climbing robot chain drive carrying the suction cups around"><source src="{r}assets/video/climber-chain-drive.mp4" type="video/mp4" /></video>'
                f'</div></div>')
    return f'<div class="feature-media">{badge}{img(r, p["tile"])}</div>'

def build_index():
    r = ''
    # Strongest verified outcomes first; case-study pages keep content.py order.
    rank = {s: i for i, s in enumerate(FEATURE_ORDER)}
    feats = sorted((p for p in PROJECTS if p['featured']), key=lambda p: rank.get(p['slug'], 99))
    others = [p for p in PROJECTS if not p['featured'] and not p.get('hidden')]
    o = [head(r, 'Manav Chandaka · Mechanical Engineering & Robotics Hardware',
              'Manav Chandaka: UIUC mechanical engineering student who designs, builds, and tests robot hardware. Suction climbing robot research, the LeKiwi open-source mobile manipulator, and Texas Instruments equipment engineering.',
              ''),
         '</head>\n<body data-home>\n', header(r, True), '<main id="main">\n']
    # hero: photo, name, links and facts beside the About text, then the project slideshow
    slides = ''.join(
        f'<a class="slide{" on" if i == 0 else ""}" href="projects/{slug}.html"{"" if i == 0 else " aria-hidden=\"true\" tabindex=\"-1\""}>'
        + (f'<span class="slide-bg" style="background-image:url({r}assets/img/{name}.webp)" aria-hidden="true"></span>' if contain else '')
        + f'{img(r, name, "contain" if contain else "", eager=(i == 0))}'
        f'<span class="slide-cap"><span class="t">{esc(t)}</span><span class="s">{esc(sub)}</span></span></a>'
        for i, (slug, name, contain, t, sub) in enumerate(SLIDES))
    o.append(f"""<section class="hero" aria-label="Introduction">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {img(r, 'headshot-sm', 'pfp-lg', eager=True, alt='Portrait of Manav Chandaka')}
      <h1 class="hero-name">Manav<br />Chandaka</h1>
      <div class="hero-actions">
        <a class="btn primary" href="#work">See the work</a>
        <a class="btn" href="{RESUME}" target="_blank" rel="noopener">Résumé (PDF)</a>
        <a class="btn" href="mailto:{EMAIL}">Email me</a>
        <a class="btn" href="tel:{PHONE_TEL}" aria-label="Phone: {PHONE}" title="{PHONE}">Phone</a>
      </div>
      <p class="facts"><span><b>UIUC</b> Mechanical Engineering · CS minor</span><span><b>Expected graduation:</b> December 2027</span></p>
    </div>
    <section id="about" class="hero-about" aria-labelledby="about-h">
      <h2 id="about-h">About</h2>
      <p class="updated">Last updated: October 2026</p>
      <p>I am a mechanical engineering student at the University of Illinois Urbana-Champaign (UIUC), with a minor in computer science. My interests are robotics hardware, CAD, and building and testing physical prototypes. I expect to graduate in December 2027.</p>
      <div id="about-more" hidden>
        <p>I do undergraduate research in UIUC’s Novel Mobile Robots Lab, where I work on a suction climbing robot for inspecting aircraft skins. I’m also the executive chair of SIGRobotics, a robotics club under ACM@UIUC. Leading the club has been one of my favorite parts of college. It’s where I designed LeKiwi, an open-source mobile manipulator that now has 100s of community builds.</p>
        <p>Last summer, I was an equipment engineering intern at Texas Instruments, where I designed tooling for semiconductor fab equipment. Two of those designs were filed as patent applications.</p>
        <p>Feel free to contact me by email (<a class="ext" href="mailto:{EMAIL}">{EMAIL}</a>), phone (<a class="ext" href="tel:{PHONE_TEL}">{PHONE}</a>), or through <a class="ext" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>, <a class="ext" href="{GITHUB}" target="_blank" rel="noopener nofollow">GitHub</a>, or my <a class="ext" href="{RESUME}" target="_blank" rel="noopener">résumé</a>. My full project deck is on <a class="ext" href="https://www.canva.com/design/DAGuM3NbWBQ/75xrgGBHBqUiWjThlxlV5A/view?utm_content=DAGuM3NbWBQ&amp;utm_campaign=designshare&amp;utm_medium=link2&amp;utm_source=uniquelinks&amp;utlId=ha6b7d31971" target="_blank" rel="noopener">Canva</a>.</p>
      </div>
      <button type="button" class="btn btn-sm" id="about-toggle" aria-expanded="false" aria-controls="about-more">Read more</button>
    </section>
  </div>
  <div class="wrap">
    <figure class="hero-show">
      <div class="show-frame" id="hero-slides">
        {slides}
        <button type="button" class="show-arrow prev" aria-label="Previous slide"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button type="button" class="show-arrow next" aria-label="Next slide"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="show-dots" role="group" aria-label="Choose slide"></div>
    </figure>
  </div>
</section>
""")
    # featured
    o.append('''<section class="section" id="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="work-h">Selected work</h2></div>
    <div class="features">
''')
    for i, p in enumerate(feats):
        mets = ''.join(f'<div><dt>{esc(l)}</dt><dd>{esc(v)}</dd></div>' for v, l in p.get('home_metrics', []))
        mets = f'<dl class="metrics">{mets}</dl>' if mets else ''
        role = p['facts'][0][1].split('.')[0]
        when = dict(p['facts']).get('Timeline', '')
        o.append(f'''      <article class="feature{' flip' if i % 2 else ''}">
        <a class="feature-link" href="projects/{p['slug']}.html">
          {feature_media(p, r)}
          <div class="feature-body">
            <p class="feature-idx"><b>{i+1:02d}</b><span>{esc(p['area'])}</span></p>
            <h3 class="feature-title">{esc(p['title'])}</h3>
            <p class="feature-obj">{esc(p['objective'])}</p>
            {mets}
            <p class="feature-role">{esc(role)} · {esc(when)}</p>
            <p class="feature-tools">{esc(dict(p['facts']).get('Tools', ''))}</p>
            <span class="feature-cta">Read the case study {ARROW}</span>
          </div>
        </a>
      </article>
''')
    o.append('    </div>\n  </div>\n</section>\n')
    # more projects
    o.append('''<section class="section" aria-labelledby="more-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="more-h">More projects</h2></div>
    <div class="cards">
''')
    for p in others:
        cls = 'contain' if p.get('tile_contain') else ''
        k, v = p['card_stat']
        o.append(f'''      <a class="card" href="projects/{p['slug']}.html">
        <div class="card-media">{img(r, p['tile'], cls)}</div>
        <p class="card-kicker">{esc(p['area'])}</p>
        <h3 class="card-title">{esc(p['title'])}</h3>
        <p class="card-desc">{esc(p['card'])}</p>
        <p class="card-stat"><b>{esc(k)}</b> · {esc(v)}</p>
      </a>
''')
    o.append('    </div>\n  </div>\n</section>\n')
    # bench
    # Equal rounded cards at staggered heights, each drifting on its own slow cycle.
    o.append('''<section class="section" aria-labelledby="bench-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="bench-h">More from the bench</h2></div>
    <div class="float-field">
''')
    for i, (name, cap, pos, _span) in enumerate(BENCH):
        o.append(f'      <figure class="float-item" style="--i:{i}"><a class="float-card lb" href="{r}assets/img/{name}.webp" data-cap="{esc(cap)}">'
                 f'{img(r, name).replace(" />", f" style=\"object-position:{pos}\" />")}</a>'
                 f'<figcaption>{esc(cap)}</figcaption></figure>\n')
    o.append('    </div>\n  </div>\n</section>\n')
    # experience: a timeline beside a sticky title, then skills in one panel
    o.append(f'''<section class="section" id="experience" aria-labelledby="xp-h">
  <div class="wrap xp-wrap">
    <div class="xp-side">
      <h2 id="xp-h">Experience</h2>
      <a class="btn btn-sm" href="{RESUME}" target="_blank" rel="noopener">Full résumé (PDF)</a>
    </div>
    <ol class="timeline">
''')
    for when, role, org, text, link in EXPERIENCE:
        l = f'<a class="tl-link" href="{link[0]}">{esc(link[1])} {ARROW}</a>' if link else ''
        o.append(f'''      <li class="tl-item">
        <p class="tl-when">{esc(when)}</p>
        <h3>{esc(role)}</h3>
        <p class="tl-org">{esc(org)}</p>
        <p class="tl-text">{text}</p>
        {l}
      </li>
''')
    o.append('    </ol>\n  </div>\n  <div class="wrap">\n    <div class="skills-panel">\n')
    for title, items in SKILLS:
        o.append(f'      <div><h3>{title}</h3><p>{" · ".join(items)}</p></div>\n')
    o.append('    </div>\n  </div>\n</section>\n')
    # contact: a closing band with one clear row per way to reach me
    rows = [('Email', EMAIL, f'mailto:{EMAIL}', ''),
            ('Phone', PHONE, f'tel:{PHONE_TEL}', ''),
            ('LinkedIn', 'linkedin.com/in/manavchandaka', LINKEDIN, ' target="_blank" rel="noopener"'),
            ('GitHub', 'SIGRobotics-UIUC/LeKiwi', GITHUB, ' target="_blank" rel="noopener nofollow"'),
            ('Résumé', 'Manav_Chandaka_Resume.pdf', RESUME, ' target="_blank" rel="noopener"')]
    rows_html = ''.join(f'<a class="c-row" href="{h}"{a}><span class="c-k">{k}</span><span class="c-v">{esc(v)}</span>{ARROW}</a>' for k, v, h, a in rows)
    o.append(f'''<section class="contact" id="contact" aria-labelledby="contact-h">
  <div class="wrap contact-grid">
    <div>
      <h2 id="contact-h" class="contact-title">Contact</h2>
      <p class="lead">Email is the fastest way to reach me. I’m glad to talk through any of the projects above.</p>
    </div>
    <div class="c-rows">{rows_html}</div>
  </div>
</section>
</main>
''')
    o.append(footer(r))
    return ''.join(o)

# --------------------------------------------------------------------------- case studies
def frame_style(opts):
    ar = opts.get('ar')
    return f' style="--ar:{ar}"' if ar else ''

def frame_cls(opts):
    c = 'frame'
    if opts.get('contain'): c += ' contain'
    if opts.get('pad'): c += ' pad'
    return c

def figcap(cap):
    return f'<figcaption class="figcap"><span>{cap}</span></figcaption>' if cap else ''

def body_html(items):
    out = []
    for kind, val in items:
        if kind == 'lead': out.append(f'<p class="lead">{val}</p>')
        elif kind == 'p': out.append(f'<p>{val}</p>')
        elif kind == 'ul': out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in val) + '</ul>')
    return ''.join(out)

def block_html(b, r):
    kind = b[0]
    if kind == 'single':
        _, name, cap, opts = b
        cls = 'fig m-single' + (' narrow' if opts.get('narrow') else '') + (' small' if opts.get('small') else '') + (' natural' if opts.get('natural') else '')
        return (f'<figure class="{cls}"{frame_style(opts)}><div class="{frame_cls(opts)}">'
                f'{lb(r, name, img(r, name), cap)}</div>{figcap(cap)}</figure>')
    if kind == 'compare':
        _, pair, cap, opts = b
        cells = ''.join(f'<div><div class="{frame_cls(opts)}"><span class="tag">{esc(lab)}</span>{lb(r, n, img(r, n), sub)}</div>'
                        f'<p class="sub">{esc(sub)}</p></div>' for n, lab, sub in pair)
        return f'<figure class="fig m-compare"{frame_style(opts)}><div class="pair">{cells}</div>{figcap(cap)}</figure>'
    if kind == 'sequence':
        _, steps, cap, opts = b
        cells = ''.join(f'<div class="step"><div class="{frame_cls(opts)}">{lb(r, n, img(r, n), lab)}</div>'
                        f'<p class="step-lab">{esc(lab)}</p></div>' for n, lab in steps)
        st = f' style="--n:{len(steps)};--ar:{opts.get("ar", "1/1")}"'
        return f'<figure class="fig m-seq"{st}><div class="steps">{cells}</div>{figcap(cap)}</figure>'
    if kind == 'annotated':
        _, name, cap, pins, opts = b
        pin_html = ''.join(f'<span class="pin" style="--x:{x}%;--y:{y}%" aria-hidden="true">{i+1}</span>' for i, (x, y, t, d) in enumerate(pins))
        legend = ''.join(f'<li><div><b>{esc(t)}</b><span>{esc(d)}</span></div></li>' for x, y, t, d in pins)
        bg = ' style="background:#fff"' if name == 'climber-robot' else ''
        return (f'<figure class="fig m-anno"{frame_style(opts)}><div class="anno"><div class="{frame_cls(opts)}"{bg}>'
                f'{lb(r, name, img(r, name), cap)}{pin_html}</div><ol class="legend" aria-label="Labelled components">{legend}</ol></div>{figcap(cap)}</figure>')
    if kind == 'video':
        _, vid, poster, cap, title, text, specs, opts = b
        w, h = dims(poster)
        dl = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in specs)
        cls = 'fig m-video' + (' portrait' if opts.get('portrait') else '')
        return (f'<figure class="{cls}"><div class="vid"><div class="vframe"><video controls playsinline preload="none" '
                f'width="{w}" height="{h}" poster="{r}assets/img/{poster}.webp" aria-label="{esc(title)}">'
                f'<source src="{r}assets/video/{vid}.mp4" type="video/mp4" /></video></div>'
                f'<div class="spec"><h3>{esc(title)}</h3><p>{esc(text)}</p><dl>{dl}</dl></div></div>{figcap(cap)}</figure>')
    if kind == 'clips':
        # Short silent clips side by side, each with its own controls.
        _, items, cap = b
        cells = ''.join(
            f'<div><div class="vframe"><video controls muted loop playsinline preload="none" poster="{r}assets/img/{v}-poster.webp" '
            f'aria-label="{esc(c)}"><source src="{r}assets/video/{v}.mp4" type="video/mp4" /></video></div><p class="gcap">{esc(c)}</p></div>'
            for v, c in items)
        return f'<figure class="fig m-clips" style="--n:{len(items)}"><div class="grid">{cells}</div>{figcap(cap)}</figure>'
    if kind == 'gallery':
        _, items, cap, opts = b
        st = f' style="--cols:{opts.get("cols", 3)};--ar:{opts.get("ar", "4/3")}"'
        cells = ''.join(f'<div><div class="{frame_cls(opts)}">{lb(r, n, img(r, n), c)}</div><p class="gcap">{esc(c)}</p></div>' for n, c in items)
        return f'<figure class="fig m-gallery"{st}><div class="grid">{cells}</div>{figcap(cap)}</figure>'
    if kind == 'table':
        _, cap, cols, rows, hi = b
        th = ''.join(f'<th scope="col">{esc(c)}</th>' for c in cols)
        trs = ''.join(f'<tr{" class=\"hi\"" if i == hi else ""}>' + ''.join(f'<td>{esc(c)}</td>' for c in row) + '</tr>' for i, row in enumerate(rows))
        return f'<figure class="fig m-table"><div class="tbl-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>{figcap(cap)}</figure>'
    if kind == 'prose':
        return f'<div class="prose prose-inset">{body_html(b[1])}</div>'
    if kind == 'stream':
        _, embed, page, label = b
        return (f'<figure class="fig m-stream"><div class="stream" data-embed="{esc(embed)}" data-title="{esc(label)}">'
                f'<button type="button"><span class="play" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'
                f'{esc(label)}<small>Loads a Google Drive player</small></button></div>'
                f'<figcaption class="figcap"><span>{esc(label)}. <a class="ext" href="{esc(page)}" target="_blank" rel="noopener">Open in Google Drive {EXT}</a></span></figcaption></figure>')
    if kind == 'placeholder':
        if not SHOW_PLACEHOLDERS:
            return ''
        _, what, detail = b
        return f'<div class="placeholder" role="note"><b>Media in progress · {esc(what)}</b><span>{esc(detail)}</span></div>'
    if kind == 'note':
        _, label, text = b
        return f'<p class="note"><span class="mono">{esc(label)}</span><span>{esc(text)}</span></p>'
    raise ValueError(kind)

def build_project(i, p):
    r = '../'
    # Unlisted pages stay reachable by URL but are left out of the prev/next loop.
    listed = [q for q in PROJECTS if not q.get('hidden')]
    k = listed.index(p) if p in listed else -1
    prev_p, next_p = listed[(k - 1) % len(listed)], listed[(k + 1) % len(listed)]
    hero_name, hopts = p['hero']
    o = [head(r, f"{p['title']} · Manav Chandaka", p['objective'], f"projects/{p['slug']}.html",
              og_image=f"assets/img/{hero_name}.webp"),
         '</head>\n<body>\n', header(r, False), '<main id="main">\n<article class="cs">\n']
    o.append(f'''<header class="wrap cs-top">
  <a class="crumb" href="../index.html#work">← All work</a>
  <p class="eyebrow">{esc(p['kicker'])}</p>
  <h1 class="cs-title">{esc(p['title'])}</h1>
  <p class="cs-obj">{esc(p['objective'])}</p>
</header>
''')
    badge = f'<span class="tag">{esc(hopts["badge"])}</span>' if hopts.get('badge') else ''
    bg = ' style="background:#fff"' if hero_name == 'climber-robot' else ''
    o.append(f'''<div class="cs-hero">
  <figure class="m-single" style="--ar:{hopts.get('ar', '16/9')}"><div class="{frame_cls(hopts)}"{bg}>{badge}{lb(r, hero_name, img(r, hero_name, eager=True), ALT.get(hero_name, ''))}</div></figure>
</div>
''')
    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p['facts'])
    o.append('<div class="wrap">\n')
    if p.get('summary'):
        cells = ''.join(f'<div><h2>{esc(k)}</h2><p>{esc(v)}</p></div>' for k, v in p['summary'])
        o.append(f'  <section class="glance" aria-label="At a glance">{cells}</section>\n')
    o.append(f'  <dl class="cs-facts">{facts}</dl>\n')
    if p['metrics']:
        ms = ''.join(f'<div><dt>{esc(l)}</dt><dd{" class=\"word\"" if u == "word" else ""}>{metric_value(v, u)}</dd></div>' for v, u, l in p['metrics'])
        o.append(f'  <dl class="cs-results" aria-label="Key results">{ms}</dl>\n')
    o.append('</div>\n')
    if len(p['sections']) > 2:
        toc = ''.join(f'<a href="#{s["id"]}"><b>{j+1:02d}</b>{esc(s["title"])}</a>' for j, s in enumerate(p['sections']))
        o.append(f'<div class="toc-bar"><nav class="wrap toc" aria-label="On this page">{toc}</nav></div>\n')
    for j, s in enumerate(p['sections']):
        blocks = ''.join(block_html(b, r) for b in s.get('blocks', []))
        blocks = f'<div class="blocks">{blocks}</div>' if blocks else ''
        o.append(f'''<section class="wrap cs-sec" id="{s['id']}" aria-labelledby="{s['id']}-h">
  <div class="cs-sec-grid">
    <div class="cs-sec-head"><span class="num">{j+1:02d}</span><h2 id="{s['id']}-h">{esc(s['title'])}</h2></div>
    <div class="prose">{body_html(s['body'])}</div>
  </div>
  {blocks}
</section>
''')
    if p['links']:
        ls = ''.join(f'<a class="btn" href="{esc(h)}" target="_blank" rel="noopener{" nofollow" if "github.com" in h else ""}">{esc(t)} {EXT}</a>' for h, t in p['links'])
        o.append(f'<div class="wrap"><div class="cs-links">{ls}</div></div>\n')
    o.append(f'''<div class="wrap"><aside class="cs-cta" aria-label="Get in touch">
  <p>Want to talk through this project?<span>I’m happy to go deeper on the design decisions and testing.</span></p>
  <div><a class="btn primary" href="mailto:{EMAIL}">Email me</a><a class="btn" href="{r}{RESUME}" target="_blank" rel="noopener">Résumé (PDF)</a></div>
</aside></div>
''')
    def nav_card(q, d):
        return (f'<a href="{q["slug"]}.html"><span class="thumb">{img(r, q["tile"], "contain" if q.get("tile_contain") else "")}</span>'
                f'<span><span class="dir">{d}</span><span class="ttl">{esc(q["title"])}</span></span></a>')
    o.append(f'<nav class="wrap cs-next" aria-label="More projects"><div class="cs-next-grid">{nav_card(prev_p, "← Previous")}{nav_card(next_p, "Next →")}</div></nav>\n')
    o.append('</article>\n</main>\n')
    o.append(footer(r))
    return ''.join(o)

def main():
    os.makedirs(os.path.join(ROOT, 'projects'), exist_ok=True)
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(build_index())
    for i, p in enumerate(PROJECTS):
        with open(os.path.join(ROOT, 'projects', p['slug'] + '.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(build_project(i, p))
    print('built index.html +', len(PROJECTS), 'project pages')

if __name__ == '__main__':
    main()
