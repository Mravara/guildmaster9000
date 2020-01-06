from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404, JsonResponse
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, F, Sum
from django.core import serializers

from guildmaster9000.decorators import *
from itertools import chain

from members.models import Member, Character, EPLog
from raid.models import Raid, RaidCharacter, BenchedRaidCharacter
from loot.models import Loot
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from raid.forms import NewRaidForm, GiveItemForm, GiveEPForm, AddRaidersForm, AddBenchedRaidersForm


def index(request):
    raids = Raid.objects.order_by('-start').annotate(total_items=Count('loot')).select_related('dungeon', 'leader').prefetch_related('raidcharacter')
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    referer = request.META.get('HTTP_REFERER')
    raid = None
    try:
        raid = Raid.objects.select_related('leader', 'dungeon').get(pk=raid_id)
    except Raid.DoesNotExist:
        raise Http404("WTF?")
    loot = Loot.objects.filter(raid=raid).select_related('item', 'character', 'item_info', 'given_by')
    form = None
    form_ep = None
    form_add_raiders = None
    form_add_benched_raiders = None
    
    characters = RaidCharacter.objects.filter(raid=raid).select_related('character__owner')
    
    benched_characters = BenchedRaidCharacter.objects.filter(raid=raid).select_related('character__owner')
    
    all_characters_query = Character.objects.all()
    raid_characters_query = characters.filter(end=None).order_by('character__name')

    if not raid.done:
        form = GiveItemForm()
        form.fields['character'].queryset = raid_characters_query
        form_ep = GiveEPForm()
        form_ep.fields['character'].queryset = raid_characters_query
        form_add_raiders = AddRaidersForm()
        form_add_raiders.fields['character'].queryset = all_characters_query
        form_add_benched_raiders = AddBenchedRaidersForm()
        form_add_benched_raiders.fields['character'].queryset = all_characters_query
    context = {
        'raid': raid,
        'loot': loot,
        'raid_characters': characters,
        'benched_raid_characters': benched_characters,
        'form': form,
        'form_ep': form_ep,
        'form_add_raiders': form_add_raiders,
        'form_add_benched_raiders': form_add_benched_raiders,
        'item_types': ItemInfo.ItemSlot.choices,
        'breadcrumbs': [
            'Raids' if (referer is not None and 'raids' in referer)else 'Loot',
            raid.dungeon.name,
        ]
    }
    return render(request, "raid/raid.html", context)


@officers('/raids/')
def new_raid(request):
    if request.method == 'POST':
        form = NewRaidForm(request.POST)

        if form.is_valid():
            leader = request.user.member
            dung = form.cleaned_data.get('dungeon')
            raid = Raid(dungeon=dung, leader=leader)
            raid.save()

            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list.append('Primalbank')
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            text_members_list = [x.capitalize().strip() for x in text_members_list]

            if len(text_members_list) > 0:
                characters = Character.objects.filter(name__in=text_members_list)
                RaidCharacter.objects.bulk_create([RaidCharacter(character=c, raid=raid) for c in characters])
            else:
                return redirect("/raids/{}/".format(raid.id))
            
            text_benched_members = form.cleaned_data.get('benched_members')
            text_benched_members_list = text_benched_members.splitlines()
            text_benched_members_list = list(dict.fromkeys(text_benched_members_list)) # removes duplicates

            if len(text_benched_members_list) > 0:
                characters = Character.objects.filter(name__in=text_benched_members_list)
                BenchedRaidCharacter.objects.bulk_create([BenchedRaidCharacter(character=c, raid=raid) for c in characters])

            return HttpResponseRedirect(reverse('raid', args=(raid.id,)))

        return redirect(request.path)

    context = {
        'form': NewRaidForm(),
        'breadcrumbs': [
            'Raids',
            'New Raid',
        ],
    }
    return render(request, "raid/new_raid.html", context)


@officers('/raids/')
def give_item(request, raid_id):
    if request.method == 'POST':
        form = GiveItemForm(request.POST)
        if form.is_valid():
            character = form.cleaned_data.get('character')
            item_id = form.cleaned_data.get('item_id')
            item_info = form.cleaned_data.get('item_slot')
            comment = form.cleaned_data.get('comment')
            raid = get_object_or_404(Raid, pk=raid_id)
            item = get_object_or_404(Item, pk=item_id)
            price_percentage = form.cleaned_data.get('price')
            loot = Loot(
                character=character.character,
                raid=raid,
                item=item,
                item_info=item_info,
                price_percentage=price_percentage,
                given_by=request.user.member,
                comment=comment,
            )
            loot.save()
            character.character.owner.gp = F('gp') + loot.gp
            character.character.owner.save()
        return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def complete_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.SUCCESS
    raid.save()
    RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def pause_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.PAUSED
    raid.save()
    RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def fail_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.FAILED
    raid.save()
    RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = RaidCharacter.objects.get(id=raider_id, raid=raid)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_benched_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = BenchedRaidCharacter.objects.get(id=raider_id, raid=raid)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def delete_loot(request, raid_id, loot_id):
    loot = get_object_or_404(Loot, pk=loot_id)
    loot.character.owner.gp = F('gp') - loot.gp
    loot.character.owner.save()
    loot.delete()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def give_ep(request, raid_id):
    form = GiveEPForm(request.POST)
    if form.is_valid():
        ep = form.cleaned_data.get('ep')
        character = form.cleaned_data.get('character')
        raid = get_object_or_404(Raid, pk=raid_id)

        print(character)

        if character is not None:
            character.character.owner.ep = F('ep') + ep
            character.character.owner.save()
            character.earned_ep = F('earned_ep') + ep
            character.save()
        else:
            raiders = RaidCharacter.objects.filter(raid=raid, end=None).select_related('character__owner')
            raiders.update(earned_ep=F('earned_ep') + ep)
            for raider in raiders:
                raider.character.owner.ep = F('ep') + ep
                raider.character.owner.save()
            
            benched_raiders = BenchedRaidCharacter.objects.filter(raid=raid, end=None).select_related('character__owner')
            benched_raiders.update(earned_ep=F('earned_ep') + ep)
            for benched_raider in benched_raiders:
                benched_raider.character.owner.ep = F('ep') + ep
                benched_raider.character.owner.save()
        
        EPLog.objects.create(raid=raid, amount=ep)
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_raiders(request, raid_id):
    form = AddRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        character = form.cleaned_data.get('character')

        if character is not None:
            RaidCharacter.objects.create(character=character, raid=raid)
        else:
            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            text_members_list = [x.capitalize().strip() for x in text_members_list]

            characters = Character.objects.filter(name__in=text_members_list)
            RaidCharacter.objects.bulk_create([RaidCharacter(character=c, raid=raid) for c in characters])

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_benched_raiders(request, raid_id):
    form = AddBenchedRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        character = form.cleaned_data.get('character')

        if character is not None:
            BenchedRaidCharacter.objects.create(character=character, raid=raid)
        else:
            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            characters = Character.objects.filter(name__in=text_members_list)
            BenchedRaidCharacter.objects.bulk_create([BenchedRaidCharacter(character=c, raid=raid) for c in characters])
    
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def ping(request, raid_id):
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))
    # raid = get_object_or_404(Raid, pk=raid_id)
    # benched_members = raid.benched_members.all()


@officers('/raids/')
def get_items(request, raid_id):
    term = request.GET.get('term')
    items = Item.objects.filter(name__icontains=term, item_quality__gte=Item.Quality.EPIC).values('id', value=F('name')).order_by('name')
    data = []
    for i in items:
        data.append(i)
    print(data)
    return JsonResponse(data, safe=False)
