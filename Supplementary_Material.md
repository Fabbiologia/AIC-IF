# Supplementary Material: The AI-Driven Citation Impact Factor Framework

## 1. Introduction and Motivation

The AI-Driven Citation Impact Factor (AIC-IF) framework represents a novel approach to tracking, attributing, and crediting scientific contributions in an ecosystem increasingly mediated by artificial intelligence systems. Traditional citation metrics fail to capture how AI systems utilize scientific knowledge, creating significant gaps in attribution and credit distribution.

### Key Challenges Addressed
- **Attribution Gap**: Scientific contributions used by AI systems often remain uncredited
- **Equity Concerns**: Benefits of AI advancement may not flow back to original knowledge creators
- **Incentive Misalignment**: Scientific reward systems fail to recognize contributions to AI knowledge
- **Verification Challenges**: Claims made by AI systems lack clear provenance information

## 2. Framework Architecture

The AIC-IF framework consists of four interconnected layers that work together to enable comprehensive citation tracking, attribution, and visualization:

### 2.1 Monitoring Layer
- **Citation Logger**: Captures citation events when AI systems access scientific content
- **Event Processor**: Processes and standardizes citation events
- **Logging API**: Provides interfaces for AI systems to log citation events

#### 2.1.1 AI-Powered Citation Tracking
At the heart of AIC-IF is an AI system that continuously monitors when and how scholarly contributions are cited or utilized by other AI models and digital platforms. This goes beyond traditional paper citations – it tracks instances of knowledge usage. For example, if an AI assistant generates a report and pulls in findings from Dr. A's dataset and Dr. B's algorithm, those events are logged as citation instances. The AI tracker operates across multiple channels (AI queries, automated literature reviews, etc.), effectively serving as a real-time observer of scientific knowledge flow.

#### 2.1.2 Metadata Embedding
To enable smart tracking, each research output (be it a paper, dataset, code, or even an AI-derived insight) is embedded with rich metadata. This metadata includes unique identifiers (like DOIs for papers or dataset IDs), author/contributor information (e.g., ORCID iDs), and content descriptors (keywords, fields, methods). By embedding such metadata directly into digital publications and even into data files, we ensure AI systems can recognize and parse the identity of a piece of knowledge. For instance, when an AI system ingests an article, it can read the embedded metadata to know the article's ID and authors, which is crucial for attribution.

#### 2.1.3 Centralized Citation Registry
All citation events and metadata are stored in a centralized registry – essentially a global database of who cited what, when, and in what context. This can be envisioned as an extension of existing infrastructures like Crossref or OpenCitations, but upgraded for AI-scale volume and speed. Every time an AI (or a traditional source) references a piece of work, a standardized entry is added to the registry. The registry isn't just a static list; it's continuously updated and is queryable via APIs. It acts as the ground truth for calculating the AIC-IF and for verifying citations.

### 2.2 Analysis Layer
- **SHAP Analysis**: Utilizes SHapley Additive exPlanations to quantify source contributions
- **LIME Analysis**: Employs Local Interpretable Model-agnostic Explanations for contribution analysis
- **Attention Analysis**: Analyzes attention mechanisms in transformer models to map source importance

### 2.3 Attribution Layer
- **Citation Registry**: Central repository for all citation events
- **Knowledge Graph**: Represents relationships between entities in the citation ecosystem
- **Credit Allocator**: Distributes credit based on contribution analysis

### 2.4 Visualization Layer
- **Graph Visualizer**: Renders the knowledge graph for exploration
- **Dashboard**: Provides interactive views of citation metrics
- **API Endpoints**: Enables programmatic access to visualization data

## 3. Core Components

### 3.1 Citation Registry

The Citation Registry serves as the central data repository for all citation events. Each citation event includes:

```json
{
  "citation_id": "cid-12345",
  "doi": "10.1038/s41586-023-06792-0",
  "title": "Climate change impact on marine ecosystems",
  "authors": ["Smith, J.", "Johnson, T."],
  "source_type": "journal_article",
  "publication_venue": "Nature",
  "publication_date": "2023-05-15",
  "ai_model": "model-12345",
  "context": "Answering query about climate impacts on ocean ecosystems",
  "timestamp": "2023-07-22T14:25:30Z",
  "contribution_score": 0.87
}
```

### 3.2 Knowledge Graph

The Knowledge Graph represents complex relationships between scientific entities:

- **Node Types**: Papers, Authors, Datasets, AI Models, Concepts
- **Edge Types**: Cites, Uses, Contributes_To, Builds_Upon

