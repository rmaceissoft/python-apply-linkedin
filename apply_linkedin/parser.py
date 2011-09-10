from apply_linkedin.models import Application
from apply_linkedin.utils import simplejson


def parse_application(raw_response):
    """
    main function used to parse application response according to data structure provied by Linkedin
    https://developer.linkedin.com/application-response-data-structure 
    """
    application_json = simplejson.loads(raw_response)
    return Application.parse(application_json)


