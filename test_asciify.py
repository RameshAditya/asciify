import unittest
import asciify

class Test_get_name(unittest.TestCase):
    def test_get_name_from_path(self):
        # sould return string
        self.assertEqual(type(asciify.get_name_from_path("photo.jpg")),type(str("a")))
        
        # different paths
        self.assertEqual(asciify.get_name_from_path("photo.jpg"),"photo")
        self.assertEqual(asciify.get_name_from_path("dir1/photo.jpg"),"photo")
        self.assertEqual(asciify.get_name_from_path("./dir1/dir2/dir3/photo.jpg"),"photo")
        
        # different endings should not matter
        self.assertEqual(asciify.get_name_from_path("./dir1/dir2/dir3/photo.long_ending"),"photo")
        self.assertEqual(asciify.get_name_from_path("photo.png"),"photo")
        self.assertEqual(asciify.get_name_from_path("photo.jpeg"),"photo")


        

if __name__ == '__main__':
    unittest.main()