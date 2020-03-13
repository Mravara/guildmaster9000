from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.utils.timezone import datetime
from members.models import Member, Character
from officers.models import Log
from guildmaster9000.decorators import *
from officers.forms import DecayForm, NewMemberForm
from django.contrib.auth.models import User
from django.contrib import messages


@officers('/')
def index(request):
    form = DecayForm()
    new_member_form = NewMemberForm()
    context = {
        'form': form,
        'new_member_form': new_member_form,
    }
    return render(request, "officers/index.html", context)


@officers('/')
def decay_epgp(request):
    form = DecayForm(request.POST)
    if form.is_valid():
        decay = form.cleaned_data.get('decay')
        members = Member.objects.all()
        members.update(ep=F('ep') * (1 - decay/100), gp=F('gp') * (1 - decay/100))
        for m in members:
            Log.objects.create(
                writer=request.user.member,
                target_member=m,
                action=Log.Action.DECAY,
                value='{0}'.format(decay)
            )
        messages.success(request, "Decay of {0}% slammed!".format(decay))
    else:
        messages.error(request, "Something went wrong :(")
    return HttpResponseRedirect(reverse('officers_index'))


@officers('/')
def new_member(request):
    form = NewMemberForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        character_name = form.cleaned_data.get('character_name')
        character_class = form.cleaned_data.get('character_class')
        discord_id = form.cleaned_data.get('discord_id')
        starting_ep = form.cleaned_data.get('starting_ep')
        starting_gp = form.cleaned_data.get('starting_gp')
        user = User(username=username, password=password)
        user.save()

        member = Member(
            user=user, 
            discord_id=discord_id, 
            name=character_name, 
            rank=Member.Rank.MEMBER, 
            ep=starting_ep, 
            gp=starting_gp
        )
        member.save()

        character = Character(
            name=character_name,
            owner=member,
            character_class=character_class,
        )
        character.save()

        log = Log(
            writer=request.user.member, 
            target=character, 
            target_member=member, 
            action=Log.Action.NEW_MEMBER
        )
        log.save()

        messages.success(request, "Member {0} created. Good job.".format(character_name))
    else:
        messages.error(request, "Something went wrong :(")

    return HttpResponseRedirect(reverse('officers_index'))


@officers('/')
def logs(request):
    pass
