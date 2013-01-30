============
Django Vingd
============

Django Vingd enables integrating Vingd into django project.

Basic setup
===========

1. Add "django_vingd" to INSTALLED_APPS.

2. Configure django settings::

    VINGD_SETTINGS = {
        'sandbox': {
            'VINGD_USR': 'test@knopso.com',
            'VINGD_PWD': '123',
        }
    }
    VINGD_MODE = 'sandbox'

3. In any django app that uses vingd define Vingd Orders details (models.py)::

    # Imaginary scenario where users are voting for candidates via vingd.

    from django.db import models
    from django.http import HttpResponseRedirect
    from django_vingd.models import VingdOrder

    class Candidate(models.Model):
        name = models.CharField(max_length=128)
        votes = models.IntegerField(default=0)
        
        def add_vote(self):
            Candidate.objects.filter(id=self.id).update(votes=models.F('votes')+1)
            self.votes += 1

    class VoteOrder(VingdOrder):
        candidate = models.ForeignKey(Candidate)

        # Short object description
        def get_display_name(self):
            return 'Vote for candidate'

        # Handle form submission (before sending user to vingd)
        def take_order(self):
            self.candidate_id = self.request.POST.get('candidate_id')

        # Determine vingd price
        def get_vingd_amount(self):
            return 75   # 0.75 vingd
        
        # Access is confirmed (user has returned back from vingd)
        def accept_order(self):
            self.candidate.add_vote()

        # Serve requested content to user
        def success_response(self):
            return HttpResponseRedirect('/')

4. Register order classes in your urls (urls.py)::

    from django_vingd.models import VingdMeta
    from base.models import VoteOrder
    
    VingdMeta.register([VoteOrder, ])
    
    urlpatterns = patterns('',
        (r'^vgd/', include('django_vingd.urls')),
    )

5. In HTML template place vingd order forms::

    {% for candidate in candidates %}
        <form action="{% url vingd_order "VoteOrder" %}" method="POST">
            {% csrf_token %}
            {{ candidate.name }}: {{ candidate.votes }}
            <input type="hidden" name="candidate_id" value="{{ candidate.id }}">
            <input type="submit" value="vote">
        </form>
    {% endfor %}

Sync database and start your engines! 


Popup version
=============

1. Add jQuery to your page.

2. Add popup related javascript to HTML head::

    {% load vingd_tt %}
    {% vingd_scripts %}
    
    <script type="text/javascript">
        $(document).ready(function(){
            $('form').vingd_popup(function(data){
                alert('Vote added!');
            }, function(data){
                alert('Failed to add vote.');
            });
        });
    </script> 


3. Handle ajax requests in your VoteOrders (models.py)::

    from django_vingd.util import HttpResponseJSON
    ...
    def success_response(self):
        request = self.request
        if request.is_ajax():
            return HttpResponseJSON({
                'ok': True,
                'votes': self.candidate.votes,
            })
        return HttpResponseRedirect('/')


Deny access to content
======================

In some situations user should not be allowed to access content. Such cases should be handled both for:
  
  * denying access at vingd ordering time (before sending user to vingd)
  * denying access at vingd verification time (after user has returned from vingd).

In those cases one should raise exception within take_order and accept_order respectively.

Handling exceptions
===================

To gracefully handle any kind of exception one should use VingdOrder handle_exception function::

    def handle_exception(self, e):
        // log exception
        // inform user
        return HttpResponse("Inform user that something has gone wrong.")

