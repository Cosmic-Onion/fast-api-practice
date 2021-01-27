import requests 
import lxml.html
from typing import Optional
from fastapi import FastAPI
import re

app = FastAPI()

def clean(string):
     return re.sub("\n          ", "", string)
     
@app.get("/{target_language}/{word}")
def return_simple_translation(target_language: str, word: str):
    return(perform_translation(target_language, word))

@app.get("/{source_language}/{target_language}/{word}")
def return_translation(source_language: str, target_language: str, word: str):
    return(perform_translation(target_language, word, source_language))

def perform_translation(target_language: str, word: str, source_language: Optional[str] = "english"):

    got = requests.get('https://context.reverso.net/translation/'+ source_language + '-' + target_language + '/' + word, 
            headers={'Host': 'context.reverso.net',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://context.reverso.net/translation/english-french/hello',
            'DNT': '1',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'}
            )

    soup = lxml.html.fromstring(got.text)

    source_examples = soup.xpath("//div[@class='src ltr']/span[@class='text']")

    target_examples = soup.xpath("//div[@class='trg ltr']/span[@class='text']")

    target_highlights = soup.xpath("//div[@class='trg ltr']/span[@class='text']//em")

    outputJSON = []

    for target_example, target_highlight, source_example in zip(target_examples, target_highlights, source_examples):

        s_example = clean(source_example.text_content())
        t_example = clean(target_example.text_content())

        translationJSON = { 
                     target_highlight.text_content(): {
                                     "source example" : s_example,
                                     "translation example" : t_example
                                     }
                      }
        outputJSON.append(translationJSON)

    return(outputJSON)

