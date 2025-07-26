import json
import argparse
from datetime import datetime
from pathlib import Path
from document_processor import DocumentProcessor
from persona_analyzer import PersonaAnalyzer
from output_formatter import OutputFormatter

def main():
    parser = argparse.ArgumentParser(description='Persona-Driven Document Intelligence')
    parser.add_argument('--documents', nargs='+', required=True, help='Paths to PDF documents')
    parser.add_argument('--persona', required=True, help='Persona description')
    parser.add_argument('--job', required=True, help='Job-to-be-done description')
    parser.add_argument('--output', default='output.json', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Initialize components
    doc_processor = DocumentProcessor()
    persona_analyzer = PersonaAnalyzer()
    output_formatter = OutputFormatter()
    
    # Process documents
    print("Processing documents...")
    extracted_sections = []
    
    for doc_path in args.documents:
        print(f"Processing: {doc_path}")
        sections = doc_processor.extract_sections(doc_path)
        extracted_sections.extend(sections)
    
    # Analyze with persona context
    print("Analyzing with persona context...")
    ranked_sections = persona_analyzer.rank_sections(
        extracted_sections, 
        args.persona, 
        args.job
    )
    
    # Generate subsection analysis
    print("Generating subsection analysis...")
    refined_subsections = persona_analyzer.analyze_subsections(
        ranked_sections[:10],  # Top 10 sections
        args.persona,
        args.job
    )
    
    # Format output (this will generate a fresh timestamp)
    print("Formatting output...")
    print(f"Current time: {datetime.now().isoformat()}")
    output_data = output_formatter.format_output(
        documents=args.documents,
        persona=args.persona,
        job=args.job,
        sections=ranked_sections,
        subsections=refined_subsections
    )
    
    # Verify timestamp is current
    print(f"Generated timestamp: {output_data['metadata']['processing_timestamp']}")
    
    # Save output immediately after formatting
    print(f"Saving output to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Processing completed at: {output_data['metadata']['processing_timestamp']}")
    print(f"Output saved to: {args.output}")

if __name__ == "__main__":
    main()
