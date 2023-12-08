import unittest
from images import find_image_dir
from datetime import datetime
from os import path

class TestFindImageDir(unittest.TestCase):
    def test_something(self):
        dir_name = '01_08_2021_Test'
        file_path = path.join(dir_name, "IMG_1234.png")
        image_dir_found = find_image_dir(file_path, datetime.strptime("01_08_2021", "%d_%m_%Y"))
        expected = "2021_08_01_Test"
        self.assertEqual(expected, image_dir_found)

    def test_date_format_2(self):
        dir_name = '2020-05-31_test2'
        file_path = path.join(dir_name, "IMG_1234.png")
        image_dir_found = find_image_dir(file_path, datetime.strptime("2020_05_31", "%Y_%m_%d"))
        expected = '2020_05_31_test2'
        self.assertEqual(expected, image_dir_found)

    def test_date_format_3(self):
        dir_name = 'Test Test3'
        file_path = path.join(dir_name, "IMG_20190422_140133.jpg")
        image_dir_found = find_image_dir(file_path, datetime.strptime("2019_04_22", "%Y_%m_%d"))
        expected = '2019_04_22_Test_Test3'
        self.assertEqual(expected, image_dir_found)


if __name__ == '__main__':
    unittest.main()
