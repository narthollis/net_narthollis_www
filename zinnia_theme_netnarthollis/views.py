
from django.http import HttpResponse
from pygments.formatters import HtmlFormatter

def get_pygments_css(request):
    response = HttpResponse(content_type="text/css")

    response.write(HtmlFormatter().get_style_defs('.codehilite'))

    return response
    
