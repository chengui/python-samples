import click
from ngram import predict


@click.command()
@click.option('-n', '--ngram', type=int, default=3, help='set ngram lenght')
@click.option('-t', '--text', default='', help='predict string')
def cli(ngram, text):
    print('Predicted Languange: {}'.format(predict(text, ngram)))

if __name__ == '__main__':
    cli()
