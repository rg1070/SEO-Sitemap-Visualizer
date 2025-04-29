# backend/sitemap_parser.py
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import networkx as nx
from pyvis.network import Network
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_sitemap(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml-xml')
        return [loc.text for loc in soup.find_all('loc')]
    except Exception as e:
        print(f"Error: {e}")
        return []

def parse_sitemap(url):
    locs = fetch_sitemap(url)
    if not locs:
        return {}

    tree = {}
    urls = []

    for loc in locs:
        if loc.endswith('.xml'):
            tree[loc] = parse_sitemap(loc)
        else:
            urls.append(loc)

    if tree and urls:
        tree["_final_urls"] = urls
        return tree
    elif urls:
        return urls
    else:
        return tree

def tree_to_edges(tree, parent=None):
    edges = []
    if isinstance(tree, list):
        for item in tree:
            edges.append((parent, item))
    elif isinstance(tree, dict):
        for key, value in tree.items():
            if parent:
                edges.append((parent, key))
            edges += tree_to_edges(value, parent=key)
    return edges

def generate_graph(sitemap_url, output_file="sitemap_network.html", json_filename=None):
    tree = {sitemap_url: parse_sitemap(sitemap_url)}

    # Default name if not provided
    if json_filename is None:
        json_filename = "sitemap_tree.json"

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

    edges = tree_to_edges(tree[sitemap_url], parent=sitemap_url)

    G = nx.DiGraph()
    G.add_edges_from(edges)
    net = Network(height="750px", width="100%", directed=True, notebook=False)

    for node in G.nodes():
        if node == sitemap_url:
            net.add_node(node, label=str(urlparse(sitemap_url).netloc), title=node, shape='dot', size=30,
                         color={"background": "white", "border": "blue"}, borderWidth=4,
                         font={"color": "black", "size": 35, "bold": True})
        elif node.endswith('.xml'):
            net.add_node(node, label="Sitemap", title=node, shape='dot', size=25)
        else:
            net.add_node(node, label=" ", title=node, shape='dot', size=15,
                         color={"background": "#ccffcc", "border": "#009933"})

    for source, target in G.edges():
        net.add_edge(source, target)

    net.force_atlas_2based()
    net.set_options("""
    { "physics": { "stabilization": false }, "interaction": { "dragNodes": true } }
    """)
    net.write_html(output_file)

    # Read the generated HTML
    with open(output_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Inject JS
    inject_js = f"""
    <script type="text/javascript">
    window.addEventListener("load", function () {{
        // ✅ Hide the Pyvis loading bar if it exists
        const loader = document.getElementById("loadingBar");
        if (loader) loader.style.display = "none";

        const rootNodeId = "{sitemap_url}";
        const titleNodeId = "graph_title";
        const originalLabels = {{}};

        network.on("click", function (params) {{
        if (params.nodes.length > 0) {{
            let clickedNodeId = params.nodes[0];

            nodes.get().forEach(function (node) {{
            if (!(node.id in originalLabels)) {{
                originalLabels[node.id] = node.label;
            }}

            if (node.id === rootNodeId || node.id === titleNodeId) {{
                return;
            }}

            if (node.id === clickedNodeId) {{
                nodes.update({{id: node.id, label: node.title}});
            }} else {{
                nodes.update({{id: node.id, label: ""}});
            }}
            }});
        }} else {{
            nodes.get().forEach(function (node) {{
            if (node.id !== rootNodeId && node.id !== titleNodeId && originalLabels[node.id] === "") {{
                nodes.update({{id: node.id, label: ""}});
            }}
            }});
        }}
        }});
    }});
    </script>
    """

    # Inject before </body>
    html = html.replace("</body>", inject_js + "\\n</body>")

    # Save it back
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    return output_file