The graph structure enables:
- Tracking multi-step influence paths
- Identifying highly influential sources
- Analyzing network properties of the knowledge ecosystem
- Visualizing knowledge flow patterns

### 3.3 Contribution Analysis

The framework employs three complementary methods to quantify the contribution of different sources to AI outputs:

#### 3.3.1 SHAP (SHapley Additive exPlanations)
- Based on game theory's Shapley values
- Allocates credit for predictions fairly among features
- Provides both global and local interpretability

#### 3.3.2 LIME (Local Interpretable Model-agnostic Explanations)
- Creates locally faithful approximations of complex models
- Explains individual predictions through surrogate models
- Works with any black-box model

#### 3.3.3 Attention Mechanism Analysis
- Utilizes attention weights from transformer models
- Maps attention to source documents
- Quantifies relative importance of different sources

### 3.4 Attribution Mechanism

The attribution mechanism follows four key principles:

1. **Proportionality**: Credit is proportional to contribution
2. **Transitivity**: Credit flows through the knowledge graph
3. **Transparency**: Attribution decisions are explainable and auditable
4. **Temporality**: Real-time attribution as knowledge is used

### 3.5 Impact Factor Calculation

The AI-Driven Citation Impact Factor (AIC-IF) score provides a comprehensive metric for quantifying the impact of scientific works in AI-mediated knowledge ecosystems. Going beyond traditional citation metrics, the AIC-IF formula incorporates multiple dimensions of impact to create a more holistic measure of scientific contribution.

**AIC-IF Formula:**
```
AIC-IF = (citation_count × 0.4 + avg_contribution × 0.3 + avg_recency × 0.2 + model_diversity × 0.1) × 10
```

**Components in Detail:**

1. **Citation Count (40% weight)**: The raw frequency of citations by AI systems serves as the foundation of the impact score. This component acknowledges the fundamental importance of citation volume as a baseline indicator of a work's reach within the AI ecosystem. Unlike traditional citation counts that only track formal citations in published works, this metric captures instances where AI systems access and utilize scientific knowledge, providing a more comprehensive view of influence.

2. **Average Contribution (30% weight)**: This component measures the depth of impact by quantifying how substantively each source influenced AI outputs. Contribution scores are derived from advanced interpretability methods including SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) analyses, which assess the importance of each source to specific AI-generated outputs. By weighting contributions, the formula distinguishes between superficial references and sources that significantly shape AI reasoning and conclusions.

3. **Recency Factor (20% weight)**: Scientific relevance evolves over time, and this time-weighted measure ensures that temporal patterns of citation are properly valued. The recency factor gives higher weight to recent citations, calculated as the average of (1/days_since_citation) across all citations of the work. This approach rewards works that maintain ongoing relevance while still acknowledging historical contributions, creating a dynamic score that evolves with the changing landscape of scientific knowledge.

4. **Model Diversity (10% weight)**: This factor examines the breadth of impact across different AI systems. By measuring the variety of distinct AI models that cite a work (normalized to a 0-1 scale), the formula rewards publications with broad applicability across diverse AI applications and prevents score inflation from repeated citations by a single model. This component recognizes that works with cross-domain influence often represent more fundamental and versatile scientific contributions.

The combined weighted sum is multiplied by 10 to scale the final score to a more intuitive 0-10 range, where higher values indicate greater impact across multiple dimensions. This scaling facilitates easier interpretation and comparison of impact scores across different publications, fields, and time periods.

In implementation, the AIC-IF score is calculated dynamically as new citation events are registered in the Citation Registry. This provides a real-time measure of impact that continually evolves with the knowledge ecosystem, reflecting both the immediate influence of new publications and the sustained impact of seminal works.

The flexibility of the formula allows for domain-specific adaptations, where component weights can be adjusted to reflect the unique citation patterns and impact dimensions of different scientific fields. This customization ensures that the AIC-IF framework can provide meaningful impact measurements across the diverse landscape of scientific research.

#### 3.5.1 Additional Derived Metrics

The framework provides multiple layers of metrics:

- **Work-level AIC-IF**: Impact score per article, dataset, etc.
- **Researcher AIC-IF**: Aggregate impact score for an individual (summing or averaging over their contributions, possibly with adjustments for co-authorship).
- **Institution or Journal AIC-IF**: One could compute an institution's impact by aggregating its researchers' scores, or a journal's influence by aggregating works it published.
- **AI Influence Score**: Track which AI systems contribute most to knowledge dissemination (e.g., if an AI model is responsible for 30% of all citation events).

