==========================
Python Apply with Linkedin
==========================

This library is designed to facilitate implementation of apply with linkedin described at
`https://developer.linkedin.com/apply <https://developer.linkedin.com/application-response-data-structure>`_.

Parse http post request from linkedin and you can get an application object, 
that complies with the data structure described at 
`https://developer.linkedin.com/application-response-data-structure <https://developer.linkedin.com/application-response-data-structure>`_
  

For now it has only implementation for django framework

general instalation
===================

* using **easy_install**
  
  easyinstall python-apply-linkedin

* using **pip** 
  
  pip install python-apply-linkedin

* direct from repository
  
  pip install -e git+git://github.com/rmaceissoft/python-apply-linkedin.git#egg=python-apply-linkedin


django implementation
=====================


Configuration
-------------


#. Add the 'apply_linkedin.django' to INSTALL_APPS

#. define at settings.py the LINKEDIN_API_SECRET variable 

#. Add the following url route
   url(r'^apply_linkedin/', include('apply_linkedin.django.urls')),
   
   

Basic usage
-----------

When linkedin make a http POST request, it is your interes retrive data 
to process current application. To do that connect to signal 
'new_apply_with_linkedin. For example::

     from apply_linkedin.django.signals import new_apply_with_linkedin
     
     def new_apply_with_linkedin_handler(sender, application, **kwargs):
        #retrieve application data
        name=application.person.firstName,
        last_name=application.person.lastName
        full_name = '%s %s' % (name, last_name)
        print "%s has applied to %s" % (full_name, application.job.position.title)

     new_apply_with_linkedin.connect(new_apply_with_linkedin_handler)


Render at template url to process http post request
---------------------------------------------------

Fragment of template page.html::

     <script type="IN/Apply" 
         data-companyName="{{ vacancy.company.name }}" 
         data-jobTitle="{{ vacancy.title }}" 
         data-jobLocation="{{ vacancy.location }}"
         data-jobId="{{ vacancy.id }}"
         data-url="http://{{ current_site.domain }}{% url apply_linkedin.process_application %}">
     </script>
