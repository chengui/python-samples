import click
from simple_http.server import SimpleHTTPServer

@click.command()
@click.option('-h', '--host', default='127.0.0.1', help='address ip, default to 127.0.0.1')
@click.option('-p', '--port', default=8080, help='address port, default to 8080')
@click.option('-d', '--dir', default='.', help='root directory, default to $PWD')
def cli(host, port, dir):
    server = SimpleHTTPServer((host, port), dir)
    print('Web server started at {}:{}'.format(host, port))
    server.serve_forever()

if __name__ == '__main__':
    cli()

