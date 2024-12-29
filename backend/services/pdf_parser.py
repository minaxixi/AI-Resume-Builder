import pdfplumber
import re

class PDFParser:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and format the extracted text
        """
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Remove excessive spaces
        text = re.sub(r' +', ' ', text)
        
        # Fix spacing after periods
        text = re.sub(r'\.(?! )', '. ', text)
        
        # Fix spacing after commas
        text = re.sub(r',(?! )', ', ', text)
        
        # Remove spaces at the beginning of lines
        text = re.sub(r'\n\s+', '\n', text)
        
        # Remove spaces at the end of lines
        text = re.sub(r'\s+\n', '\n', text)
        
        # Ensure sections are properly separated
        text = re.sub(r'([a-z])\n([A-Z])', r'\1\n\n\2', text)
        
        return text.strip()

    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """
        Extract text from a PDF file using pdfplumber
        
        Args:
            pdf_file (file-like object): Uploaded PDF file
        
        Returns:
            str: Extracted and cleaned text from the PDF
        """
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text_content = []
                for page in pdf.pages:
                    # Extract text with better word spacing
                    text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if text:
                        text_content.append(text)
                
                # Join all pages with proper spacing
                full_text = '\n'.join(text_content)
                
                # Clean and format the text
                cleaned_text = PDFParser.clean_text(full_text)
                
                return cleaned_text
                
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
