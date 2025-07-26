import json
from datetime import datetime
from typing import List, Dict
from persona_analyzer import RankedSection, RefinedSubsection

class OutputFormatter:
    def format_output(self, documents: List[str], persona: str, job: str, 
                     sections: List[RankedSection], subsections: List[RefinedSubsection]) -> Dict:
        
        # Always generate fresh timestamp
        timestamp = datetime.now().isoformat()
        
        # Clean up job description if it's in dictionary format
        if isinstance(job, str) and job.startswith('{') and job.endswith('}'):
            try:
                job_dict = eval(job)
                if isinstance(job_dict, dict) and 'task' in job_dict:
                    job = job_dict['task']
            except:
                pass  # Keep original if parsing fails
        
        output = {
            "metadata": {
                "input_documents": [doc.split('/')[-1].split('\\')[-1] + ('.pdf' if not doc.endswith('.pdf') else '') for doc in documents],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": timestamp  # Fresh timestamp every time
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        # Format extracted sections with correct field order
        for section in sections[:15]:  # Top 15 sections
            document_name = section.document_name
            if not document_name.endswith('.pdf'):
                document_name += '.pdf'
            
            output["extracted_sections"].append({
                "document": document_name,
                "section_title": section.section_title,
                "importance_rank": section.importance_rank,
                "page_number": section.page_number
            })
        
        # Format subsection analysis
        for subsection in subsections:
            document_name = subsection.document_name
            if not document_name.endswith('.pdf'):
                document_name += '.pdf'
                
            output["subsection_analysis"].append({
                "document": document_name,
                "refined_text": subsection.refined_text,
                "page_number": subsection.page_number
            })
        
        return output
