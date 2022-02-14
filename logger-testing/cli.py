import click
from logger.consolelog import test as test_consolelog
from logger.coloredlog import test as test_coloredlog
from logger.teelog import test as test_teelog


@click.command()
@click.option('-t', '--test', default='console', help='logger test type')
def cli(test):
    mapping = {
        'console': test_consolelog,
        'colored': test_coloredlog,
        'tee': test_teelog,
    }
    if test in mapping:
        mapping[test]()
    else:
        click.echo('test not found!')


if __name__ == '__main__':
    cli()
