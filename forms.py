"""Forms for repo application"""
from django import forms
from eulxml.xmlmap.dc import DublinCore
from eulxml.forms import XmlObjectForm


class DublinCoreEditForm(XmlObjectForm):
    """Edit form for DublinCore metadata"""
    class Meta:
        """Metadata declaration"""
        model = DublinCore
        fields = ['title', 'creator', 'date']


class UploadMasterImageForm(forms.Form):
    """Upload form for MasterImage Objects"""
    label = forms.CharField(
        max_length=255,  # fedora label maxes out at 255 characters
        help_text='Preliminary title for the new object. 255 characters max.'
    )
    modsFile = forms.FileField(label="MODS")
    masterFile = forms.FileField(label="MASTER")
    colorbarFile = forms.FileField(label="MASTER-COLORBAR")
