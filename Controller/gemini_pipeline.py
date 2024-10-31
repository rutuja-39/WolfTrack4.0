'''
MIT License

Copyright (c) 2024 MD NAZMUL HAQUE, KISHAN KUMAR GANGULY, RAVI 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from PyPDF2 import PdfFileReader
import numpy as np
import os
import google.generativeai as genai
        
API_KEY = "" #add gemini API key
def get_gemini_feedback(pdf_path):
    if pdf_path:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        sample_pdf = genai.upload_file(pdf_path)
        prompt = "critique the following resume on the basis of its conciseness, use of action words and numbers. Give suggestions on the 1. education section, then the 2. experiences section, then the 3. skills section and finally the 4. projects section. Give these suggestions on these four sections in the form of four paragraphs and label them Section 1, Section 2, Section 3 and Section 4 respectively, each separated by a line. Make sure each paragraph is atleast 50-70 words long." 
        try:
            response = model.generate_content(
                [prompt, sample_pdf],
                generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    candidate_count=1,
                    max_output_tokens=10000,
                    temperature=0.8,
                ),
            )
            return response.text

        except Exception as e:
            print(f"An error occurred: {e}")
        
        return None
