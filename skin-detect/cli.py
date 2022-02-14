#!/usr/bin/env python3
import os
import click
from naked.skin_rate import SkinRate
from naked.skin_area import SkinArea

skin_algo = [
    'rgb1',
    'rgb2',
    'hsv1',
    'hsv2',
    'hsv3',
    'ycbcr1',
    'ycbcr2',
    'ycbcr3',
]

@click.group()
def cli():
    pass

@click.command('skinrate')
@click.option('-a', '--algo', type=click.Choice(skin_algo), default='rgb1', help='skin threshold algorithm')
@click.option('-m', '--mask', type=click.BOOL, default=False, help='save skin mask image')
@click.option('-t', '--thres', type=click.IntRange(0, 100), default=30, help='threshold of skin rate')
@click.argument('image')
def skinrate(algo, mask, thres, image):
    if not os.path.exists(image):
        return
    skin = SkinRate(image)
    skin.parse(algo, mask, thres / 100.)

@click.command('skinarea')
@click.option('-a', '--algo', type=click.Choice(skin_algo), default='rgb1', help='skin threshold algorithm')
@click.option('-m', '--mask', type=click.BOOL, default=False, help='save skin mask image')
@click.argument('image')
def skinarea(algo, mask, image):
    if not os.path.exists(image):
        return
    skin = SkinArea(image)
    skin.parse(algo, mask)

cli.add_command(skinrate)
cli.add_command(skinarea)

if __name__ == '__main__':
    cli()

