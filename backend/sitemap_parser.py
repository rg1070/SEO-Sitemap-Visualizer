# backend/sitemap_parser.py
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import networkx as nx
from pyvis.network import Network

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

def generate_graph(sitemap_url, output_file="sitemap_network.html"):
    tree = {sitemap_url: parse_sitemap(sitemap_url)}
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
    return output_file
