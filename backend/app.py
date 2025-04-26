from flask import Flask, render_template, request, Response
from backend.sitemap_parser import generate_graph
from urllib.parse import urlparse

# ✅ Tell Flask where to find templates and static files
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    graph_file = None
    json_available = False
    domain_name = None  # ✅ Always define upfront

    if request.method == 'POST':
        raw_url = request.form['url_input'].strip()
        if not raw_url.startswith("http"):
            raw_url = "https://" + raw_url
        if not raw_url.endswith("/sitemap.xml"):
            raw_url = raw_url.rstrip("/") + "/sitemap.xml"

        parsed_url = urlparse(raw_url)
        if parsed_url.scheme and parsed_url.netloc:
            generate_graph(raw_url)
            graph_file = "sitemap_network.html"
            json_available = True
            domain_name = parsed_url.netloc.replace(".", "_")  # ✅ Only if defined

    return render_template("index.html", graph_file=graph_file, json_available=json_available, domain_name=domain_name)


@app.route('/graph')
def graph():
    with open("sitemap_network.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(html_content, mimetype='text/html')

@app.route('/download-json')
def download_json():
    from flask import request, send_file
    filename = request.args.get("filename", "sitemap_tree")
    return send_file("sitemap_tree.json", as_attachment=True, download_name=f"{filename}.json")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
