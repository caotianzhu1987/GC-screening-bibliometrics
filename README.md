Project Overview
This repository applies bibliometric methods to analyze the evolution of gastric cancer (GC) screening technologies from 2004–2024. By integrating lifecycle models and knowledge graphs, we map research trends, collaboration networks, and translational gaps in endoscopy, liquid biopsy, and AI-aided screening.
Repository Structure
├── /data                # Datasets (CSV/JSON)  
│   ├── raw_data.csv     # Raw screening tech publications (2004–2024)  
│   └── processed_data   # Cleaned data for bibliometric analysis  
├── /scripts             # Analysis code  
│   ├── vosviewer_analysis.py  # Keyword co-occurrence & clustering  
│   ├── citespace_script.R     # Citation network & timeline mapping  
│   └── prophet_model.py        # Tech lifecycle prediction (Prophet)  
└── /docs                # Documentation  
    ├── workflow.md      # Step-by-step analysis pipeline  
    └── requirements.md  # Dependencies & environment setup  
    Usage Guide
1. Dependencies
Python (≥3.8): For data processing and Prophet modeling.
Core libraries: pandas, matplotlib, fbprophet
R (≥4.0): For VOSviewer/CiteSpace visualization.
Core libraries: tidyverse, igraph
Bibliometric Tools: VOSviewer, CiteSpace (install separately; scripts include export/import workflows).
2. Quick Start
Step 1: Clone Repository
git clone https://github.com/caotianzhu1987/GC-screening-bibliometric.git  
cd GC-screening-bibliometric
Step 2: Set Up Environment
Python Dependencies:
pip install -r docs/requirements.txt
Step 3: Run Analysis
Data Preprocessing (Python):
python scripts/data_cleaning.py  # Generates processed_data/
Bibliometric Mapping (VOSviewer/R):
For keyword networks: Import data/processed_data/keywords.csv into VOSviewer, run clustering.
For citation timelines: Use scripts/citespace_script.R to generate JSON outputs for CiteSpace.
Lifecycle Prediction (Python):
python scripts/prophet_model.py  # Predicts tech growth curves (endoscopy, liquid biopsy, etc.)
3. Outputs
Visualizations: Keyword co-occurrence maps (/docs/figures), citation timelines, lifecycle charts.
Reports: docs/workflow.md details analysis steps; results/ stores raw model outputs (CSV/JSON).
For collaboration or issues, open a GitHub Issue or contact [xy22010602@163.com/GitHub handle].
