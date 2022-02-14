import click
from ascii_art.simple import SimpleConverter


@click.group()
def cli():
    pass

@click.command()
@click.option('-s', '--scale', type=click.IntRange(1, 100), default=100, help='image scale (1~100)')
@click.option('-w', '--width', default=0, help='image width')
@click.option('-h', '--height', default=0, help='image height')
@click.option('-o', '--out', default='0.txt', help='output file')
@click.argument('picture')
def simple(scale, width, height, out, picture):
    simple_conv = SimpleConverter()
    if width > 0 and height > 0:
        txt = simple_conv.convert_fixed(picture, width, height)
    else:
        txt = simple_conv.convert_scale(picture, scale)
    with open(out, 'w') as wf:
        wf.write(txt)

cli.add_command(simple)

if __name__ == '__main__':
    cli()


