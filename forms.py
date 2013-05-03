"""Forms for repo application"""
from django import forms
from eulxml.xmlmap.dc import DublinCore
from bdrxml import irMetadata
from eulxml.forms import XmlObjectForm
import ace_editor


class DublinCoreEditForm(XmlObjectForm):
    """Edit form for DublinCore metadata"""
    class Meta:
        """Metadata declaration"""
        model = DublinCore
        fields = ['title', 'creator', 'date']

class EditXMLForm( forms.Form ):
    xml_content = forms.CharField(widget=ace_editor.CodeEditorWidget(mode='xml'))

class UploadMasterImageForm(forms.Form):
    """Upload form for MasterImage Objects"""
    label = forms.CharField(
        max_length=255,  # fedora label maxes out at 255 characters
        help_text='Preliminary title for the new object. 255 characters max.'
    )
    modsFile = forms.FileField(label="MODS")
    masterFile = forms.FileField(label="MASTER")
    colorbarFile = forms.FileField(label="MASTER-COLORBAR")

class EditIRMetadataForm(forms.Form):
    pass

class RightsMetadataEditForm(forms.Form):
    rights_choices = [
        ('PUBLIC', 'Public'),
        ('BROWN', 'Brown Only'),
        ('ADMIN', 'Private')
    ]
    rights = forms.ChoiceField(choices=rights_choices, widget = forms.RadioSelect())
