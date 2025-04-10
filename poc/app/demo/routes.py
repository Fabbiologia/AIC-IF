from flask import render_template, request, jsonify, redirect, url_for
from app.demo import bp
from app.models.citation_registry import CitationRegistry
from app.models.knowledge_graph import KnowledgeGraph
from app.models.model_interpreter import ModelInterpreter
import json
import numpy as np
import pandas as pd
from datetime import datetime

# Initialize components
citation_registry = CitationRegistry()
knowledge_graph = KnowledgeGraph()
model_interpreter = ModelInterpreter()

@bp.route('/citation-tracker')
def citation_tracker():
    """Redirect to real-time citations demo"""
    return redirect(url_for('demo.real_time_citations'))

@bp.route('/model-interpretation')
def model_interpretation():
    """Redirect to real-time citations demo"""
    return redirect(url_for('demo.real_time_citations'))

@bp.route('/feature-contributions', methods=['POST'])
def feature_contributions():
    """Analyze and visualize feature contributions using SHAP or LIME"""
    data = request.get_json()
    
    dataset_id = data.get('dataset_id', 'climate_data')
    model_id = data.get('model_id', 'regression_model')
    method = data.get('method', 'shap')
    
    # Generate feature contributions using the specified method
    contributions = model_interpreter.analyze_contributions(
        dataset_id=dataset_id,
        model_id=model_id,
        method=method
    )
    
    # Log each feature contribution as a citation
    for contrib in contributions:
        citation_data = {
            "doi": contrib["doi"],
            "source_title": contrib["feature"],
            "source_type": "dataset",
            "ai_model": model_id,
            "contribution_score": float(contrib["value"]),
            "user_id": data.get("user_id", "demo_user"),
            "context": f"Feature contribution via {method.upper()} analysis",
            "timestamp": datetime.utcnow().isoformat()
        }
        citation_registry.add_citation(citation_data)
        knowledge_graph.add_citation(citation_data)
    
    return jsonify({
        'status': 'success',
        'contributions': contributions,
        'visualization_url': url_for('demo.contribution_visualization', 
                                   dataset_id=dataset_id, 
                                   model_id=model_id,
                                   method=method)
    })

@bp.route('/visualization/<dataset_id>/<model_id>/<method>')
def contribution_visualization(dataset_id, model_id, method):
    """Redirect to real-time citations demo"""
    return redirect(url_for('demo.real_time_citations'))

@bp.route('/real-time-citations')
def real_time_citations():
    """Real-time citation event simulation"""
    return render_template('demo/real_time_citations.html',
                         title='Real-Time Citations Demo')

@bp.route('/simulate-citations', methods=['POST'])
def simulate_citations():
    """Simulate a batch of citation events for demonstration"""
    data = request.get_json()
    
    # Number of citations to simulate
    count = data.get('count', 10)
    ai_model = data.get('ai_model', 'GPT-4')
    
    # Sample publications for demo
    publications = [
        {"doi": "10.1038/s41586-023-06792-0", "title": "Climate change impact on marine ecosystems", "authors": "Smith et al."},
        {"doi": "10.1126/science.abd4896", "title": "Ocean acidification and coral reefs", "authors": "Johnson & Williams"},
        {"doi": "10.1073/pnas.2023152118", "title": "Biodiversity loss in tropical forests", "authors": "Lee et al."},
        {"doi": "10.1016/j.ocecoaman.2022.12.007", "title": "Coastal management strategies", "authors": "Wong & Chen"},
        {"doi": "10.1029/2021GL094771", "title": "Sea level rise prediction models", "authors": "Garcia et al."}
    ]
    
    # Sample contexts
    contexts = [
        "Climate change research",
        "Marine ecology query",
        "Biodiversity assessment",
        "Conservation planning",
        "Environmental policy development"
    ]
    
    # Generate random citations
    citations = []
    for i in range(count):
        pub = publications[i % len(publications)]
        citation_data = {
            "doi": pub["doi"],
            "source_title": pub["title"],
            "source_type": "journal_article",
            "authors": pub["authors"],
            "ai_model": ai_model,
            "contribution_score": round(np.random.uniform(0.3, 0.95), 2),
            "user_id": f"demo_user_{i % 5 + 1}",
            "context": contexts[i % len(contexts)],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Log the citation
        citation_id = citation_registry.add_citation(citation_data)
        knowledge_graph.add_citation(citation_data)
        
        citations.append({
            "citation_id": citation_id,
            **citation_data
        })
    
    return jsonify({
        "status": "success",
        "count": len(citations),
        "citations": citations
    })
