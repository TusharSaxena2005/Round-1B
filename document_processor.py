import PyPDF2
import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DocumentSection:
    document_name: str
    page_number: int
    section_title: str
    content: str
    section_type: str

class DocumentProcessor:
    def __init__(self):
        # Enhanced section patterns for better title extraction
        self.section_patterns = [
            r'^([A-Z][A-Z\s]{10,60})\s*$',  # ALL CAPS sections (longer titles)
            r'^(\d+\.?\s+[A-Z][a-zA-Z\s]{10,80})\s*$',  # Numbered sections with longer titles
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,8})\s*$',  # Multi-word title case sections
            r'^(Comprehensive Guide to [A-Za-z\s]{5,50})',  # Comprehensive guides
            r'^(Guide to [A-Za-z\s]{5,50})',  # General guides
            r'^([A-Z][a-z]+\s+in\s+[A-Z][a-z\s]{5,30})',  # "Something in Location" format
            r'^([A-Z][a-z]+\s+and\s+[A-Z][a-z\s]{5,30})',  # "Something and Something" format
            r'^(Top\s+\d+\s+[A-Za-z\s]{5,40})',  # "Top X Something" format
            r'^(Best\s+[A-Za-z\s]{5,40})',  # "Best Something" format
            r'^([A-Z][a-z]+\s+Tips\s+and\s+Tricks)',  # Tips and tricks sections
            r'^([A-Z][a-z]+\s+Activities)',  # Activity sections
            r'^([A-Z][a-z]+\s+Experiences)',  # Experience sections
            r'^([A-Z][a-z]+\s+Adventures)',  # Adventure sections
            r'^(Nightlife\s+and\s+Entertainment)',  # Entertainment sections
            r'^(Coastal\s+Adventures)',  # Coastal sections
        ]
        
        # Skip generic titles that are too common or vague
        self.skip_titles = {
            'introduction', 'overview', 'preface', 'foreword', 'contents', 
            'table of contents', 'index', 'bibliography', 'references',
            'conclusion', 'summary', 'about', 'acknowledgments',
            'key attractions', 'attractions', 'things to do', 'activities',
            'restaurants', 'hotels', 'places', 'locations', 'sites'
        }
        
        # Preferred specific title patterns
        self.preferred_patterns = {
            'coastal': 'Coastal Adventures and Beach Activities',
            'nightlife': 'Nightlife and Entertainment Options', 
            'culinary': 'Culinary Experiences and Food Tours',
            'packing': 'Comprehensive Packing Guide and Travel Tips',
            'water activities': 'Water Sports and Marine Activities',
            'historical sites': 'Historical Landmarks and Cultural Sites',
            'major cities': 'Guide to Major Cities and Destinations',
            'restaurants': 'Dining Guide and Restaurant Recommendations',
            'famous dishes': 'Regional Cuisine and Traditional Dishes',
            'local experiences': 'Authentic Local Experiences and Culture',
            'artistic': 'Art, Museums and Cultural Attractions'
        }
    
    def extract_sections(self, pdf_path: str) -> List[DocumentSection]:
        sections = []
        document_name = pdf_path.split('/')[-1].replace('.pdf', '').split('\\')[-1]
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    page_sections = self._extract_page_sections(text, document_name, page_num)
                    sections.extend(page_sections)
                    
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
        
        return sections
    
    def _extract_page_sections(self, text: str, doc_name: str, page_num: int) -> List[DocumentSection]:
        sections = []
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        # First pass: collect all potential section headers
        potential_headers = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            section_title = self._identify_section_header(line)
            if section_title and section_title.lower() not in self.skip_titles:
                potential_headers.append((i, section_title, line))
        
        # If we found meaningful headers, use them
        if potential_headers:
            for i, (line_idx, section_title, original_line) in enumerate(potential_headers):
                # Get content between this header and the next
                start_idx = line_idx + 1
                end_idx = potential_headers[i + 1][0] if i + 1 < len(potential_headers) else len(lines)
                
                content_lines = []
                for j in range(start_idx, end_idx):
                    if j < len(lines) and lines[j].strip():
                        content_lines.append(lines[j].strip())
                
                if content_lines:  # Only add if there's actual content
                    sections.append(DocumentSection(
                        document_name=doc_name,
                        page_number=page_num,
                        section_title=section_title,
                        content=' '.join(content_lines),
                        section_type=self._classify_section_type(section_title)
                    ))
        else:
            # Fallback: create sections based on content structure
            sections.extend(self._extract_content_based_sections(text, doc_name, page_num))
        
        return sections
    
    def _extract_content_based_sections(self, text: str, doc_name: str, page_num: int) -> List[DocumentSection]:
        """Extract sections based on content analysis when headers aren't clear"""
        sections = []
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
        
        current_section = None
        current_content = []
        
        for para in paragraphs:
            # Look for content that suggests a new section
            first_sentence = para.split('.')[0] if '.' in para else para[:100]
            
            # Check if this paragraph starts a new topic
            if self._is_section_start(first_sentence, para):
                # Save previous section
                if current_section and current_content:
                    sections.append(DocumentSection(
                        document_name=doc_name,
                        page_number=page_num,
                        section_title=current_section,
                        content=' '.join(current_content),
                        section_type=self._classify_section_type(current_section)
                    ))
                
                # Start new section
                current_section = self._generate_specific_section_title(first_sentence, para, doc_name)
                current_content = [para]
            else:
                # Add to current section
                if current_section:
                    current_content.append(para)
                else:
                    # First section without clear header
                    current_section = self._generate_specific_section_title(first_sentence, para, doc_name)
                    current_content = [para]
        
        # Add final section
        if current_section and current_content:
            sections.append(DocumentSection(
                document_name=doc_name,
                page_number=page_num,
                section_title=current_section,
                content=' '.join(current_content),
                section_type=self._classify_section_type(current_section)
            ))
        
        return sections
    
    def _is_section_start(self, first_sentence: str, full_para: str) -> bool:
        """Determine if a paragraph starts a new section"""
        # Check for topic indicators
        topic_indicators = [
            'coastal adventures', 'nightlife and entertainment', 'culinary experiences',
            'packing tips', 'general tips', 'water activities', 'cultural experiences',
            'historical sites', 'major cities', 'restaurants and hotels', 'upscale restaurants',
            'famous dishes', 'key attractions', 'local experiences', 'artistic influence'
        ]
        
        first_lower = first_sentence.lower()
        para_lower = full_para.lower()
        
        # Check if paragraph starts with topic indicators
        for indicator in topic_indicators:
            if indicator in first_lower or indicator in para_lower[:100]:
                return True
        
        # Check for list-like content that might indicate a new section
        if len(full_para.split('•')) > 2 or len(full_para.split('-')) > 3:
            return True
        
        return False
    
    def _generate_section_title(self, first_sentence: str, full_para: str) -> str:
        """Generate a meaningful section title from content"""
        # Extract key phrases that could be titles
        content_lower = full_para.lower()
        
        # Look for specific patterns that suggest section topics
        title_patterns = {
            'coastal': 'Coastal Adventures',
            'nightlife': 'Nightlife and Entertainment', 
            'culinary': 'Culinary Experiences',
            'packing': 'General Packing Tips and Tricks',
            'water activities': 'Water Activities',
            'historical sites': 'Key Historical Sites',
            'major cities': 'Comprehensive Guide to Major Cities',
            'restaurants': 'Upscale Restaurants',
            'famous dishes': 'Famous Dishes',
            'attractions': 'Key Attractions',
            'local experiences': 'Local Experiences',
            'artistic': 'Artistic Influence'
        }
        
        for pattern, title in title_patterns.items():
            if pattern in content_lower:
                return title
        
        # Fallback: use first meaningful phrase
        words = first_sentence.split()
        if len(words) > 3:
            return ' '.join(words[:6]).title()
        
        return first_sentence.title()
    
    def _generate_specific_section_title(self, first_sentence: str, full_para: str, doc_name: str) -> str:
        """Generate a specific, meaningful section title from content"""
        content_lower = full_para.lower()
        doc_lower = doc_name.lower()
        
        # Context-aware title generation based on document type and content
        if 'things to do' in doc_lower or 'activities' in doc_lower:
            if 'coastal' in content_lower or 'beach' in content_lower or 'sea' in content_lower:
                return 'Coastal Adventures and Beach Activities'
            elif 'nightlife' in content_lower or 'entertainment' in content_lower:
                return 'Nightlife and Entertainment Options'
            elif 'water' in content_lower and ('sport' in content_lower or 'activity' in content_lower):
                return 'Water Sports and Marine Activities'
            elif 'cultural' in content_lower or 'museum' in content_lower:
                return 'Cultural Attractions and Museums'
        
        elif 'cuisine' in doc_lower or 'food' in doc_lower:
            if 'experience' in content_lower or 'tour' in content_lower:
                return 'Culinary Experiences and Food Tours'
            elif 'dish' in content_lower or 'traditional' in content_lower:
                return 'Regional Cuisine and Traditional Dishes'
            elif 'restaurant' in content_lower or 'dining' in content_lower:
                return 'Dining Guide and Restaurant Recommendations'
        
        elif 'tips' in doc_lower or 'tricks' in doc_lower:
            if 'packing' in content_lower:
                return 'Comprehensive Packing Guide and Travel Tips'
            elif 'budget' in content_lower or 'money' in content_lower:
                return 'Budget Planning and Money-Saving Tips'
            elif 'transport' in content_lower or 'travel' in content_lower:
                return 'Transportation and Getting Around'
        
        elif 'cities' in doc_lower:
            if 'attraction' in content_lower:
                return 'Major City Attractions and Landmarks'
            elif 'experience' in content_lower or 'local' in content_lower:
                return 'Authentic Local Experiences and Culture'
            elif 'artistic' in content_lower or 'art' in content_lower:
                return 'Art Districts and Cultural Neighborhoods'
        
        elif 'history' in doc_lower:
            if 'montpellier' in content_lower:
                return 'Historical Landmarks in Montpellier'
            elif 'aix' in content_lower or 'provence' in content_lower:
                return 'Historical Sites in Aix-en-Provence'
            elif 'site' in content_lower:
                return 'Important Historical Sites and Monuments'
        
        # Look for specific location mentions
        locations = ['montpellier', 'marseille', 'nice', 'cannes', 'aix-en-provence', 'avignon', 'saint-tropez']
        for location in locations:
            if location in content_lower:
                return f'Guide to {location.title()}'
        
        # Extract meaningful phrases from content
        sentences = full_para.split('.')
        for sentence in sentences[:2]:  # Check first two sentences
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 80:
                # Clean up and use as title if it's descriptive
                if any(word in sentence.lower() for word in ['comprehensive', 'guide', 'ultimate', 'complete']):
                    return sentence
        
        # Fallback: use a cleaned version of the first meaningful phrase
        words = first_sentence.split()
        if len(words) > 3:
            clean_title = ' '.join(words[:8]).title()
            return clean_title if len(clean_title) < 80 else ' '.join(words[:5]).title()
        
        return first_sentence.title()[:50]
    
    def _identify_section_header(self, line: str) -> str:
        # Skip if it's a generic title we want to avoid
        if line.lower().strip() in self.skip_titles:
            return None
        
        # Enhanced pattern matching for better titles
        for pattern in self.section_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if title.lower() not in self.skip_titles and len(title) > 10:
                    return title
        
        # Look for specific meaningful section headers
        if len(line) < 120 and len(line) > 15:  # Reasonable header length
            line_lower = line.lower()
            
            # Specific patterns we want to capture
            meaningful_patterns = [
                'comprehensive guide to', 'ultimate guide to', 'complete guide to',
                'culinary experiences', 'coastal adventures', 'nightlife and entertainment',
                'historical landmarks', 'packing guide', 'travel tips', 'dining guide',
                'cultural attractions', 'water sports', 'local experiences'
            ]
            
            for pattern in meaningful_patterns:
                if pattern in line_lower:
                    return line
        
        return None
    
    def _classify_section_type(self, section_title: str) -> str:
        title_lower = section_title.lower()
        
        if any(word in title_lower for word in ['abstract', 'summary']):
            return 'summary'
        elif any(word in title_lower for word in ['introduction', 'background']):
            return 'introduction'
        elif any(word in title_lower for word in ['method', 'approach', 'technique']):
            return 'methodology'
        elif any(word in title_lower for word in ['result', 'finding', 'outcome']):
            return 'results'
        elif any(word in title_lower for word in ['discussion', 'analysis']):
            return 'analysis'
        elif any(word in title_lower for word in ['conclusion', 'future']):
            return 'conclusion'
        elif any(word in title_lower for word in ['financial', 'revenue', 'profit']):
            return 'financial'
        else:
            return 'general'
