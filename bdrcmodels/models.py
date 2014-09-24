from eulfedora.models import DigitalObject, FileDatastream, XmlDatastream, Relation
from bdrxml import rights
from bdrxml import irMetadata
from bdrxml import mods
from bdrxml import mets
from bdrxml import rels
from bdrxml import darwincore
from rdflib import URIRef
from rdflib.namespace import Namespace
from eulfedora.rdfns import relsext as relsextns


def choose_content_model(ds_list, default_model=None):
    """Chooses the appropriate content model based on the contents of the list of datastream names"""
    #audio formats
    if "AUDIO-MASTER" in ds_list:
        if "MP3" in ds_list:
            return AudioMP3
        else:
            return AudioMaster
    elif "MP3" in ds_list:
        return MP3
    #video formats
    elif "MP4" in ds_list:
        return VideoMP4
    elif "MOV" in ds_list:
        return VideoMOV
    elif "M4V" in ds_list:
        return VideoM4V
    #handle all the master image content models here
    elif "MASTER" in ds_list or "MASTER-COLORBAR" in ds_list:
        if "JP2" in ds_list:
            return JP2Image
        elif "JPG" in ds_list:
            return JPGImage
        elif "PNG" in ds_list:
            return PNGImage
        else:
            return MasterImage
    #now handle images by themselves, without a master
    elif "JP2" in ds_list:
        return JP2
    elif "JPG" in ds_list:
        return JPG
    elif "PNG" in ds_list:
        return PNG
    #other content types
    elif "PDF" in ds_list:
        return PDFDigitalObject
    elif "ZIP" in ds_list:
        return ZippedArchive
    elif "TEI" in ds_list:
        return TeiFile
    elif "DOC" in ds_list:
        return DocFile
    elif "JSON" in ds_list:
        return JSON
    elif "XML" in ds_list:
        return XmlFile
    else:
        if default_model == 'undetermined':
            return Undetermined
        else:
            return ImplicitSet


CONTENT_MODEL_BASE_PID = 'bdr-cmodel'
CONTENT_MODEL_BASE_URI = 'info:fedora/%s' % CONTENT_MODEL_BASE_PID

pagination = "http://library.brown.edu:hasPagination"
LIBNS = Namespace(URIRef("http://library.brown.edu/#"))


COMMON_METADATA_CONTENT_MODEL = "%s:commonMetadata" % CONTENT_MODEL_BASE_URI


class CommonMetadataDO(DigitalObject):
    CONTENT_MODELS = [COMMON_METADATA_CONTENT_MODEL]
    owning_collection = Relation(relsextns.isMemberOf, type="self")
    isPartOf = Relation(relsextns.isPartOf, type="self")
    page_number = Relation(LIBNS.hasPagination, ns_prefix={"bul-rel": LIBNS})

    rels_int = XmlDatastream(
        "RELS-INT",
        "Internal Datastream Relations",
        rels.RelsInt,
        defaults={
            'control_group': 'X',
            'format': 'info:fedora/fedora-system:FedoraRELSInt-1.0',
            'versionable': True,
        }
    )

    rightsMD = XmlDatastream('rightsMetadata', "Rights Metadata", rights.Rights,
                             defaults={
                                 'control_group': 'X',
                                 'format': 'http://cosimo.stanford.edu/sdr/metsrights/',
                                 'versionable': True,
                             }
                             )

    irMD = XmlDatastream('irMetadata', "Institutional Repository Metadata", irMetadata.IR,
                         defaults={
                             'control_group': 'X',
                             'format': 'http://dl.lib.brown.edu/md/irdata',
                             'versionable': True,
                         }
                         )
    mods = XmlDatastream('MODS', "MODS metadata", mods.Mods,
                         defaults={
                             'control_group': 'M',
                             'format': mods.MODS_NAMESPACE,
                             'versionable': True,
                         }
                         )
    dwc = XmlDatastream('DWC', "Darwincore metadata", darwincore.SimpleDarwinRecord,
                         defaults={
                             'control_group': 'M',
                             'format': darwincore.DWCNS,
                             'versionable': True,
                         }
                         )
    archive_mets = XmlDatastream('archiveMETS', "old METS metadata", mets.BDRMets,
                         defaults={
                             'control_group': 'M',
                             'format': mets.METS_NAMESPACE,
                             'versionable': True,
                         }
                         )

    def convert_mods_to_external(self):
        """Convert the mods datastream to be an external reference"""
        #del self.mods
        self.mods = XmlDatastream('MODS', "MODS metadata", mods.Mods,
                                  defaults={
                                      'control_group': 'E',
                                      'format': mods.MODS_NAMESPACE,
                                      'versionable': True,
                                  }
                                  )
        return self


