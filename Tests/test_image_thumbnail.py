from PIL import Image

from .helper import PillowTestCase, fromstring, hopper, tostring


class TestImageThumbnail(PillowTestCase):
    def test_sanity(self):
        im = hopper()
        self.assertIsNone(im.thumbnail((100, 100)))

        self.assertEqual(im.size, (100, 100))

    def test_aspect(self):
        im = Image.new("L", (128, 128))
        im.thumbnail((100, 100))
        self.assertEqual(im.size, (100, 100))

        im = Image.new("L", (128, 256))
        im.thumbnail((100, 100))
        self.assertEqual(im.size, (50, 100))

        im = Image.new("L", (128, 256))
        im.thumbnail((50, 100))
        self.assertEqual(im.size, (50, 100))

        im = Image.new("L", (256, 128))
        im.thumbnail((100, 100))
        self.assertEqual(im.size, (100, 50))

        im = Image.new("L", (256, 128))
        im.thumbnail((100, 50))
        self.assertEqual(im.size, (100, 50))

        im = Image.new("L", (128, 128))
        im.thumbnail((100, 100))
        self.assertEqual(im.size, (100, 100))

        im = Image.new("L", (256, 162))  # ratio is 1.5802469136
        im.thumbnail((33, 33))
        self.assertEqual(im.size, (33, 21))  # ratio is 1.5714285714

        im = Image.new("L", (162, 256))  # ratio is 0.6328125
        im.thumbnail((33, 33))
        self.assertEqual(im.size, (21, 33))  # ratio is 0.6363636364

    def test_no_resize(self):
        # Check that draft() can resize the image to the destination size
        with Image.open("Tests/images/hopper.jpg") as im:
            im.draft(None, (64, 64))
            self.assertEqual(im.size, (64, 64))

        # Test thumbnail(), where only draft() is necessary to resize the image
        with Image.open("Tests/images/hopper.jpg") as im:
            im.thumbnail((64, 64))
            self.assertEqual(im.size, (64, 64))

    def test_DCT_scaling_edges(self):
        # Make an image with red borders and size (N * 8) + 1 to cross DCT grid
        im = Image.new("RGB", (257, 257), "red")
        im.paste(Image.new("RGB", (255, 255)), (1, 1))

        thumb = fromstring(tostring(im, "JPEG", quality=99, subsampling=0))
        thumb.thumbnail((32, 32), Image.BICUBIC)

        ref = im.resize((32, 32), Image.BICUBIC)
        self.assert_image_similar(thumb, ref, 2)
