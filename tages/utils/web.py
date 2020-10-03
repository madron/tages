from django.utils.html import format_html


def email_link(email):
    if email:
        return format_html(
            '<a href="mailto:{email}" title="{email}">{email}</a>',
            email=email,
        )
    return ''


def url_link(url, label=None, title=None):
    if url:
        if not label:
            label = url
        info = dict(url=url, label=label, title=title)
        if title:
            return format_html('<a href="{url}" title="{title}">{label}</a>', **info)
        return format_html('<a href="{url}">{label}</a>', **info)
    return ''


def pdf_link(pdf):
    if pdf:
        return format_html(
            '<a href="{pdf}" title="{pdf}" class="icon-book">',
            pdf=pdf,
        )
    return ''
