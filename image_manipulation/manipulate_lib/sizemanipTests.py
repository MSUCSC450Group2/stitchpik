import unittest
from PIL import Image
import sizemanip

class sizemanipTest(unittest.TestCase):

    def test_newSize(self):
        # Tests for a valid new width and new height
        im = Image.open("/home/lefty/stitchpik/image_manipulation/static/image_manipulation/img/bubblegum.jpg")
        self.assertRaises(ValueError,sizemanip.reSize,im,(-500,500))
        self.assertRaises(ValueError,sizemanip.reSize,im,(500,-500))
        self.assertRaises(ValueError,sizemanip.reSize,im,(0,500))
        self.assertRaises(ValueError,sizemanip.reSize,im,(500,0))

    def testRatio(self):
        # Tests for incorrect ratio type and values
        im = Image.open("/home/lefty/stitchpik/image_manipulation/static/image_manipulation/img/bubblegum.jpg")
        self.assertRaises(TypeError,sizemanip.reSize,im,50)
        self.assertRaises(IndexError,sizemanip.reSize,im,"fred is fat")
        self.assertRaises(ValueError,sizemanip.reSize,im,"fr:ed is fat")
        self.assertRaises(ValueError,sizemanip.reSize,im,"-16:9")
        self.assertRaises(ValueError,sizemanip.reSize,im,"16:-9")

    def testRandomOption(self):
        im = Image.open("/home/lefty/stitchpik/image_manipulation/static/image_manipulation/img/bubblegum.jpg")
        self.assertRaises(TypeError,sizemanip.reSize,im,[500,500])
        self.assertRaises(TypeError,sizemanip.reSize,im,{500,600})
             


if __name__ == '__main__':
    unittest.main()
        
        
        
