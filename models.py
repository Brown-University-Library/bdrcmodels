#from django.db import models
from eulfedora.models import DigitalObject, FileDatastream, XmlDatastream, RdfDatastream
from bdrxml import rights
from bdrxml import irMetadata
from bdrxml import mods
from bdrxml import rels

# Create your models here.
def choose_content_model(ds_list):
    """Chooses the appropriate content model based on the contents of the list of datastream names"""
    if "MP3" in ds_list:
        return AudioMP3
    elif "PDF" in ds_list:
        return PDFDigitalObject
    elif "MASTER-COLORBAR" in ds_list:
        return MasterImage
    elif "MASTER" in ds_list:
        return MasterImage
    else:
        return ImplicitSet

CONTENT_MODEL_BASE_PID = 'bdr-cmodel'
CONTENT_MODEL_BASE_URI = 'info:fedora/%s' % CONTENT_MODEL_BASE_PID

COMMON_METADATA_CONTENT_MODEL = "%s:commonMetadata" % CONTENT_MODEL_BASE_URI
class CommonMetadataDO(DigitalObject):
    CONTENT_MODELS = [COMMON_METADATA_CONTENT_MODEL]

    rels_int= XmlDatastream("RELS-INT", "Internal Datastream Relations", rels.RelsInt, defaults={
            'control_group': 'X',
            'format': 'info:fedora/fedora-system:FedoraRELSInt-1.0',
            'versionable': True,
        })

    rightsMD = XmlDatastream('rightsMetadata', "Rights Metadata", rights.Rights, defaults={
        'control_group': 'X',
        'format' : 'http://cosimo.stanford.edu/sdr/metsrights/',
        'versionable': True,
        })
    
    irMD = XmlDatastream('irMetadata', "Institutional Repository Metadata", irMetadata.IR, defaults={
        'control_group': 'X',
        'format' : 'http://dl.lib.brown.edu/md/irdata',
        'versionable': True,
        })
    mods = XmlDatastream('MODS', "MODS metadata", mods.Mods,  defaults={
        'control_group': 'M',
        'format' : mods.MODS_NAMESPACE,
        'versionable': True,
        })

MASTER_TIFF_CONTENT_MODEL = '%s:masterImage' % CONTENT_MODEL_BASE_URI
JP2_CONTENT_MODEL = '%s:jp2' % CONTENT_MODEL_BASE_URI
class MasterImage(CommonMetadataDO):
    CONTENT_MODELS = [ MASTER_TIFF_CONTENT_MODEL, JP2_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    master = FileDatastream("MASTER", "Master Image File", defaults={
        'versionable': True,
        'control_group': 'M',
        'mimetype': 'image/tiff',
        })

    master_colorbar = FileDatastream("MASTER-COLORBAR", "Master Image File with the Colorbar", defaults={
        'versionable': True,
        'control_group': 'M',
        'mimetype': 'image/tiff',
        })

    jp2 = FileDatastream("JP2", "JP2 version of the MASTER image.  Suitable for further dissemination", defaults={
        'versionable': True,
        'control_group': 'M',
        'mimetype': 'image/jp2',
        })

PDF_CONTENT_MODEL = '%s:pdf' % CONTENT_MODEL_BASE_URI
class PDFDigitalObject(CommonMetadataDO):
    CONTENT_MODELS = [ PDF_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    pdf = FileDatastream("PDF", "PDF Document", defaults={
        'versionable': True,
        'control_group': 'M',
        'mimetype': 'application/pdf',
        })

MP3_CONTENT_MODEL = '%s:mp3' % CONTENT_MODEL_BASE_URI
class AudioMP3(CommonMetadataDO):
    CONTENT_MODELS = [ MP3_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    mp3 = FileDatastream("MP3", "MP3 Audio File", defaults={
        'versionable': True,
        'control_group': 'M',
        'mimetype': 'audio/mpeg',
        })

IMPLICIT_SET_CONTENT_MODEL = '%s:implicit-set' % CONTENT_MODEL_BASE_URI
class ImplicitSet(CommonMetadataDO):
    CONTENT_MODELS = [ IMPLICIT_SET_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
