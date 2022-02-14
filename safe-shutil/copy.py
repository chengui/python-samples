import click
from safe_shutil import safe_copy


@click.command()
@click.option('-i', '--ignore-patterns', default=None, help='ignore patterns')
@click.argument('src')
@click.argument('dst')
def cli(src, dst, ignore_patterns):
    safe_copy(src, dst, ignore_patterns)


if __name__ == '__main__':
    cli()


