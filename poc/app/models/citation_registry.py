import json
import os
import uuid
from datetime import datetime
import pandas as pd
from collections import defaultdict, Counter

class CitationRegistry:
    """
    Citation Registry component of the AIC-IF framework.
    
    Responsible for:
    - Logging citation events when AI systems use scientific content
    - Tracking attribution and contribution metrics
    - Providing impact analytics
    
    This simulates a database with in-memory storage for the PoC.
    In production, this would use a proper database like PostgreSQL.
    """
    
    def __init__(self):
        """Initialize the citation registry"""
        # In-memory storage for the PoC
        self.citations = []
        self.citation_counts = defaultdict(int)
        self.author_citations = defaultdict(int)
        self.citation_by_doi = defaultdict(list)
        
        # Load sample data if available
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample citation data for demonstration"""
        sample_citations = [
            {
                "citation_id": str(uuid.uuid4()),
                "doi": "10.1038/s41586-023-06792-0",
                "source_title": "Climate change impact on marine ecosystems",
                "source_type": "journal_article",
                "authors": "Smith et al.",
                "ai_model": "GPT-4",
                "contribution_score": 0.89,
                "user_id": "user_123",
                "context": "Climate change research",
                "timestamp": "2025-04-01T10:15:30"
            },
            {
                "citation_id": str(uuid.uuid4()),
                "doi": "10.1126/science.abd4896",
                "source_title": "Ocean acidification and coral reefs",
                "source_type": "journal_article",
                "authors": "Johnson & Williams",
                "ai_model": "GPT-4",
                "contribution_score": 0.76,
                "user_id": "user_456",
                "context": "Marine ecology query",
                "timestamp": "2025-04-02T15:22:45"
            },
            {
                "citation_id": str(uuid.uuid4()),
                "doi": "10.1073/pnas.2023152118",
                "source_title": "Biodiversity loss in tropical forests",
                "source_type": "dataset",
                "authors": "Lee et al.",
                "ai_model": "Claude-3",
                "contribution_score": 0.92,
                "user_id": "user_789",
                "context": "Biodiversity assessment",
                "timestamp": "2025-04-03T09:11:05"
            }
        ]
        
        # Add sample citations to our registry
        for citation in sample_citations:
            self.add_citation(citation)
    
    def add_citation(self, citation_data):
        """
        Log a new citation event
        
        Args:
            citation_data (dict): Citation metadata
                Required keys: doi, ai_model
                Optional keys: source_title, source_type, authors, user_id, 
                               context, contribution_score, timestamp
                
        Returns:
            str: The generated citation ID
        """
        # Generate a citation ID if not provided
        citation_id = citation_data.get('citation_id', str(uuid.uuid4()))
        citation_data['citation_id'] = citation_id
        
        # Ensure timestamp exists
        if 'timestamp' not in citation_data:
            citation_data['timestamp'] = datetime.utcnow().isoformat()
        
        # Add to our in-memory storage
        self.citations.append(citation_data)
        
        # Update citation counts
        doi = citation_data['doi']
        self.citation_counts[doi] += 1
        self.citation_by_doi[doi].append(citation_data)
        
        # Update author citation counts if authors are provided
        if 'authors' in citation_data:
            self.author_citations[citation_data['authors']] += 1
        
        return citation_id
    
    def get_citations(self, doi=None, ai_model=None, start_date=None, end_date=None, limit=50):
        """
        Retrieve citation logs based on filters
        
        Args:
            doi (str, optional): Filter by DOI
            ai_model (str, optional): Filter by AI model
            start_date (str, optional): Filter by start date (ISO format)
            end_date (str, optional): Filter by end date (ISO format)
            limit (int, optional): Maximum number of results
            
        Returns:
            list: Filtered citation logs
        """
        # Start with all citations
        filtered = self.citations
        
        # Apply filters
        if doi:
            filtered = [c for c in filtered if c['doi'] == doi]
        
        if ai_model:
            filtered = [c for c in filtered if c['ai_model'] == ai_model]
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            filtered = [c for c in filtered if datetime.fromisoformat(
                c['timestamp'].replace('Z', '+00:00')) >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            filtered = [c for c in filtered if datetime.fromisoformat(
                c['timestamp'].replace('Z', '+00:00')) <= end_dt]
        
        # Sort by timestamp (newest first)
        filtered.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Apply limit
        return filtered[:limit]
    
    def get_top_cited(self, ai_model=None, limit=10):
        """
        Get the top cited works
        
        Args:
            ai_model (str, optional): Filter by AI model
            limit (int, optional): Maximum number of results
            
        Returns:
            list: Top cited works with citation counts
        """
        if ai_model:
            # Filter citations by AI model
            filtered_citations = [c for c in self.citations if c['ai_model'] == ai_model]
            # Count DOIs
            counter = Counter([c['doi'] for c in filtered_citations])
        else:
            # Convert defaultdict to Counter
            counter = Counter()
            for doi, count in self.citation_counts.items():
                counter[doi] = count
        
        # Get top cited
        top_cited_dois = [doi for doi, _ in counter.most_common(limit)] if counter else []
        
        # Format results
        top_cited = []
        for doi in top_cited_dois:
            # Get details from the first citation with this DOI
            citation = next((c for c in self.citations if c['doi'] == doi), None)
            if citation:
                top_cited.append({
                    'doi': doi,
                    'title': citation.get('source_title', 'Unknown'),
                    'authors': citation.get('authors', 'Unknown'),
                    'type': citation.get('source_type', 'journal_article'),
                    'citation_count': counter[doi],
                    'aicif_score': self._calculate_aicif_score(doi)
                })
        
        return top_cited
    
    def get_recent_citations(self, limit=5):
        """Get most recent citation events"""
        # Sort by timestamp (newest first)
        sorted_citations = sorted(self.citations, key=lambda x: x['timestamp'], reverse=True)
        return sorted_citations[:limit]
    
    def get_summary_stats(self):
        """Get summary statistics for the dashboard"""
        return {
            'total_citations': len(self.citations),
            'unique_sources': len(self.citation_counts),
            'ai_models': list(set(c['ai_model'] for c in self.citations)),
            'source_types': Counter(c.get('source_type', 'unknown') for c in self.citations),
            'total_authors': len(self.author_citations)
        }
    
    def _calculate_aicif_score(self, doi):
        """
        Calculate the AI-Driven Citation Impact Factor score for a publication
        
        In a real implementation, this would be a more sophisticated algorithm
        that takes into account citation frequency, recency, contribution scores,
        and AI model reputation/usage.
        
        Args:
            doi (str): The DOI of the publication
            
        Returns:
            float: The AIC-IF score
        """
        citations = self.citation_by_doi.get(doi, [])
        
        if not citations:
            return 0.0
        
        # Basic calculation based on citation count and contribution scores
        citation_count = len(citations)
        avg_contribution = sum(c.get('contribution_score', 0.5) for c in citations) / citation_count
        
        # Calculate recency factor (more recent citations have higher weight)
        now = datetime.utcnow()
        recency_weights = []
        
        for citation in citations:
            try:
                citation_time = datetime.fromisoformat(citation['timestamp'].replace('Z', '+00:00'))
                # Calculate days since citation (with a minimum of 1 day)
                days_since = max(1, (now - citation_time).days)
                # More recent citations get higher weights
                recency_weights.append(1 / days_since)
            except (ValueError, KeyError):
                recency_weights.append(0.5)  # Default weight for invalid timestamps
        
        avg_recency = sum(recency_weights) / len(recency_weights) if recency_weights else 0.5
        
        # AI model diversity factor
        ai_models = set(c['ai_model'] for c in citations)
        model_diversity = min(1.0, len(ai_models) / 5)  # Normalize to max of 1.0
        
        # Calculate final AIC-IF score
        # This is a simplified formula for the PoC
        aicif_score = (citation_count * 0.4 + 
                      avg_contribution * 0.3 + 
                      avg_recency * 0.2 +
                      model_diversity * 0.1) * 10  # Scale to a 0-10 range
        
        return round(aicif_score, 2)
