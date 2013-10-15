from eulfedora.models import DigitalObject, FileDatastream, XmlDatastream, Relation
from bdrxml import rights
from bdrxml import irMetadata
from bdrxml import mods
from bdrxml import mets
from bdrxml import rels
from rdflib import URIRef
from rdflib.namespace import Namespace
from eulfedora.rdfns import relsext as relsextns


def choose_content_model(ds_list):
    """Chooses the appropriate content model based on the contents of the list of datastream names"""
    if "MP3" in ds_list:
        return AudioMP3
    elif "MP4" in ds_list:
        return VideoMP4
    elif "MOV" in ds_list:
        return VideoMOV
    elif "M4V" in ds_list:
        return VideoM4V
    elif "PDF" in ds_list:
        return PDFDigitalObject
    elif "JP2" in ds_list:
        return JP2Image
    elif "JPG" in ds_list:
        return JPGImage
    elif "MASTER-COLORBAR" in ds_list:
        return MasterImage
    elif "MASTER" in ds_list:
        return MasterImage
    elif "ZIP" in ds_list:
        return ZippedArchive
    elif "TEI" in ds_list:
        return TeiFile
    elif "DOC" in ds_list:
        return DocFile
    elif "PNG" in ds_list:
        return PNGImage
    else:
        return ImplicitSet


def get_cmodel_info(extension=None, content_type=None):
    #this is a function for a single file upload for the APIs
    #defaults to Undetermined cmodel
    cmodel = Undetermined
    content_member_name = 'content'
    content_ds_name = 'content'
    if extension:
        extension = extension.lower()
    if content_type:
        content_type = content_type.lower()
    if extension == 'pdf' or content_type == 'application/pdf':
        cmodel = PDFDigitalObject
        content_member_name = 'pdf'
        content_ds_name = 'PDF'
    elif extension == 'm4v':
        cmodel = VideoM4V
        content_member_name = 'm4v'
        content_ds_name = 'm4v'
    elif extension == 'mov':
        cmodel = VideoMOV
        content_member_name = 'mov'
        content_ds_name = 'mov'
    elif extension == 'doc':
        cmodel = DocFile
        content_member_name = 'doc'
        content_ds_name = 'DOC'
    elif extension == 'mp3':
        cmodel = AudioMP3
        content_member_name = 'mp3'
        content_ds_name = 'MP3'
    elif extension == 'jpg':
        cmodel = JPG
        content_member_name = 'jpg'
        content_ds_name = 'jpg'
    elif extension == 'jp2':
        cmodel = JP2
        content_member_name = 'jp2'
        content_ds_name = 'JP2'
    elif content_type == 'application/tei+xml':
        cmodel = TeiFile
        content_member_name = 'tei'
        content_ds_name = 'TEI'
    return (cmodel, content_member_name, content_ds_name)


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


LEGACY_METADATA_CONTENT_MODEL = "%s:legacyMetadata" % CONTENT_MODEL_BASE_URI

class LegacyMetadataDO(DigitalObject):
    CONTENT_MODELS = [LEGACY_METADATA_CONTENT_MODEL]
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

    mets = XmlDatastream('METS', "METS metadata", mets.BDRMets,
                         defaults={
                             'control_group': 'M',
                             'format': mets.METS_NAMESPACE,
                             'versionable': True,
                         }
                         )

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

class JP2(CommonMetadataDO):
    CONTENT_MODELS = [JP2_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    jp2 = FileDatastream("JP2", "JP2 image.",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'image/jp2',
                         }
                         )


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

class JPG(CommonMetadataDO):
    CONTENT_MODELS = [JPG_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
    jpg = FileDatastream("jpg", "JPG image.",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'image/jpeg',
                         }
                         )


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
class PDFLegacy(LegacyMetadataDO):
    CONTENT_MODELS = [PDF_CONTENT_MODEL, LEGACY_METADATA_CONTENT_MODEL]

    pdf = FileDatastream("PDF", "PDF Document",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/pdf',
                         }
                         )

MP3_CONTENT_MODEL = '%s:mp3' % CONTENT_MODEL_BASE_URI


class AudioMP3(CommonMetadataDO):
    CONTENT_MODELS = [MP3_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]

    mp3 = FileDatastream("MP3", "MP3 Audio File",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'audio/mpeg',
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

class BlobLegacy(LegacyMetadataDO):
    CONTENT_MODELS = [BLOB_CONTENT_MODEL, LEGACY_METADATA_CONTENT_MODEL]

    blob = FileDatastream("BLOB", "Any application file",
                         defaults={
                             'versionable': True,
                             'control_group': 'M',
                             'mimetype': 'application/octet-stream',
                         }
                         )


IMPLICIT_SET_CONTENT_MODEL = '%s:implicit-set' % CONTENT_MODEL_BASE_URI


class ImplicitSet(CommonMetadataDO):
    CONTENT_MODELS = [IMPLICIT_SET_CONTENT_MODEL, COMMON_METADATA_CONTENT_MODEL]
