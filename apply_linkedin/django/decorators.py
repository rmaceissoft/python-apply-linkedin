from functools import wraps
import hmac,hashlib

from django.utils.decorators import available_attrs
from django.http import Http404
from django.conf import settings


def verify_signature(view_func):
    """
    To help you verify the request signature verification 
    to ensure that calls are coming from LinkedIn
    """
    def wrapped_view(request, *args, **kwargs):
        linkedin_signature = request.META.get('HTTP_CONTENT_SIGNATURE', None)
        api_secret = settings.LINKEDIN_API_SECRET
        my_signature = hmac.new(api_secret, request.raw_post_data, hashlib.sha1).digest().encode("base64").strip()

        if (my_signature == linkedin_signature):
            return view_func(request, *args, **kwargs)
            
        else:
            raise Http404("Invalid signature: expected %s, calculated %s" % (linkedin_signature, my_signature))
        
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
