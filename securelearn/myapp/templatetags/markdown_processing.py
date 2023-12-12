import markdown  as md
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()





#@register.filter: Decorator to register the following function (markdown) as a template filter.
# @stringfilter: Decorator that ensures the input value is treated as a string before applying the filter.
@register.filter()
@stringfilter

# This custom template filter, named 'markdown', converts a Markdown-formatted string to HTML.
# The 'markdown.extensions.fenced_code' extension is included for supporting fenced code blocks.
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
