import unittest
from bdrcmodels import models


class ChooseCmodelTest(unittest.TestCase):

    def test_ia(self):
        ds_list = ['PDF', 'IA_DC', 'META_MRC', 'BW_PDF', 'gif', 'txt']
        self.assertEqual(models.choose_content_model(ds_list), models.InternetArchive)
        ds_list = ['MARC_XML', 'METASOURCE_XML', 'META_MRC', 'IA_DC', 'XTAR', 'SCANDATA_XML', 'xml', 'META_XML']
        self.assertEqual(models.choose_content_model(ds_list), models.InternetArchive)

    def test_image_compound(self):
        ds_list = ['highres', 'lowres']
        self.assertEqual(models.choose_content_model(ds_list), models.ImageCompound)

    def test_master_jp2(self):
        ds_list = ['MASTER', 'highres_jp2', 'lowres']
        self.assertEqual(models.choose_content_model(ds_list), models.ImageCompound)

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

    def test1(self):
        ds_list = ['pdf']
        self.assertEqual(models.choose_content_model(ds_list), models.PDFDigitalObject)


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
