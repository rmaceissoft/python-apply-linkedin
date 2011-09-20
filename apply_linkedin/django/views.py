from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

from apply_linkedin.parser import parse_application
from apply_linkedin.django.signals import new_apply_with_linkedin
from apply_linkedin.django.decorators import verify_signature


@csrf_exempt
@verify_signature
def process_application(request):
    """
    when you implement apply with linkedin and choose 
    receive data via HTTP POST, this view parses the request and 
    dispatch a signal with application object as param.
    """
    if request.method == 'POST':
        post_body = request.raw_post_data
        application = parse_application(post_body)
        new_apply_with_linkedin.send(sender=None, application=application, request=request)
        return HttpResponse()
    else:
        raise Http404()
        
        
        