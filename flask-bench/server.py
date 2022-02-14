import click
from subprocess import Popen


mapping = {
    'flask': 'FLASK_APP=flask_app.app python -m flask run --no-reload --with-threads --host 0.0.0.0 --port {port}',
    'gevent': 'python flask_app/gevent_wsgi.py {port}',
    'gunicorn': 'gunicorn --workers {workers} --threads {threads} --bind 0.0.0.0:{port} flask_app.app:app',
    'gunicorn-gevent': 'gunicorn --worker-class gevent --workers {workers} --bind 0.0.0.0:{port} flask_app.patched:app',
    'uwsgi': 'uwsgi --master --workers {workers} --threads {threads} --protocol http --socket 0.0.0.0:{port} --module flask_app.app:app',
    'uwsgi-gevent': 'uwsgi --master --single-interpreter --workers {workers} --gevent {threads} --protocol http --socket 0.0.0.0:{port} --module flask_app.patched:app',
}

@click.command()
@click.option('-p', '--port', type=int, default=8080, help='server port')
@click.option('-w', '--workers', type=int, default=4, help='workers number')
@click.option('-t', '--threads', type=int, default=1000, help='threads number')
@click.argument('serve', type=click.Choice(mapping.keys()))
def cli(serve, port, workers, threads):
    if serve not in mapping:
        return click.echo('serve not found.')
    cmdline = mapping[serve].format(port=port, workers=workers, threads=threads)
    p = Popen(cmdline, shell=True)
    p.wait()


if __name__ == '__main__':
    cli()