IMPLICIT_SET_CONTENT_MODEL = '%s:implicit-set' % CONTENT_MODEL_BASE_URI

class ImplicitSet(CommonMetadataDO):
    CONTENT_MODELS = [IMPLICIT_SET_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


BDR_COLLECTION_CONTENT_MODEL = '%s:bdr-collection' % CONTENT_MODEL_BASE_URI

class BDRCollection(CommonMetadataDO):
    CONTENT_MODELS = [BDR_COLLECTION_CONTENT_MODEL, IMPLICIT_SET_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


MASTER_IMAGE_CONTENT_MODEL = '%s:masterImage' % CONTENT_MODEL_BASE_URI

class MasterImage(CommonMetadataDO):
    CONTENT_MODELS = [MASTER_IMAGE_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    master = FileDatastream("MASTER", "Master Image File",
                            defaults={
                                'versionable': True,
                                'control_group': 'M',
                                'mimetype': 'image/tiff',
                            }
                            )

    master_colorbar = FileDatastream("MASTER-COLORBAR", "Master Image File with the Colorbar",
                                     defaults={
                                         'versionable': True,
                                         'control_group': 'M',
                                         'mimetype': 'image/tiff',
                                     }
                                     )

    digital_negative = FileDatastream("DIGITAL-NEGATIVE", "Adobe DNG Digital Negative",
                                     defaults={
                                         'versionable': True,
                                         'control_group': 'M',
                                         'mimetype': 'image/tiff',
                                     }
                                     )

    thumbnail = FileDatastream("thumbnail", "Thumbnail Image",
                            defaults={
                                'versionable': True,
                                'control_group': 'M',
                                'mimetype': 'image/jpeg',
                            }
                            )

JP2_CONTENT_MODEL = '%s:jp2' % CONTENT_MODEL_BASE_URI

class JP2Image(MasterImage):
    CONTENT_MODELS = [JP2_CONTENT_MODEL, MASTER_IMAGE_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    jp2 = FileDatastream("JP2", "JP2 version of the MASTER image.  Suitable for further dissemination",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'image/jp2',
                         }
                         )

class JP2(JP2Image):
    CONTENT_MODELS = [JP2_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


JPG_CONTENT_MODEL = '%s:jpg' % CONTENT_MODEL_BASE_URI

class JPGImage(MasterImage):
    CONTENT_MODELS = [JPG_CONTENT_MODEL, MASTER_IMAGE_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    jpg = FileDatastream("jpg", "JPG version of the MASTER image. Suitable for further dissemination",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'image/jpeg',
                         }
                         )

class JPG(JPGImage):
    CONTENT_MODELS = [JPG_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


PNG_CONTENT_MODEL = '%s:png' % CONTENT_MODEL_BASE_URI

class PNGImage(MasterImage):
    CONTENT_MODELS = [PNG_CONTENT_MODEL, MASTER_IMAGE_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    png = FileDatastream("png", "PNG image",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'image/png',
                         }
                         )

class PNG(PNGImage):
    CONTENT_MODELS = [PNG_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


MOV_CONTENT_MODEL = '%s:mov' % CONTENT_MODEL_BASE_URI

class VideoMOV(CommonMetadataDO):
    CONTENT_MODELS = [MOV_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    mov = FileDatastream("mov", "Quicktime MOV video",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'video/quicktime',
                         }
                         )

M4V_CONTENT_MODEL = '%s:m4v' % CONTENT_MODEL_BASE_URI


class VideoM4V(CommonMetadataDO):
    CONTENT_MODELS = [M4V_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    m4v = FileDatastream("m4v", "M4V video",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'video/x-m4v',
                         }
                         )

MP4_CONTENT_MODEL = '%s:mp4' % CONTENT_MODEL_BASE_URI


class VideoMP4(CommonMetadataDO):
    CONTENT_MODELS = [MP4_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    mp4 = FileDatastream("mp4", "MP4 video",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'video/mp4',
                         }
                         )

PDF_CONTENT_MODEL = '%s:pdf' % CONTENT_MODEL_BASE_URI


class PDFDigitalObject(CommonMetadataDO):
    CONTENT_MODELS = [PDF_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    pdf = FileDatastream("PDF", "PDF Document",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/pdf',
                         }
                         )

AUDIO_MASTER_CONTENT_MODEL = '%s:audioMaster' % CONTENT_MODEL_BASE_URI


class AudioMaster(CommonMetadataDO):
    CONTENT_MODELS = [AUDIO_MASTER_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    
    audio_master = FileDatastream("AUDIO-MASTER", "Master Audio File",
                         defaults={
                            'versionable': True,
                            'control_group': 'M',
                            'mimetype': 'audio/wav',
                          }
                          )


MP3_CONTENT_MODEL = '%s:mp3' % CONTENT_MODEL_BASE_URI

class AudioMP3(AudioMaster):
    CONTENT_MODELS = [MP3_CONTENT_MODEL, AUDIO_MASTER_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    mp3 = FileDatastream("MP3", "MP3 Audio File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'audio/mpeg',
                         }
                         )

class MP3(AudioMP3):
    '''class for objects that have no audio_master, so they shouldn't have that cmodel'''
    CONTENT_MODELS = [MP3_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]


AIFF_CONTENT_MODEL = '%s:aiff' % CONTENT_MODEL_BASE_URI

class AudioAIFF(CommonMetadataDO):
    CONTENT_MODELS = [AIFF_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    aiff = FileDatastream("AIFF", "AIFF Audio File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'audio/aiff',
                         }
                         )

WAV_CONTENT_MODEL = '%s:wav' % CONTENT_MODEL_BASE_URI


class AudioWAV(CommonMetadataDO):
    CONTENT_MODELS = [WAV_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    wav = FileDatastream("WAV", "WAV Audio File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'audio/wav',
                         }
                         )

ZIP_CONTENT_MODEL = '%s:zip' % CONTENT_MODEL_BASE_URI


class ZippedArchive(CommonMetadataDO):
    CONTENT_MODELS = [ZIP_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    zip = FileDatastream("ZIP", "Zipped Archive",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/zip',
                         }
                         )

XML_CONTENT_MODEL = '%s:xml' % CONTENT_MODEL_BASE_URI

class XmlFile(CommonMetadataDO):
    CONTENT_MODELS = [XML_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    content = XmlDatastream("XML", "XML File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'text/xml',
                         }
                         )


TEI_CONTENT_MODEL = '%s:tei' % CONTENT_MODEL_BASE_URI

class TeiFile(CommonMetadataDO):
    CONTENT_MODELS = [TEI_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    tei = FileDatastream("TEI", "TEI File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/tei+xml',
                         }
                         )

DOC_CONTENT_MODEL = '%s:doc' % CONTENT_MODEL_BASE_URI


class DocFile(CommonMetadataDO):
    CONTENT_MODELS = [DOC_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    doc = FileDatastream("DOC", "Doc File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/msword',
                         }
                         )

STREAMING_CONTENT_MODEL = '%s:stream' % CONTENT_MODEL_BASE_URI


class StreamingFile(CommonMetadataDO):
    CONTENT_MODELS = [STREAMING_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    isDerivationOf = Relation(relsextns.isDerivationOf, type="self")
    stream_uri = Relation(LIBNS.hasStream, ns_prefix={"bul-rel": LIBNS})


ANNOTATION_CONTENT_MODEL = '%s:annotation' % CONTENT_MODEL_BASE_URI


class Annotation(CommonMetadataDO):
    CONTENT_MODELS = [ANNOTATION_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    isAnnotationOf = Relation(relsextns.isAnnotationOf, type="self")

    content = FileDatastream("content", "Annotation File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'text/xml',
                         }
                         )

JSON_CONTENT_MODEL = '%s:json' % CONTENT_MODEL_BASE_URI

class JSON(CommonMetadataDO):
    CONTENT_MODELS = [JSON_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    content = FileDatastream("content", "JSON file",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/javascript',
                         }
                         )

UNDETERMINED_CONTENT_MODEL = '%s:undetermined' % CONTENT_MODEL_BASE_URI

class Undetermined(CommonMetadataDO):
    CONTENT_MODELS = [UNDETERMINED_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    content = FileDatastream("content", "Any application file",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/octet-stream',
                         }
                         )

BLOB_CONTENT_MODEL = '%s:blob' % CONTENT_MODEL_BASE_URI

class Blob(CommonMetadataDO):
    CONTENT_MODELS = [BLOB_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    blob = FileDatastream("BLOB", "Any application file",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/octet-stream',
                         }
                         )

