# ManavCha328.github.io

Static portfolio served by GitHub Pages.

- `index.html`, `projects/*.html`: generated pages (committed)
- `assets/css/site.css`, `assets/js/site.js`: shared styles and behaviour, no dependencies
- `assets/img/*.webp`, `assets/video/*.mp4`: media
- `tools/content.py`: all page text, metrics, and media layouts
- `tools/build.py`: turns `content.py` into the HTML

To change content, edit `tools/content.py`, then run:

```bash
python tools/build.py
```

The build needs Pillow (`pip install pillow`) to read image sizes.
Set `SHOW_PLACEHOLDERS = False` in `build.py` to hide "media in progress" boxes.