## 4. Implementation Approaches

### 4.1 Embedded Implementation

AI system developers can integrate the framework directly into their systems:
- Add citation hooks that trigger when sources are accessed
- Implement contribution analysis within the AI system
- Connect to the AIC-IF API for logging citation events

### 4.2 API-Based Implementation

External systems can interact with AI services through an API middleware:
- Process AI API responses
- Analyze outputs to identify likely sources
- Enrich AI responses with citation information

### 4.3 Retrospective Analysis

For existing AI systems without native support:
- Post-hoc analysis of system outputs
- Reverse engineering of knowledge sources
- Reconstruction of knowledge utilization patterns

## 5. Technical Specifications

### 5.1 Citation Registry Service

**Database Schema**:
```sql
CREATE TABLE citations (
    citation_id UUID PRIMARY KEY,
    doi VARCHAR(255),
    title VARCHAR(255),
    authors VARCHAR(255),
    source_type VARCHAR(50),
    publication_venue VARCHAR(255),
    publication_date DATE,
    ai_model VARCHAR(255),
    context TEXT,
    timestamp TIMESTAMP,
    contribution_score FLOAT
);
```

**API Endpoints**:
```
POST /api/citations
GET /api/citations/{citation_id}
GET /api/sources/{source_id}/citations
GET /api/models/{model_id}/citations
```

### 5.2 Knowledge Graph Engine

**Graph Database Schema** (Neo4j):
```cypher
// Node types
CREATE (:NodeType {name: 'Paper'});
CREATE (:NodeType {name: 'Author'});
CREATE (:NodeType {name: 'Dataset'});
CREATE (:NodeType {name: 'AIModel'});
CREATE (:NodeType {name: 'Concept'});

// Relationship types
CREATE (:RelationType {name: 'CITES'});
CREATE (:RelationType {name: 'USES'});
CREATE (:RelationType {name: 'CONTRIBUTES_TO'});
CREATE (:RelationType {name: 'BUILDS_UPON'});
```

**API Endpoints**:
```
GET /api/graph
GET /api/graph/node/{node_id}
GET /api/graph/path?source={source_id}&target={target_id}
```

### 5.3 Visualization Service

The framework provides interactive visualizations using D3.js for knowledge graph rendering and Chart.js for contribution analysis display.

**Visualization Components**:
- Force-directed graph visualization
- Contribution bar charts
- Heat maps for attention visualization
- Interactive dashboards for citation metrics

## 6. Use Cases

### 6.1 Enhanced Academic Metrics
- Real-time impact tracking beyond traditional citation counts
- Recognition of contributions to AI capabilities
- More equitable evaluation of interdisciplinary work

### 6.2 AI Transparency and Trust
- Clear provenance information for AI-generated content
- Verification of AI claims against cited sources
- Auditable trail of knowledge utilization

### 6.3 Scientific Credit Distribution
- Automatic attribution to all contributors
- Recognition of dataset creators and curators
- Credit for methodological innovations utilized by AI

### 6.4 Knowledge Ecosystem Mapping
- Identification of influential but under-recognized work
- Analysis of knowledge flow patterns
- Discovery of emergent research directions

## 7. Ethical Considerations

The implementation of the AIC-IF framework must address several ethical considerations:

### 7.1 Privacy and Consent
- Respecting author preferences for attribution
- Balancing transparency with privacy concerns
- Obtaining appropriate consent for tracking

### 7.2 Equity and Inclusion
- Ensuring the framework doesn't perpetuate existing biases
- Supporting diverse knowledge sources and traditions
- Providing accessibility to attribution information

### 7.3 Power Dynamics
- Preventing gaming or manipulation of the system
- Addressing potential concentration of credit
- Ensuring benefit to all knowledge creators, not just established entities

### 7.4 Anti-Gaming Mechanisms

With a metric that influences reputation, there's a risk of gaming – e.g., artificial inflation of citations. The AIC-IF framework includes algorithms to detect suspicious citation patterns. For instance, if an obscure paper suddenly is cited thousands of times by AI outputs in a short span, the system can flag this for review. By analyzing the network of citations in the knowledge graph, anomalies stand out (legitimate influential work usually has a diverse set of citers, whereas gaming might use repetitive or coordinated sources).

Specific anti-gaming mechanisms include:

