# -*- coding: utf-8 -*-

from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django_vingd.models import VingdOrder, VingdMeta
from django_vingd.util import HttpResponseJSON

class Candidate(models.Model):
    name = models.CharField(max_length=128)
    votes = models.IntegerField(default=0)
    
    def add_vote(self):
        Candidate.objects.filter(id=self.id).update(votes=models.F('votes')+1)
        self.votes += 1

@VingdMeta.register()
class VoteOrder(VingdOrder):
    candidate = models.ForeignKey(Candidate)

    def get_display_name(self):
        return 'Glas kandidatu'

    def take_order(self):
        self.candidate_id = self.request.POST.get('candidate_id')

    def get_vingd_amount(self):
        return 20
    
    def accept_order(self):
        self.candidate.add_vote()

    def success_response(self):
        if self.request.is_ajax():
            return HttpResponseJSON({
                'ok': True,
                'votes': self.candidate.votes,
            })
        return HttpResponseRedirect('/')
