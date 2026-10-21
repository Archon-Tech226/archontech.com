from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def article_body(text):
    """Render plain-text article bodies: '## ' headings, '- ' bullets, blank-line paragraphs."""
    out, bullets, para = [], [], []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % escape(" ".join(para)))
            para.clear()

    def flush_bullets():
        if bullets:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % escape(b) for b in bullets))
            bullets.clear()

    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            flush_para(); flush_bullets()
        elif line.startswith("## "):
            flush_para(); flush_bullets()
            out.append("<h2>%s</h2>" % escape(line[3:]))
        elif line.startswith("- "):
            flush_para()
            bullets.append(line[2:])
        else:
            flush_bullets()
            para.append(line)
    flush_para(); flush_bullets()
    return mark_safe("\n".join(out))


@register.filter
def initials(name):
    parts = (name or "").split()
    return ("".join(p[0] for p in parts[:2]) or "?").upper()


@register.filter
def cover_url(post):
    """Local branded cover for a post, falling back to a generic one."""
    from django.contrib.staticfiles import finders
    from django.templatetags.static import static
    name = "img/cover-%s.svg" % (getattr(post, "slug", "") or "")
    return static(name if finders.find(name) else "img/cover-default.svg")
