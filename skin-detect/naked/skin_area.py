import os
from PIL import Image


class SkinArea(object):
    offsets = [
        [-1, -1], [0, -1], [1, -1],
        [-1,  0], [0,  0], [1,  0],
        [-1,  1], [0,  1], [1,  1],
    ]
    conv_mode = {
        'rgb1': 'RGB',
        'rgb2': 'RGB',
        'hsv1': 'HSV',
        'ycbcr1': 'YCbCr',
    }

    def __init__(self, imgpath):
        self.imgpath = imgpath
        self.image = Image.open(imgpath)
        self.width, self.height = self.image.size

    def parse(self, algo, mask=False):
        connected = self.detect_skin(algo)
        areas = self.detect_connect(connected)
        if self.analyse(areas):
            result = 'Naked'
        else:
            result = 'Normal'
        print(f'{self.imgpath}: {result}')
        if mask:
            self.save_mask(areas, result)

    def save_mask(self, areas, result):
        maskimage = Image.new('RGB', (self.width, self.height))
        pixels = maskimage.load()
        for area in areas:
            for (x, y) in area:
                pixels[x, y] = (255, 255, 255)
        dirname = os.path.dirname(self.imgpath)
        basename = os.path.basename(self.imgpath)
        filename, extname = os.path.splitext(basename)
        maskname = f'{filename}_{result}{extname}'
        maskfile = os.path.join(dirname, maskname)
        maskimage.save(maskfile)

    def analyse(self, areas):
        if len(areas) < 3:
            print('number of skin area is less than 3')
            return False
        areas = sorted(areas, key=lambda s: len(s), reverse=True)
        total_skin = float(sum([len(s) for s in areas]))
        if total_skin / (self.width * self.height) < 0.15:
            print('rate of skin area is less than 15%')
            return False
        if len(areas[0]) / total_skin < 0.45:
            print('top skin rate is less than 45%')
            return False
        if len(areas) > 60:
            print('number of skin areas is more than 60')
            return False
        return True

    def detect_skin(self, algo='ycbcr1'):
        connected = {}
        pixels = self.image.load()
        mode = self.conv_mode[algo]
        handler = getattr(self, f'threshold_{algo}')
        for y in range(self.height):
            for x in range(self.width):
                if mode == 'RGB':
                    pixel = pixels[x, y]
                else:
                    convert = getattr(self, f'_to_{mode}')
                    pixel = convert(*pixels[x, y])
                if handler(*pixel):
                    connected[x, y] = 1
                else:
                    connected[x, y] = 0
        return connected

    def detect_connect(self, connected):
        arid = 2
        areas = []
        for y in range(self.height):
            for x in range(self.width):
                if connected[x, y] == 1:
                    area = self.travel(arid, connected, x, y)
                    if len(area) > 30:
                        arid += 1
                        areas.append(area)
        return areas

    def travel(self, arid, connected, x, y):
        area = []
        stk = []
        stk.append((x, y))
        while len(stk) > 0:
            (i, j) = stk.pop()
            area.append((i, j))
            neighbors = self.neighbors(i, j)
            for (ni, nj) in neighbors:
                if connected[ni, nj] == 1:
                    stk.append((ni, nj))
                    connected[ni, nj] = arid
        return area

    def neighbors(self, i, j):
        ns = set()
        for off in self.offsets:
            x = min(max(0, i + off[0]), self.width - 1)
            y = min(max(0, j + off[1]), self.height - 1)
            ns.add((x, y))
        ns.remove((i, j))
        return list(ns)

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
        nr, ng, nb = self._to_Norm(r, g, b)
        return nr / ng > 1.185 \
            and float(r * b) / ((r + g + b)**2) > 0.107 \
            and float(r * g) / ((r + g + b)**2) > 0.112

    def threshold_hsv1(self, h, s, v):
        return 7 <= h <= 20 \
            and 28 <= s < 256 \
            and 50 <= v <= 256

    def threshold_ycbcr1(self, y, cb, cr):
        return 97.5 <= cb <= 142.5 \
            and 134 <= cr <= 176

    def _to_Norm(self, r, g, b):
        r = r or 0.0001
        g = g or 0.0001
        b = b or 0.0001
        _sum = float(r + g + b)
        return (r / _sum, g / _sum, b / _sum)

    def _to_HSV(self, r, g, b):
        pass

    def _to_YCbCr(self, r, g, b):
        y = 0.299*r + 0.587*g + 0.114*b
        cb = 128 - 0.168736*r - 0.331364*g + 0.5*b
        cr = 128 + 0.5*r - 0.418688*g - 0.081312*b
        return y, cb, cr
