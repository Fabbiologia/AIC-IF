from flask import jsonify, request, current_app
from app.api import bp
from app.models.citation_registry import CitationRegistry
from app.models.knowledge_graph import KnowledgeGraph
import json
from datetime import datetime

# Initialize our components
citation_registry = CitationRegistry()
knowledge_graph = KnowledgeGraph()

@bp.route('/citations', methods=['POST'])
def log_citation():
    """
    API endpoint to log citation events when an AI system uses academic content
    
    Request body example:
    {
        "doi": "10.1038/s41586-023-05782-3",
        "source_title": "Nature Article on Climate Change",
        "source_type": "journal_article",
        "ai_model": "GPT-4",
        "user_id": "user_123",
        "context": "Answer to climate science query",
        "contribution_score": 0.85
    }
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['doi', 'ai_model']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Add timestamp if not provided
    if 'timestamp' not in data:
        data['timestamp'] = datetime.utcnow().isoformat()
        
    # Log the citation in our registry
    citation_id = citation_registry.add_citation(data)
    
    # Update the knowledge graph
    knowledge_graph.add_citation(data)
    
    return jsonify({
        'status': 'success',
        'citation_id': citation_id,
        'message': 'Citation logged successfully'
    })

@bp.route('/citations', methods=['GET'])
def get_citations():
    """Get citation logs based on filters"""
    # Parse query parameters
    doi = request.args.get('doi')
    ai_model = request.args.get('ai_model')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 50, type=int)
    
    # Get citations from the registry
    citations = citation_registry.get_citations(
        doi=doi,
        ai_model=ai_model,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    
    return jsonify({
        'status': 'success',
        'count': len(citations),
        'citations': citations
    })

@bp.route('/stats/top-cited', methods=['GET'])
def top_cited():
    """Get top cited works"""
    ai_model = request.args.get('model')
    limit = request.args.get('limit', 10, type=int)
    
    top_cited = citation_registry.get_top_cited(
        ai_model=ai_model,
        limit=limit
    )
    
    return jsonify({
        'status': 'success',
        'top_cited': top_cited
    })

@bp.route('/contributions/analyze', methods=['POST'])
def analyze_contributions():
    """
    Analyze feature contributions using SHAP and LIME
    
    Request body example:
    {
        "model_id": "climate_model_1",
        "input_data": [...],
        "method": "shap"  # or "lime"
    }
    """
    data = request.get_json()
    
    # This would be a more complex integration with model interpretability tools
    # For the PoC, we'll simulate this with sample data
    
    if data.get('method', 'shap').lower() == 'shap':
        # Simulated SHAP values
        contributions = [
            {"feature": "Temperature Data (Smith et al., 2023)", "doi": "10.1038/s12345", "value": 0.45},
            {"feature": "CO2 Measurements (Johnson, 2022)", "doi": "10.1126/s98765", "value": 0.28},
            {"feature": "Ocean Current Dataset (NOAA, 2023)", "doi": "10.1016/j12345", "value": 0.15},
            {"feature": "Rainfall Patterns (Lee & Wong, 2021)", "doi": "10.1038/s55555", "value": 0.12}
        ]
    else:
        # Simulated LIME explanations
        contributions = [
            {"feature": "Temperature Data (Smith et al., 2023)", "doi": "10.1038/s12345", "value": 0.42},
            {"feature": "CO2 Measurements (Johnson, 2022)", "doi": "10.1126/s98765", "value": 0.31},
            {"feature": "Ocean Current Dataset (NOAA, 2023)", "doi": "10.1016/j12345", "value": 0.17},
            {"feature": "Rainfall Patterns (Lee & Wong, 2021)", "doi": "10.1038/s55555", "value": 0.10}
        ]
        
    # Log the contributions as citations
    for contrib in contributions:
        citation_data = {
            "doi": contrib["doi"],
            "source_title": contrib["feature"],
            "ai_model": data.get("model_id", "unknown_model"),
            "contribution_score": contrib["value"],
            "user_id": data.get("user_id", "system"),
            "context": f"Feature contribution via {data.get('method', 'shap').upper()} analysis",
            "timestamp": datetime.utcnow().isoformat()
        }
        citation_registry.add_citation(citation_data)
        knowledge_graph.add_citation(citation_data)
    
    return jsonify({
        'status': 'success',
        'contributions': contributions,
        'explanation_method': data.get('method', 'shap').upper()
    })
