import unittest
from bdrcmodels import models


class ChooseCmodelTest(unittest.TestCase):

    def test_empty_ds_list(self):
        ds_list = []
        self.assertEqual(models.choose_content_model(ds_list), models.ImplicitSet)

    def test_default_model(self):
        ds_list = []
        self.assertEqual(models.choose_content_model(ds_list, default_model='undetermined'), models.Undetermined)

    def test1(self):
        ds_list = ['pdf']
        self.assertEqual(models.choose_content_model(ds_list), models.PDFDigitalObject)

if __name__ == '__main__':
    unittest.main()
    sys.exit(0)
