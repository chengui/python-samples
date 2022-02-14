from PIL import Image

class SimpleConverter(object):
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.  ")

    def convert_fixed(self, picture, width, height):
        im = Image.open(picture)
        im = im.resize((width, height), Image.NEAREST)
        txt = ""
        for j in range(height):
            for i in range(width):
                txt += self.get_char(*im.getpixel((i, j)))
            txt += '\n'
        return txt

    def convert_scale(self, picture, scale=100):
        im = Image.open(picture)
        width = int(im.size[0] * scale / 100)
        height = int(im.size[1] * scale / 100)
        im = im.resize((width, height), Image.NEAREST)
        txt = ""
        for j in range(height):
            for i in range(width):
                txt += self.get_char(*im.getpixel((i, j)))
            txt += '\n'
        return txt

    def get_char(self, r, g, b, alpha=256):
        if alpha == 0:
            return ' '
        # gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        idx = gray / (256.0 + 1) * len(self.ascii_char)
        return self.ascii_char[int(idx)]

