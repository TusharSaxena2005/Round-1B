# Persona-Driven Document Intelligence - Round 1B

## Overview
A lightweight, CPU-only document intelligence system that extracts and ranks document sections based on specific personas and their job-to-be-done requirements. The solution processes PDF collections and delivers persona-aware content analysis without requiring any ML models or internet connectivity.

## Approach

### Core Methodology
Our solution implements a **rule-based algorithmic approach** rather than ML models to ensure:
- CPU-only execution (no GPU requirements)
- Model size ≤ 1GB (actual: ~50MB)
- Processing time ≤ 60 seconds
- Complete offline capability

### System Architecture

#### 1. Document Processing Pipeline
- **PDF Extraction**: Uses PyPDF2 for efficient text extraction
- **Section Identification**: Pattern-based recognition using regex to identify meaningful section headers
- **Content Structuring**: Organizes extracted text into structured sections with metadata

#### 2. Persona-Aware Analysis Engine
- **Persona Classification**: Maps user descriptions to predefined persona types (researcher, student, analyst, entrepreneur, travel planner, etc.)
- **Keyword Dictionaries**: Each persona has associated keywords that influence relevance scoring
- **Section Priorities**: Different content types are weighted based on persona preferences

#### 3. Multi-Factor Relevance Scoring
Content relevance calculated using weighted factors:
- **Persona Keyword Matching** (10% weight): Domain-specific terminology alignment
- **Section Type Priority** (30-90% weight): Content category preferences by persona
- **Job-Specific Alignment** (15% weight): Dynamic keyword extraction from job description
- **Content Quality Metrics** (10% weight): Length, structure, and technical density indicators

#### 4. Intelligent Content Refinement
- **Key Sentence Extraction**: Identifies most relevant sentences using keyword density scoring
- **Context-Aware Summarization**: Creates focused summaries highlighting job-relevant content
- **Relevance Explanation**: Generates explanations for why content matters to the specific task

## Libraries and Dependencies

### Required Libraries
- **PyPDF2 (v3.0.1)**: PDF text extraction and processing
- **Python Standard Library**: 
  - `re`: Regular expressions for pattern matching
  - `json`: Data serialization
  - `datetime`: Timestamp generation
  - `pathlib`: File system operations
  - `argparse`: Command-line interface
  - `dataclasses`: Structured data containers

### No ML Models
The solution deliberately avoids machine learning models to meet constraints:
- No TensorFlow, PyTorch, or similar frameworks
- No pre-trained language models
- No neural networks or deep learning components
- Pure algorithmic processing ensures predictable performance

## Solution Structure

```
Round1B/
├── main.py                    # Main application entry point
├── document_processor.py      # PDF processing and section extraction
├── persona_analyzer.py        # Persona-aware content analysis
├── output_formatter.py        # JSON output formatting
├── run_example.py            # Helper script for easy execution
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── README.md               # This documentation
├── Input/                  # Input directory
│   ├── PDFs/              # Place PDF documents here
│   └── challenge1b_input.json # Persona and job configuration
└── Output/                # Output directory
    └── challenge1b_output.json # Generated analysis results
```

## How to Build and Run

### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized execution)

### Docker Execution (Recommended)

1. **Build Image**
   ```bash
   docker build -t persona-doc-intelligence .
   ```

2. **Run Container**
   ```bash
   # PowerShell (Windows)
   docker run -v "$(Get-Location)\Input:/app/Input" -v "$(Get-Location)\Output:/app/Output" persona-doc-intelligence
   
   # Command Prompt (Windows) - use full paths
   docker run -v "C:\path\to\project\Input:/app/Input" -v "C:\path\to\project\Output:/app/Output" persona-doc-intelligence
   ```

### Quick Start (Local Execution)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Input Structure**
   ```bash
   python run_example.py
   # Type 'y' when prompted to create folder structure
   ```

3. **Add Your Documents**
   - Place PDF files in: `Input/PDFs/`
   - Configure: `Input/challenge1b_input.json`
   ```json
   {
     "persona": "Travel Planner",
     "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends"
   }
   ```

4. **Execute Processing**
   ```bash
   python run_example.py
   ```

5. **View Results**
   - Check: `Output/challenge1b_output.json`


### Direct Command Usage
```bash
python main.py --documents doc1.pdf doc2.pdf --persona "Your Persona" --job "Your Task" --output result.json
```

## Performance Characteristics

### Optimization Features
- **Efficient Text Processing**: Streamlined regex operations and string processing
- **Cached Lookups**: Pre-computed persona keyword dictionaries
- **Memory Management**: Processes documents sequentially to minimize memory usage
- **Fast I/O**: Direct file operations without unnecessary data transformations

### Benchmark Performance
- **Processing Speed**: 3-7 PDF documents in <60 seconds
- **Memory Usage**: ~100-200MB RAM during processing
- **Storage**: <100MB for complete application
- **Scalability**: Linear performance scaling with document count

## Input/Output Format

### Input Structure
```json
{
  "persona": "Travel Planner",
  "job_to_be_done": "Plan a comprehensive trip itinerary"
}
```

### Output Structure
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan trip itinerary",
    "processing_timestamp": "2025-07-26T10:30:45.123456"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Comprehensive Travel Guide",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Key travel information...",
      "page_number": 1
    }
  ]
}
```

## Constraint Compliance

✅ **CPU Only**: No GPU dependencies, pure algorithmic processing  
✅ **Model Size ≤ 1GB**: ~50MB total application size  
✅ **Processing Time ≤ 60s**: Optimized for 3-7 document collections  
✅ **No Internet**: Completely offline, self-contained execution  
✅ **Generalization**: Handles diverse domains (academic, business, travel, etc.)  

## Troubleshooting

### Common Issues
- **Import Errors**: Run `pip install PyPDF2`
- **Docker Build Fails**: Ensure Dockerfile and all .py files exist
- **Permission Errors**: Run terminal as administrator
- **Timeout Issues**: Reduce number of input documents

### Support
For additional help or issues, refer to the execution instructions in the Docker commands or run the system with verbose output for debugging.
