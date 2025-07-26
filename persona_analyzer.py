import re
from typing import List, Dict, Tuple
from collections import Counter
from dataclasses import dataclass
from document_processor import DocumentSection

@dataclass
class RankedSection:
    document_name: str
    page_number: int
    section_title: str
    importance_rank: int
    relevance_score: float
    content: str

@dataclass
class RefinedSubsection:
    document_name: str
    page_number: int
    refined_text: str
    relevance_explanation: str

class PersonaAnalyzer:
    def __init__(self):
        # Persona-specific keywords and priorities
        self.persona_keywords = {
            'researcher': ['methodology', 'experiment', 'data', 'analysis', 'hypothesis', 'study', 'research'],
            'student': ['concept', 'definition', 'example', 'theory', 'principle', 'formula', 'equation'],
            'analyst': ['trend', 'performance', 'metric', 'benchmark', 'comparison', 'forecast', 'insight'],
            'entrepreneur': ['market', 'opportunity', 'strategy', 'business', 'revenue', 'growth', 'innovation'],
            'journalist': ['fact', 'source', 'evidence', 'quote', 'statement', 'report', 'investigation'],
            'travel': ['destination', 'place', 'location', 'visit', 'culture', 'experience', 'attraction']
        }
        
        self.section_priorities = {
            'researcher': {'methodology': 0.9, 'results': 0.8, 'analysis': 0.7, 'introduction': 0.6},
            'student': {'introduction': 0.9, 'summary': 0.8, 'methodology': 0.6, 'conclusion': 0.5},
            'analyst': {'financial': 0.9, 'results': 0.8, 'analysis': 0.7, 'summary': 0.6},
            'entrepreneur': {'summary': 0.9, 'analysis': 0.8, 'results': 0.7, 'introduction': 0.5},
            'journalist': {'summary': 0.9, 'introduction': 0.8, 'results': 0.7, 'analysis': 0.6},
            'travel': {'summary': 0.9, 'introduction': 0.8, 'general': 0.7, 'analysis': 0.6}
        }
    
    def rank_sections(self, sections: List[DocumentSection], persona: str, job: str) -> List[RankedSection]:
        scored_sections = []
        
        for section in sections:
            score = self._calculate_relevance_score(section, persona, job)
            scored_sections.append((section, score))
        
        # Sort by relevance score
        scored_sections.sort(key=lambda x: x[1], reverse=True)
        
        # Convert to ranked sections
        ranked_sections = []
        for rank, (section, score) in enumerate(scored_sections, 1):
            ranked_sections.append(RankedSection(
                document_name=section.document_name,
                page_number=section.page_number,
                section_title=section.section_title,
                importance_rank=rank,
                relevance_score=score,
                content=section.content
            ))
        
        return ranked_sections
    
    def _calculate_relevance_score(self, section: DocumentSection, persona: str, job: str) -> float:
        score = 0.0
        
        # Persona-based scoring
        persona_type = self._identify_persona_type(persona)
        if persona_type in self.persona_keywords:
            keywords = self.persona_keywords[persona_type]
            content_lower = section.content.lower()
            keyword_matches = sum(1 for keyword in keywords if keyword in content_lower)
            score += keyword_matches * 0.1
        
        # Section type priority
        if persona_type in self.section_priorities:
            section_priority = self.section_priorities[persona_type].get(section.section_type, 0.3)
            score += section_priority
        
        # Job-specific keyword matching
        job_keywords = self._extract_keywords_from_job(job)
        content_lower = section.content.lower()
        job_matches = sum(1 for keyword in job_keywords if keyword.lower() in content_lower)
        score += job_matches * 0.15
        
        # Content quality factors
        score += self._assess_content_quality(section.content)
        
        return score
    
    def _identify_persona_type(self, persona: str) -> str:
        persona_lower = persona.lower()
        
        if any(word in persona_lower for word in ['researcher', 'phd', 'scientist']):
            return 'researcher'
        elif any(word in persona_lower for word in ['student', 'undergraduate', 'graduate']):
            return 'student'
        elif any(word in persona_lower for word in ['analyst', 'investment', 'financial']):
            return 'analyst'
        elif any(word in persona_lower for word in ['entrepreneur', 'business', 'startup']):
            return 'entrepreneur'
        elif any(word in persona_lower for word in ['journalist', 'reporter', 'writer']):
            return 'journalist'
        elif any(word in persona_lower for word in ['travel', 'tourist', 'trip', 'vacation']):
            return 'travel'
        else:
            return 'general'
    
    def _extract_keywords_from_job(self, job: str) -> List[str]:
        # Extract meaningful keywords from job description
        words = re.findall(r'\b[a-zA-Z]{3,}\b', job.lower())
        # Filter out common words
        stopwords = {'the', 'and', 'for', 'with', 'given', 'from', 'that', 'this', 'will', 'can', 'should'}
        return [word for word in words if word not in stopwords]
    
    def _assess_content_quality(self, content: str) -> float:
        # Simple content quality metrics
        quality_score = 0.0
        
        # Length factor (moderate length preferred)
        length = len(content.split())
        if 50 <= length <= 500:
            quality_score += 0.1
        elif 20 <= length <= 1000:
            quality_score += 0.05
        
        # Technical term density
        technical_indicators = ['analysis', 'research', 'study', 'method', 'result', 'data']
        tech_count = sum(1 for term in technical_indicators if term in content.lower())
        quality_score += min(tech_count * 0.02, 0.1)
        
        return quality_score
    
    def analyze_subsections(self, top_sections: List[RankedSection], persona: str, job: str) -> List[RefinedSubsection]:
        refined_subsections = []
        
        for section in top_sections[:5]:  # Top 5 sections
            refined_text = self._extract_key_sentences(section.content, persona, job)
            explanation = self._generate_relevance_explanation(section, persona, job)
            
            refined_subsections.append(RefinedSubsection(
                document_name=section.document_name,
                page_number=section.page_number,
                refined_text=refined_text,
                relevance_explanation=explanation
            ))
        
        return refined_subsections
    
    def _extract_key_sentences(self, content: str, persona: str, job: str) -> str:
        sentences = re.split(r'[.!?]+', content)
        job_keywords = self._extract_keywords_from_job(job)
        persona_type = self._identify_persona_type(persona)
        
        scored_sentences = []
        for sentence in sentences:
            if len(sentence.strip()) < 20:
                continue
                
            score = 0
            sentence_lower = sentence.lower()
            
            # Job keyword matching
            for keyword in job_keywords:
                if keyword.lower() in sentence_lower:
                    score += 1
            
            # Persona keyword matching
            if persona_type in self.persona_keywords:
                for keyword in self.persona_keywords[persona_type]:
                    if keyword in sentence_lower:
                        score += 0.5
            
            scored_sentences.append((sentence.strip(), score))
        
        # Select top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sent for sent, score in scored_sentences[:3] if score > 0]
        
        return '. '.join(top_sentences) + '.' if top_sentences else content[:200] + '...'
    
    def _generate_relevance_explanation(self, section: RankedSection, persona: str, job: str) -> str:
        explanations = []
        
        persona_type = self._identify_persona_type(persona)
        if section.section_title.lower() in ['methodology', 'results', 'analysis']:
            explanations.append(f"Contains {section.section_title.lower()} relevant to {persona_type} work")
        
        job_keywords = self._extract_keywords_from_job(job)
        matching_keywords = [kw for kw in job_keywords if kw.lower() in section.content.lower()]
        if matching_keywords:
            explanations.append(f"Addresses key job requirements: {', '.join(matching_keywords[:3])}")
        
        if not explanations:
            explanations.append("Provides contextual information relevant to the specified task")
        
        return '; '.join(explanations)
