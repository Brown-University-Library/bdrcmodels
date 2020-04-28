import unittest
from bdrcmodels import models


class GetDsIdTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(models.get_dsid_from_filename('test.xyzzz'), None)
        self.assertEqual(models.get_dsid_from_filename('test.jpg'), 'JPG')
        self.assertEqual(models.get_dsid_from_filename('jpg'), 'JPG')
        self.assertEqual(models.get_dsid_from_filename('test.png'), 'PNG')
        self.assertEqual(models.get_dsid_from_filename('test.mov'), 'MOV')
        self.assertEqual(models.get_dsid_from_filename('test.avi'), 'AVI')
        self.assertEqual(models.get_dsid_from_filename('test.wav'), 'AUDIO-MASTER')
        self.assertEqual(models.get_dsid_from_filename('test.aiff'), 'AUDIO-MASTER')
        self.assertEqual(models.get_dsid_from_filename('test.tiff'), 'MASTER')


class GetMimetypeTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(models.get_mimetype_from_filename('test.xyzzz'), None)
        self.assertEqual(models.get_mimetype_from_filename('test.jpg'), 'image/jpeg')
        self.assertEqual(models.get_mimetype_from_filename('jpg'), 'image/jpeg')
        self.assertEqual(models.get_mimetype_from_filename('test.tif'), 'image/tiff')
        self.assertEqual(models.get_mimetype_from_filename('test.tiff'), 'image/tiff')
        self.assertEqual(models.get_mimetype_from_filename('test.jp2'), 'image/jp2')
        self.assertEqual(models.get_mimetype_from_filename('test.dng'), 'image/x-adobe-dng')
        self.assertEqual(models.get_mimetype_from_filename('test.png'), 'image/png')
        self.assertEqual(models.get_mimetype_from_filename('test.svg'), 'image/svg+xml')
        self.assertEqual(models.get_mimetype_from_filename('test.pdf'), 'application/pdf')
        self.assertEqual(models.get_mimetype_from_filename('test.zip'), 'application/zip')
        self.assertEqual(models.get_mimetype_from_filename('test.tar'), 'application/x-tar')
        self.assertEqual(models.get_mimetype_from_filename('test.mp3'), 'audio/mpeg')
        self.assertEqual(models.get_mimetype_from_filename('test.odt'), 'application/vnd.oasis.opendocument.text')
        self.assertEqual(models.get_mimetype_from_filename('test.mov'), 'video/quicktime')
        self.assertEqual(models.get_mimetype_from_filename('test.mkv'), 'video/x-matroska')
        self.assertEqual(models.get_mimetype_from_filename('test.tei'), 'application/tei+xml')
        self.assertEqual(models.get_mimetype_from_filename('test.tei.xml'), 'application/tei+xml')


class ChooseCmodelTest(unittest.TestCase):

    def test_ia(self):
        ds_list = ['PDF', 'IA_DC', 'META_MRC', 'BW_PDF', 'gif', 'txt']
        self.assertEqual(models.choose_content_model(ds_list), models.InternetArchive)
        ds_list = ['MARC_XML', 'METASOURCE_XML', 'META_MRC', 'IA_DC', 'XTAR', 'SCANDATA_XML', 'xml', 'META_XML']
        self.assertEqual(models.choose_content_model(ds_list), models.InternetArchive)

    def test_image_compound(self):
        ds_list = ['highres', 'lowres']
        self.assertEqual(models.choose_content_model(ds_list), models.Image)

    def test_master_jp2(self):
        ds_list = ['MASTER', 'highres_jp2', 'lowres']
        self.assertEqual(models.choose_content_model(ds_list), models.Image)

    def test_audio(self):
        ds_list = ['AUDIO-MASTER']
        self.assertEqual(models.choose_content_model(ds_list), models.Audio)
        ds_list = ['AUDIO-MASTER', 'MP3']
        self.assertEqual(models.choose_content_model(ds_list), models.Audio)

    def test_video(self):
        ds_list = ['VIDEO-MASTER']
        self.assertEqual(models.choose_content_model(ds_list), models.Video)
        ds_list = ['VIDEO-MASTER', 'MP4']
        self.assertEqual(models.choose_content_model(ds_list), models.Video)

    def test_ppt(self):
        ds_list = ['ppt']
        self.assertEqual(models.choose_content_model(ds_list), models.PptFile)
        ds_list = ['pptx']
        self.assertEqual(models.choose_content_model(ds_list), models.PptxFile)

    def test_empty_ds_list(self):
        ds_list = []
        self.assertEqual(models.choose_content_model(ds_list), models.ImplicitSet)

    def test_default_model(self):
        ds_list = []
        self.assertEqual(models.choose_content_model(ds_list, default_model='undetermined'), models.Undetermined)

    def test_pdf(self):
        ds_list = ['pdf']
        self.assertEqual(models.choose_content_model(ds_list), models.PDFDigitalObject)

    def test_xlsx_csv(self):
        ds_list = ['XLSX', 'CSV']
        self.assertEqual(models.choose_content_model(ds_list), models.CsvFile)

    def test_xls_csv(self):
        ds_list = ['XLS', 'CSV']
        self.assertEqual(models.choose_content_model(ds_list), models.CsvFile)

    def test_tar_gzip(self):
        ds_list = ['GZIP']
        self.assertEqual(models.choose_content_model(ds_list), models.GzipArchive)
        ds_list = ['TAR']
        self.assertEqual(models.choose_content_model(ds_list), models.TarArchive)


class CmodelsTest(unittest.TestCase):

    def test_internet_archive(self):
        cmodels = models.InternetArchive.CONTENT_MODELS
        self.assertTrue(models.COMMON_METADATA_CONTENT_MODEL in cmodels)
        self.assertTrue('%s:internet_archive' % models.CONTENT_MODEL_BASE_URI in cmodels)

    def test_ppt(self):
        cmodels = models.PptFile.CONTENT_MODELS
        self.assertTrue(models.COMMON_METADATA_CONTENT_MODEL in cmodels)
        self.assertTrue('%s:ppt' % models.CONTENT_MODEL_BASE_URI in cmodels)

    def test_pptx(self):
        cmodels = models.PptxFile.CONTENT_MODELS
        self.assertTrue(models.COMMON_METADATA_CONTENT_MODEL in cmodels)
        self.assertTrue('%s:pptx' % models.CONTENT_MODEL_BASE_URI in cmodels)


if __name__ == '__main__':
    unittest.main()
    sys.exit(0)

