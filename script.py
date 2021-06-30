import os, re
from requests_html import HTMLSession
from readability import Readability
import git
from functools import reduce

def script():
    # replace these filepaths with your own
    repo_path = '/home/zuchka/grafana/'
    docs_path = '/home/zuchka/grafana/docs/sources/'
    url_path  = 'https://grafana.com/docs/grafana/latest/'
    md_suffix = re.compile(".*md$")

    # update grafana repo
    repo = git.cmd.Git(repo_path)
    repo.pull()

    # search through docs, find markdown files, and generate urls
    all_files  = []

    for root, directories, files in os.walk(docs_path, topdown=False):
        for name in files:
            all_files.append(os.path.join(root, name))

    md_files = list(filter(md_suffix.match, all_files))
    strip_md =  map(lambda x: re.sub(r'\.md$|_index\.md$|index\.md', '', x), md_files)
    urls     =  map(lambda x: re.sub(r'.*sources/', url_path, x), strip_md)

    # scrape urls, extract text (everything inside <p> tags, minus code), and analyze
    export = []
    values = []

    for url in urls:
        session = HTMLSession()
        page    = session.get(url)
        ptag    = page.html.find('p')
        ptags   = []
        
        for i in range(len(ptag)):
            x = ptag[i].text
            ptags.append(x)

        output = ' '.join(ptags)

        #pass sanitized output to analysis engine
        analysis = Readability(output)
        flesch   = analysis.flesch()
        response = {url: flesch.score} 
        export.append(response)
        values.append(flesch.score)
    
    # reduce values to one sum, count the docs, find overall average, and append to results
    values_sum = reduce(lambda a, b: a + b, values)
    docs_sum = len(export)
    flesch_average = values_sum / docs_sum
    export.append({'flesch_average': flesch_average})
    export.append({'docs_sum': docs_sum})
    
    return export