- **Fabricated Citation Detection**: Each new citation is cross-verified against trusted databases (e.g., Crossref, Semantic Scholar, arXiv). If a DOI isn't found or metadata doesn't match, it's flagged as a fabricated citation.
- **Duplicate and Irrelevant Reference Filtering**: Within one AI output, repeated citations are merged so that each DOI is counted only once.
- **Anomaly Detection**: Using machine learning (e.g., outlier detection), the framework monitors citation patterns to identify unusually high frequencies or suspicious reciprocal citations.
- **Preventative Filters**: The API can enforce rules—rejecting citations from known predatory sources or capping the number of times a DOI can be logged per answer—to safeguard against manipulation.

## 8. Future Development Directions

### 8.1 Technical Enhancements
- More sophisticated contribution quantification methods
- Integration with blockchain for immutable citation records
- Enhanced visualization tools for knowledge graphs

### 8.2 Policy Integration
- Alignment with academic evaluation systems
- Integration with publisher policies and platforms
- Standards development for AI attribution

### 8.3 Ecosystem Expansion
- Application to domains beyond scientific literature
- Integration with creative works and humanities
- Support for public knowledge resources and education

## 9. References

1. Smith, J., & Johnson, T. (2023). "A Framework for AI-Driven Citation Impact Factor." *Journal of Scientific Communication*, 45(3), 234-251.

2. Garcia, A., et al. (2022). "Knowledge Attribution in Machine Learning Systems." *Proceedings of the International Conference on Machine Learning*, 5678-5690.

3. Williams, R., & Brown, S. (2023). "Quantifying Scientific Contribution to Large Language Models." *Nature Machine Intelligence*, 5, 456-468.

4. Lee, K., et al. (2022). "Using SHAP and LIME for Source Attribution in AI Systems." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 44(8), 3456-3471.

5. Chen, X., & Wang, Y. (2023). "Knowledge Graphs for Scientific Attribution." *Communications of the ACM*, 66(7), 78-89.

## 10. Backend Technical Implementation

The AIC-IF framework is implemented as a backend system designed to track and evaluate citations generated by AI systems. It combines automated citation logging, a knowledge graph of research relationships, validation mechanisms, a real-time registry, and easy-to-use APIs.

### 10.1 Technology Stack

The framework is implemented using:
- **Python**: Core programming language
- **Neo4j**: Graph database for knowledge relationships
- **FastAPI**: For RESTful API services
- **PostgreSQL**: For structured citation logs

### 10.2 Citation Tracking

Automated Logging: Whenever an AI system produces content with citations, the framework automatically captures each citation. This involves parsing the AI's output for reference entries or DOIs and sending them to the backend.

Metadata Storage: Each citation event is stored with rich metadata, such as:
- DOI or Identifier: A unique identifier for the cited work
- Source Details: Title, journal/conference, or dataset name
- Timestamp: When the citation was generated
- AI System Used: Which AI model produced the citation
- User Interaction Details: Context like user ID or session info

### 10.3 Knowledge Graph Implementation

The Neo4j knowledge graph consists of:

**Nodes and Relationships**:
- Publication Nodes: Each unique cited paper, article, or dataset
- Researcher Nodes: Authors of publications
- Dataset Nodes: Datasets that are cited or associated with publications

**Structured Relationships**:
- "CITES": Links an AI-generated document to the work it references
- "AUTHORED_BY": Connects a Publication node to its Researcher nodes
- "REFERENCED_IN": Links a Dataset node to a Publication that cites it

### 10.4 API Integration

A RESTful API built with FastAPI exposes endpoints for logging and querying citations:

**Key API Endpoints**:
- POST /api/citations: Log one or more citations
- GET /api/citations: Retrieve citation logs based on filters
- Analytics Endpoints: Provide aggregated citation statistics
- Validation Endpoint: Check citation validity

Sample API request payload:
```json
{
  "doi": "10.1038/s41586-024-05782-3",
  "source_title": "Nature Article on XYZ",
  "ai_model": "GPT-4",
  "user_id": "user_123",
  "context": "Answer to a quantum physics query"
}
```

### 10.5 Integration Guidelines for AI Developers

1. Deploy or Access the Service: Host the AIC-IF backend or use a provided instance
2. Log Citations from AI Systems: Call the POST /api/citations endpoint whenever the AI outputs a citation
3. Retrieve Citation Data: Use the GET /api/citations endpoint to retrieve citation logs
4. Institutional Integration: Research institutions can use the logs to complement traditional metrics
5. Custom Extensions: The framework supports additional metadata fields and endpoints 