# FinalRAG

## Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your OpenAI API key


# RAG System

## Prerequisites

Before installing the Python dependencies, you need to install some system dependencies:

1. Poppler (required for pdf2image):
   - macOS: `brew install poppler`
   - Ubuntu/Debian: `sudo apt-get install poppler-utils`
   - Windows: Download from http://blog.alivate.com.au/poppler-windows/

2. Python 3.7 or higher

3. pip (Python package installer)

## Required Python Packages
The following packages are required and will be installed via `requirements.txt`:

- pdf2image: For converting PDF files to images
- Pillow: Python Imaging Library for image processing
- python-dotenv: For managing environment variables
- openai: OpenAI API client
- langchain: For document processing and RAG implementation
- langchain-community: Community extensions for langchain
- langchain-openai: OpenAI integration for langchain
- faiss-cpu: For vector similarity search
- numpy: For numerical computations
- python-docx: For working with Word documents

## Installation

1. Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate


2. Install the required packages:

pip install -r requirements.txt


## Known Issues and Solutions

1. If you encounter issues with pdf2image:
   - Make sure poppler is installed on your system
   - Verify that your virtual environment is activated
   - Try reinstalling the package: `pip install pdf2image`

2. If you encounter version conflicts:
   - Make sure you're using only one virtual environment
   - Try removing and recreating your virtual environment
   - Update pip: `pip install --upgrade pip`

## Usage

### Using vision.py

1. Ensure you have all the required dependencies installed by running:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in your project root with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. Create a `docs` directory in your project root and add your PDF documents:
   ```
   your_project/
   ├── docs/
   │   ├── document1.pdf
   │   ├── document2.pdf
   │   └── ...
   ├── vision.py
   ├── requirements.txt
   └── .env
   ```

4. Open `vision.py` and update the `docs_path` variable to point to your documents directory:
   ```python
   # Change this line in vision.py
   docs_path = "path/to/your/docs/folder"  # e.g., "./docs" or absolute path
   ```

5. To process documents using `vision.py`, run:
   ```bash
   python vision.py
   ```



===============================================




5. Make sure to install poppler for PDF processing:
   - For macOS: `brew install poppler`
   - For Ubuntu: `sudo apt-get install poppler-utils`
   - For Windows: Download from the link provided in the README

[
pip install python-docx
pip install pdf2image
pip install Pillow
pip install python-dotenv
pip install openai
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install faiss-cpu
pip install numpy

For pdf2image to work, you'll need to install poppler:
On Mac: brew install poppler
On Ubuntu: sudo apt-get install poppler-utils
On Windows: Download and install from the poppler website
Make sure you have a .env file in your project directory with your:

 OpenAI API key:your_api_key_here



Run the script:
python vision.py


 
