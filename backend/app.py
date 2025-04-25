from flask import Flask, render_template, request
from backend.sitemap_parser import generate_graph
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        raw_url = request.form['url_input'].strip()
        if not raw_url.startswith("http"):
            raw_url = "https://" + raw_url
        if not raw_url.endswith("/sitemap.xml"):
            raw_url = raw_url.rstrip("/") + "/sitemap.xml"

        parsed_url = urlparse(raw_url)
        if parsed_url.scheme and parsed_url.netloc:
            output_file = generate_graph(raw_url)
            return render_template("result.html", graph_file=output_file)

    return render_template("index.html")

@app.route('/graph')
def graph():
    return open("sitemap_network.html", "r").read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
