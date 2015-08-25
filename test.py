import unittest
from bdrcmodels import models


class ChooseCmodelTest(unittest.TestCase):

    def test_ia(self):
        ds_list = ['PDF', 'IA_DC', 'BW_PDF', 'gif', 'txt']
        self.assertEqual(models.choose_content_model(ds_list), models.InternetArchive)

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

if __name__ == '__main__':
    unittest.main()
    sys.exit(0)
