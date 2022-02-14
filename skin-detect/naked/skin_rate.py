import os
from PIL import Image


class SkinRate(object):
    conv_mode = {
        'rgb1': 'RGB',
        'rgb2': 'RGB',
        'hsv1': 'HSV',
        'hsv2': 'HSV',
        'hsv3': 'HSV',
        'ycbcr1': 'YCbCr',
        'ycbcr2': 'YCbCr',
        'ycbcr3': 'YCbCr',
    }
    def __init__(self, imgpath):
        self.imgpath = imgpath
        self.image = Image.open(imgpath)
        self.width, self.height = self.image.size

    def parse(self, algo, mask=False, thres=0.1):
        if algo not in self.conv_mode:
            raise TypeError('algo not supported')

        mode = self.conv_mode[algo]
        if mode == 'RGB':
            image = self.image
        else:
            image = self.image.convert(mode)

        handler = getattr(self, f'threshold_{algo}')

        skin = 0
        pixels = image.load()
        if mask:
            maskimage = self.image
            maskpixels = maskimage.load()
        for y in range(self.height):
            for x in range(self.width):
                is_skin = handler(*pixels[x, y])
                if is_skin:
                    skin += 1
                if mask:
                    if is_skin:
                        maskpixels[x, y] = 255, 255, 255
                    else:
                        maskpixels[x, y] = 0, 0, 0
        if skin / (self.width * self.height) > thres:
            result = 'Naked'
        else:
            result = 'Normal'
        print(f'{self.imgpath}: {result}')
        if mask:
            dirname = os.path.dirname(self.imgpath)
            basename = os.path.basename(self.imgpath)
            filename, extname = os.path.splitext(basename)
            maskname = f'{filename}_{result}{extname}'
            maskfile = os.path.join(dirname, maskname)
            maskimage.save(maskfile)

    def threshold_rgb1(self, r, g, b):
        return r > 95 \
            and g > 40 \
            and g < 100 \
            and b > 20 \
            and max([r, g, b]) - min([r, g, b]) > 15 \
            and abs(r - g) > 15 \
            and r > g \
            and r > b

    def threshold_rgb2(self, r, g, b):
        nr = r / (r + g + b + 0.1)
        ng = g / (r + g + b + 0.1)
        nb = b / (r + g + b + 0.1)
        return nr / (ng + 0.1) > 1.185 \
            and r * b / (r + g + b)**2 > 0.107 \
            and r * g / (r + g + b)**2 > 0.112

    def threshold_hsv1(self, h, s, v):
        return 0 <= h <= 0.25 \
            and 0.15 <= s < 0.9 \
            and 0.2 <= v <= 0.9

    def threshold_hsv2(self, h, s, v):
        return 0 < h < 35 \
            and 0.23 < s < 0.68

    def threshold_hsv3(self, h, s, v):
        return 7 <= h <= 20 \
            and 28 <= s < 256 \
            and 50 <= v <= 256

    def threshold_ycbcr1(self, y, cb, cr):
        return 97.5 <= cb <= 142.5 \
            and 134 <= cr <= 176

    def threshold_ycbcr2(self, y, cb, cr):
        return 77 <= cb <= 127 \
            and 134 <= cr <= 176

    def threshold_ycbcr3(self, y, cb, cr):
        return 80 <= cb <= 120 \
            and 133 <= cr <= 173
