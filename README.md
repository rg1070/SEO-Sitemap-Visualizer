# Sitemap Visualizer

This project is a web-based tool that allows you to **enter a website domain** (e.g., `www.example.com`) and generate a **visual representation of its sitemap**. It crawls sitemap XML files recursively and builds an interactive network graph of all linked pages using Python, Flask, and PyVis.

## Features

- Input any domain and crawl its `sitemap.xml`
- Recursively parses nested sitemap indexes
- Visualizes the structure as an interactive graph
- Clean UI built with Flask and HTML/CSS
- Deployed on [Render](https://render.com)

## Demo

Visit the live app here:  
**[https://seo-sitemap-visualizer.onrender.com/](https://seo-sitemap-visualizer.onrender.com/)**

> Example: Try `www.northlightai.com`

## Tech Stack

- Python 3.10
- Flask
- BeautifulSoup4
- PyVis & NetworkX
- Docker (for deployment)
- Hosted on Render

## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/rg1070/SEO-Sitemap-Visualizer.git
cd sitemap-visualizer
```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python backend/app.py
```

Then open `http://localhost:5000` in your browser.

## Docker Instructions

### Build the Image

```bash
docker build -t sitemap-visualizer .
```

### Run the Container

```bash
docker run -p 5000:5000 sitemap-visualizer
```

## Deploying on Render

This project uses Render’s **Docker-based web service** with a `render.yaml` file.  
To deploy:

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create a new **Web Service**
4. Select the repo and deploy

## Acknowledgment

This project was created for educational and practical deployment experience, showcasing the use of web scraping, graph visualization, and Dockerized Flask apps in production.

