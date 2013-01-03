""" Create your views here."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UploadMasterImageForm
from forms import DublinCoreEditForm
from models import CommonMetadataDO, MasterImage
from eulfedora.server import Repository


def upload(request):
    """Upload view for mastertiff objects"""
    obj = None
    form = UploadMasterImageForm()
    if request.method == 'POST':
        form = UploadMasterImageForm(request.POST, request.FILES)
        if form.is_valid():
            repo = Repository()
            obj = repo.get_object(type=MasterImage)
            obj.mods.content = request.FILES['modsFile'].read()
            obj.master.content = request.FILES['masterFile']
            obj.master_colorbar.content = request.FILES['colorbarFile']
            obj.label = form.cleaned_data['label']
            obj.dc.content.title = form.cleaned_data['label']
            obj.save()

            form = UploadMasterImageForm()

    if request.method == 'GET':
        form = UploadMasterImageForm()

    return render_to_response(
        'repo/upload.html',
        {
            'form': form,
            'obj': obj
        },
        context_instance=RequestContext(request)
    )


def display(request, pid):
    repo = Repository()
    obj = repo.get_object(pid)
    return render_to_response('repo/display.html', {'obj': obj})


def edit(request, pid):
    repo = Repository()
    obj = repo.get_object(pid, type=CommonMetadataDO)
    if request.method == "POST":
        form = DublinCoreEditForm(request.POST, instance=obj.dc.content)
        if form.is_valid():
            form.update_instance()
            obj.save()
    elif request.method == 'GET':
        form = DublinCoreEditForm(instance=obj.dc.content)
    return render_to_response('repo/edit.html', {'form': form, 'obj': obj}, context_instance=RequestContext(request))
