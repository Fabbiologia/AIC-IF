# AI-Driven Citation Impact Factor (AIC-IF) Framework

## Overview

The AI-Driven Citation Impact Factor (AIC-IF) framework addresses the challenge of tracking, attributing, and crediting scientific contributions in an AI-mediated knowledge ecosystem. As artificial intelligence increasingly mediates our interaction with scientific knowledge, traditional citation systems fail to capture how AI systems utilize existing scholarship.

## Project Structure

- **docs/**: Technical documentation and implementation guides
- **poc/**: Proof of concept implementation
  - **app/**: Flask application implementing core components
  - **templates/**: HTML templates for visualization
  - **static/**: CSS, JavaScript, and other static assets
- **Supplementary_Material.md**: Detailed description of the framework

## Core Components

1. **Citation Registry**: Central repository for citation events
2. **Knowledge Graph**: Representation of relationships between entities
3. **Contribution Analysis**: Quantifies source contributions using SHAP and LIME
4. **Attribution Mechanism**: Distributes credit based on analysis

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for development)
- Neo4j (optional for advanced knowledge graph features)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AIC-IF.git
cd AIC-IF

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd poc
pip install -r requirements.txt
```

### Running the Proof of Concept

```bash
cd poc
python run.py
```

## Citation

If you use this framework in your research, please cite:

```
@article{AIC-IF2023,
  title={AI-Driven Citation Impact Factor Framework},
  author={AIC-IF Team},
  journal={Journal of Scientific Communication},
  year={2023}
}
```

## License

This project is licensed under CC BY-NC-SA 4.0 - see [LICENSE](LICENSE) for details.

## Contact

Please open an issue on this repository for questions or suggestions. 