from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def analyze_seo(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = {}

        # Title Analysis
        title = soup.find('title')
        results['title'] = title.text if title else "Missing!"
        results['title_length'] = len(results['title'])

        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        results['meta_description'] = meta_desc['content'] if meta_desc else "Missing!"
        results['meta_desc_length'] = len(results['meta_description'])

        # Headers
        results['h1'] = [h.text.strip() for h in soup.find_all('h1')]
        results['h2'] = [h.text.strip() for h in soup.find_all('h2')]

        # Images (Alt Text)
        images = soup.find_all('img')
        results['images_without_alt'] = [img['src'] for img in images if not img.get('alt')]

        # Keyword Analysis (Basic)
        content = soup.get_text().lower()
        results['keyword_count'] = {
            'seo': content.count('seo'),
            'digital marketing': content.count('digital marketing'),
            'web': content.count('web')
        }

        return results

    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        results = analyze_seo(url)
        return render_template('index.html', results=results, url=url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
