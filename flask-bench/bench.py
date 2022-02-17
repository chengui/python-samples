import time
import click
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


tmpl = """
Document Path:        {path}
Concurrency Level:    {workers}
Time taken for tests: {elapse:.3f} seconds
Complete requests:    {completed}
Failed requests:      {failed}
Requests per second:  {rps:.2f} [#/sec] (mean)
"""

def request(url):
    r = requests.get(url)
    return r.status_code

@click.command()
@click.option('-n', '--requests', type=int, help='requests number')
@click.option('-c', '--workers', type=int, help='workers number')
@click.argument('url')
def cli(requests, workers, url):
    with ThreadPoolExecutor(max_workers=workers) as p:
        t0 = time.time()
        tasks = [p.submit(request, url) for _ in range(requests)]
        responses = [f.result() for f in as_completed(tasks)]
        elapse = time.time() - t0
        completed = len(list(filter(lambda x: x == 200, responses)))
        print(tmpl.format(path=url, workers=workers, elapse=elapse, completed=completed,
                          failed=requests-completed, rps=completed/elapse))

if __name__ == '__main__':
    cli()
