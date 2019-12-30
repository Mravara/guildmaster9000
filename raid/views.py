from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, F
from guildmaster9000.decorators import *

from members.models import Member, Character
from raid.models import Raid, RaidCharacter, BenchedRaidCharacter
from loot.models import Loot
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from raid.forms import NewRaidForm, GiveItemForm, GiveEPForm, AddRaidersForm, AddBenchedRaidersForm


def index(request):
    raids = Raid.objects.order_by('-start').annotate(total_items=Count('loot'))
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    referer = request.META.get('HTTP_REFERER')
    raid = get_object_or_404(Raid, pk=raid_id)
    loot = Loot.objects.filter(raid=raid)
    items = None
    form = None
    form_ep = None
    form_add_raiders = None
    form_add_benched_raiders = None
    characters = raid.raid_characters.all()
    benched_characters = raid.benched_raid_characters.all()
    if not raid.done:
        items = Item.objects.filter(item_quality__gte=Item.Quality.EPIC)
        form = GiveItemForm()
        form.fields['character'].queryset = raid.raid_characters.order_by('character__name')
        form_ep = GiveEPForm()
        form_add_raiders = AddRaidersForm()
        form_add_benched_raiders = AddBenchedRaidersForm()
    context = {
        'raid': raid,
        'loot': loot,
        'items': items,
        'raid_characters': characters,
        'benched_raid_characters': benched_characters,
        'form': form,
        'form_ep': form_ep,
        'form_add_raiders': form_add_raiders,
        'form_add_benched_raiders': form_add_benched_raiders,
        'item_types': ItemInfo.ItemSlot.choices,
        'breadcrumbs': [
            'Raids' if 'raids' in referer else 'Loot',
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
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates

            if len(text_members_list) > 0:
                characters = Character.objects.filter(name__in=text_members_list)
                raiders = RaidCharacter.objects.bulk_create([RaidCharacter(character=c) for c in characters])
                raid.raid_characters.set(raiders)
                raid.save()
            else:
                return redirect("/raids/{}/".format(raid.id))
            
            text_benched_members = form.cleaned_data.get('benched_members')
            text_benched_members_list = text_benched_members.splitlines()
            text_benched_members_list = list(dict.fromkeys(text_benched_members_list)) # removes duplicates

            if len(text_benched_members_list) > 0:
                characters = Character.objects.filter(name__in=text_benched_members_list)
                raiders = BenchedRaidCharacter.objects.bulk_create([BenchedRaidCharacter(character=c) for c in characters])
                raid.benched_raid_characters.set(raiders)
                raid.raid = raid
                raid.save()

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
        print(form.errors)
        print(form.cleaned_data)
        if form.is_valid():
            character = form.cleaned_data.get('character')
            item_id = form.cleaned_data.get('item_id')
            item_info = form.cleaned_data.get('item_slot')
            comment = form.cleaned_data.get('comment')
            raid = get_object_or_404(Raid, pk=raid_id)
            item = get_object_or_404(Item, pk=item_id)
            price_percentage = form.cleaned_data.get('price')
            loot = Loot(
                member=character.character.owner,
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
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.benched_raid_characters.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def pause_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.PAUSED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def fail_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.FAILED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = raid.raid_characters.get(id=raider_id)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_benched_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = raid.benched_raid_characters.get(id=raider_id)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def delete_loot(request, raid_id, loot_id):
    loot = get_object_or_404(Loot, pk=loot_id)
    loot.member.gp = F('gp') - loot.gp
    loot.member.save()
    loot.delete()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def give_ep(request, raid_id):
    form = GiveEPForm(request.POST)

    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        raiders = raid.raid_characters.all()
        for raider in raiders:
            if not raider.done:
                raider.member.ep = F('ep') + form.cleaned_data.get('ep')
                raider.member.save()

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_raiders(request, raid_id):
    form = AddRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        text_members = form.cleaned_data.get('members')
        text_members_list = text_members.splitlines()
        text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
        characters = Character.objects.filter(name__in=text_members_list)
        raiders = RaidCharacter.objects.bulk_create([RaidCharacter(character=c) for c in characters])
        raid.raid_characters.add(*raiders)
        raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_benched_raiders(request, raid_id):
    form = AddBenchedRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        text_members = form.cleaned_data.get('members')
        text_members_list = text_members.splitlines()
        text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
        characters = Character.objects.filter(name__in=text_members_list)
        raiders = BenchedRaidCharacter.objects.bulk_create([BenchedRaidCharacter(character=c) for c in characters])
        raid.benched_raid_characters.add(*raiders)
        raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def ping(request, raid_id):
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))
    # raid = get_object_or_404(Raid, pk=raid_id)
    # benched_members = raid.benched_members.all()

