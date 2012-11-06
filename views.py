""" Create your views here."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UploadMasterImageForm
from models import *

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

            form=UploadMasterImageForm()

    if request.method == 'GET':
        form = UploadMasterImageForm()

    return render_to_response('repo/upload.html',
            {'form': form, 'obj': obj}, context_instance=RequestContext(request))

def display(request, pid):
    repo = Repository()
    obj = repo.get_object(pid )
    return render_to_response('repo/display.html',{'obj':obj})

