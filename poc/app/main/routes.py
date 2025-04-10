from flask import render_template, current_app, request, jsonify, redirect, url_for
from app.main import bp
from app.models.citation_registry import CitationRegistry
from app.models.knowledge_graph import KnowledgeGraph

# Initialize our core components
citation_registry = CitationRegistry()
knowledge_graph = KnowledgeGraph()

@bp.route('/')
def index():
    """Main landing page for the AIC-IF framework demonstration"""
    return render_template('index.html', title='AI-Driven Citation Impact Factor')

# Redirect all removed pages to the home page
@bp.route('/about')
def about():
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    return redirect(url_for('main.index'))

@bp.route('/graph')
def graph():
    return redirect(url_for('main.index'))

@bp.route('/explanation')
def explanation():
    return redirect(url_for('main.index'))
