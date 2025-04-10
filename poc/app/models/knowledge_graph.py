import networkx as nx
import json
import uuid
from datetime import datetime

class KnowledgeGraph:
    """
    Knowledge Graph component of the AIC-IF framework.
    
    Responsible for:
    - Building a graph representation of the citation network
    - Connecting papers, authors, datasets, and AI models
    - Providing visualization data
    
    This simulates a Neo4j graph database with NetworkX for the PoC.
    In production, this would use a proper graph database like Neo4j.
    """
    
    def __init__(self):
        """Initialize the knowledge graph"""
        # Create a directed graph
        self.graph = nx.DiGraph()
        
        # Load sample data
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data to populate the knowledge graph"""
        # Sample papers
        papers = [
            {
                "id": "10.1038/s41586-023-06792-0",
                "title": "Climate change impact on marine ecosystems",
                "type": "paper",
                "authors": ["Smith, J.", "Anderson, T.", "Wilson, M."]
            },
            {
                "id": "10.1126/science.abd4896",
                "title": "Ocean acidification and coral reefs",
                "type": "paper",
                "authors": ["Johnson, K.", "Williams, P."]
            },
            {
                "id": "10.1073/pnas.2023152118",
                "title": "Biodiversity loss in tropical forests",
                "type": "paper",
                "authors": ["Lee, S.", "Brown, R.", "Martinez, D."]
            }
        ]
        
        # Sample datasets
        datasets = [
            {
                "id": "10.5061/dryad.1234",
                "title": "Global sea temperature data 2000-2022",
                "type": "dataset",
                "creators": ["NOAA", "Smith, J."]
            },
            {
                "id": "10.5061/dryad.5678",
                "title": "Coral reef health indicators",
                "type": "dataset",
                "creators": ["Johnson, K.", "Marine Biology Institute"]
            }
        ]
        
        # Add papers to the graph
        for paper in papers:
            self.graph.add_node(paper["id"], 
                               title=paper["title"], 
                               type="paper",
                               size=10,
                               color="#3498db")
            
            # Add authors and connect to papers
            for author in paper["authors"]:
                if not self.graph.has_node(author):
                    self.graph.add_node(author, 
                                       type="author",
                                       size=7,
                                       color="#e74c3c")
                
                # Connect author to paper
                self.graph.add_edge(author, paper["id"], 
                                   relationship="AUTHORED",
                                   weight=1)
        
        # Add datasets
        for dataset in datasets:
            self.graph.add_node(dataset["id"], 
                               title=dataset["title"], 
                               type="dataset",
                               size=8,
                               color="#2ecc71")
            
            # Connect creators to datasets
            for creator in dataset["creators"]:
                if not self.graph.has_node(creator):
                    self.graph.add_node(creator, 
                                       type="author",
                                       size=7,
                                       color="#e74c3c")
                
                self.graph.add_edge(creator, dataset["id"], 
                                   relationship="CREATED",
                                   weight=1)
        
        # Add some relationships between papers and datasets
        self.graph.add_edge("10.1038/s41586-023-06792-0", "10.5061/dryad.1234", 
                           relationship="USES",
                           weight=2)
        
        self.graph.add_edge("10.1126/science.abd4896", "10.5061/dryad.5678", 
                           relationship="USES",
                           weight=2)
        
        # Add AI citation relationships
        self.graph.add_node("GPT-4", 
                           type="ai_model",
                           size=12,
                           color="#9b59b6")
        
        self.graph.add_edge("GPT-4", "10.1038/s41586-023-06792-0", 
                           relationship="CITES",
                           weight=3,
                           timestamp="2025-04-01T10:15:30")
        
        self.graph.add_edge("GPT-4", "10.1126/science.abd4896", 
                           relationship="CITES",
                           weight=2,
                           timestamp="2025-04-02T15:22:45")
    
    def add_citation(self, citation_data):
        """
        Add a citation to the knowledge graph
        
        Args:
            citation_data (dict): Citation metadata
                Required keys: doi, ai_model
                Optional keys: source_title, authors, timestamp
        """
        doi = citation_data.get("doi")
        ai_model = citation_data.get("ai_model")
        source_title = citation_data.get("source_title", "Unknown")
        source_type = citation_data.get("source_type", "paper")
        authors = citation_data.get("authors", "").split("&") if "authors" in citation_data else []
        timestamp = citation_data.get("timestamp", datetime.utcnow().isoformat())
        
        # Add source node if it doesn't exist
        if not self.graph.has_node(doi):
            node_color = "#3498db"  # Default blue for papers
            if source_type == "dataset":
                node_color = "#2ecc71"  # Green for datasets
            elif source_type == "code":
                node_color = "#f39c12"  # Yellow for code
                
            self.graph.add_node(doi, 
                               title=source_title, 
                               type=source_type,
                               size=10,
                               color=node_color)
        
        # Add AI model node if it doesn't exist
        if not self.graph.has_node(ai_model):
            self.graph.add_node(ai_model, 
                               type="ai_model",
                               size=12,
                               color="#9b59b6")
        
        # Add citation relationship
        self.graph.add_edge(ai_model, doi, 
                           relationship="CITES",
                           weight=2,
                           timestamp=timestamp)
        
        # Add authors if provided
        for author in authors:
            author = author.strip()
            if author:
                if not self.graph.has_node(author):
                    self.graph.add_node(author, 
                                       type="author",
                                       size=7,
                                       color="#e74c3c")
                
                # Connect author to source
                if not self.graph.has_edge(author, doi):
                    self.graph.add_edge(author, doi, 
                                       relationship="AUTHORED",
                                       weight=1)
    
    def get_visualization_data(self):
        """
        Get graph data for visualization
        
        Returns:
            dict: Graph data in a format suitable for visualization libraries
        """
        # Convert NetworkX graph to visualization format
        nodes = []
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            nodes.append({
                "id": node_id,
                "label": node_data.get("title", node_id),
                "type": node_data.get("type", "unknown"),
                "size": node_data.get("size", 5),
                "color": node_data.get("color", "#666666")
            })
        
        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "label": data.get("relationship", ""),
                "weight": data.get("weight", 1)
            })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def get_entity_connections(self, entity_id):
        """
        Get all connections for a specific entity
        
        Args:
            entity_id (str): Node ID in the graph
            
        Returns:
            dict: Direct connections to the entity
        """
        if not self.graph.has_node(entity_id):
            return {"error": "Entity not found"}
        
        # Get incoming connections
        incoming = []
        for source, _ in self.graph.in_edges(entity_id):
            edge_data = self.graph.get_edge_data(source, entity_id)
            node_data = self.graph.nodes[source]
            incoming.append({
                "id": source,
                "label": node_data.get("title", source),
                "type": node_data.get("type", "unknown"),
                "relationship": edge_data.get("relationship", ""),
                "timestamp": edge_data.get("timestamp", "")
            })
        
        # Get outgoing connections
        outgoing = []
        for _, target in self.graph.out_edges(entity_id):
            edge_data = self.graph.get_edge_data(entity_id, target)
            node_data = self.graph.nodes[target]
            outgoing.append({
                "id": target,
                "label": node_data.get("title", target),
                "type": node_data.get("type", "unknown"),
                "relationship": edge_data.get("relationship", ""),
                "timestamp": edge_data.get("timestamp", "")
            })
        
        return {
            "entity": {
                "id": entity_id,
                "data": self.graph.nodes[entity_id]
            },
            "incoming": incoming,
            "outgoing": outgoing
        }
    
    def get_citation_path(self, source_id, target_id, max_depth=3):
        """
        Find citation paths between two entities
        
        Args:
            source_id (str): Source entity ID
            target_id (str): Target entity ID
            max_depth (int): Maximum path length
            
        Returns:
            list: List of paths from source to target
        """
        if not (self.graph.has_node(source_id) and self.graph.has_node(target_id)):
            return []
        
        try:
            # Find all simple paths with limited length
            paths = list(nx.all_simple_paths(self.graph, source_id, target_id, cutoff=max_depth))
            
            # Format paths
            formatted_paths = []
            for path in paths:
                path_info = []
                for i in range(len(path) - 1):
                    source = path[i]
                    target = path[i + 1]
                    edge_data = self.graph.get_edge_data(source, target)
                    path_info.append({
                        "source": source,
                        "source_type": self.graph.nodes[source].get("type", "unknown"),
                        "target": target,
                        "target_type": self.graph.nodes[target].get("type", "unknown"),
                        "relationship": edge_data.get("relationship", ""),
                        "timestamp": edge_data.get("timestamp", "")
                    })
                formatted_paths.append(path_info)
            
            return formatted_paths
        except:
            return []
