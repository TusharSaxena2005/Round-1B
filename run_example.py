#!/usr/bin/env python3
"""
Example script for running the Persona-Driven Document Intelligence system

QUICK START:
1. Install dependencies: pip install PyPDF2
2. Put your PDF files in: Input/PDFs/
3. Edit: Input/challenge1b_input.json
4. Run: python run_example.py
5. Check results in: Output/challenge1b_output.json
"""

import subprocess
import sys
import json
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyPDF2
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def show_quick_start():
    """Show quick start instructions"""
    print("\n🚀 QUICK START GUIDE:")
    print("=" * 50)
    print("1️⃣  Install dependencies: pip install PyPDF2")
    print("2️⃣  Put your PDF files in: Input/PDFs/")
    print("3️⃣  Edit persona & job in: Input/challenge1b_input.json")
    print("4️⃣  Run this script: python run_example.py")
    print("5️⃣  Check results in: Output/challenge1b_output.json")
    print("\n💡 Alternative: Direct command")
    print("   python main.py --documents file1.pdf file2.pdf --persona 'Your Role' --job 'Your Task' --output result.json")

def check_structure():
    """Check if Input/Output folder structure exists"""
    input_dir = Path("Input")
    pdfs_dir = input_dir / "PDFs"
    input_json = input_dir / "challenge1b_input.json"
    output_dir = Path("Output")
    
    missing = []
    if not input_dir.exists():
        missing.append("Input/ folder")
    if not pdfs_dir.exists():
        missing.append("Input/PDFs/ folder")
    if not input_json.exists():
        missing.append("Input/challenge1b_input.json file")
    if not output_dir.exists():
        missing.append("Output/ folder")
    
    return missing

def create_structure():
    """Create the required directory structure"""
    print("\n📁 Creating directory structure...")
    
    # Create directories
    input_dir = Path("Input")
    pdfs_dir = input_dir / "PDFs"
    output_dir = Path("Output")
    
    pdfs_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create example input file
    example_input = {
        "persona": "Travel Enthusiast and Blogger",
        "job_to_be_done": "Plan a comprehensive 2-week travel itinerary for South of France including must-visit places, local cuisine, and cultural experiences"
    }
    
    input_file = input_dir / "challenge1b_input.json"
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(example_input, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created structure:")
    print(f"   📁 Input/")
    print(f"   ├── 📁 PDFs/  <- PUT YOUR PDF FILES HERE")
    print(f"   └── 📄 challenge1b_input.json")
    print(f"   📁 Output/")
    print(f"   └── 📄 challenge1b_output.json (will be generated)")
    print(f"\n📝 Next steps:")
    print(f"   1. Copy your PDF files to: Input/PDFs/")
    print(f"   2. Edit Input/challenge1b_input.json to match your persona and job")
    print(f"   3. Run: python run_example.py")

def load_input_config():
    """Load configuration from Input/challenge1b_input.json"""
    input_file = Path("Input/challenge1b_input.json")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return None

def process_documents():
    """Process all documents in Input/PDFs/"""
    print(f"\n📁 Processing documents")
    print("-" * 50)
    
    # Load input configuration
    config = load_input_config()
    if not config:
        print("   ❌ Failed to load input configuration")
        return
    
    # Find PDF files in the Input/PDFs directory
    pdfs_dir = Path("Input/PDFs")
    pdf_files = list(pdfs_dir.glob("*.pdf"))
    if not pdf_files:
        print("   ❌ No PDF files found in Input/PDFs/ directory")
        return
    
    print(f"   📄 Found {len(pdf_files)} PDF files")
    
    # Handle different config formats
    persona = config.get('persona', 'Not specified')
    job = config.get('job_to_be_done', 'Not specified')
    
    # Handle nested dictionaries or dictionary strings
    if isinstance(persona, dict):
        persona = persona.get('role', str(persona))
    if isinstance(job, dict):
        if 'task' in job:
            job = job['task']
        else:
            job = str(job)
    elif isinstance(job, str) and job.startswith('{') and job.endswith('}'):
        try:
            job_dict = eval(job)
            if isinstance(job_dict, dict) and 'task' in job_dict:
                job = job_dict['task']
        except:
            pass  # Keep original if parsing fails
    
    # Ensure they are strings
    persona = str(persona) if persona else 'Not specified'
    job = str(job) if job else 'Not specified'
    
    print(f"   👤 Persona: {persona}")
    print(f"   🎯 Job: {job[:80]}...")
    
    # Prepare output file
    output_dir = Path("Output")
    output_file = output_dir / "challenge1b_output.json"
    
    # Build command with relative paths
    pdf_paths = [str(pdf) for pdf in pdf_files]
    cmd = [
        sys.executable, "main.py",
        "--documents"] + pdf_paths + [
        "--persona", persona,
        "--job", job,
        "--output", str(output_file)
    ]
    
    try:
        print("   🔄 Processing...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"   ✅ Completed successfully -> {output_file}")
            print(f"   📊 Results saved to: Output/challenge1b_output.json")
        else:
            print(f"   ❌ Failed: {result.stderr}")
            if result.stdout:
                print(f"   📝 Output: {result.stdout}")
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout: Processing took longer than 60 seconds")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def run_example():
    """Main function to process documents"""
    print("Persona-Driven Document Intelligence - Document Processor")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Missing required dependency: PyPDF2")
        print("\n📋 Installation options:")
        print("1. Run: pip install PyPDF2")
        print("2. Run: pip install -r requirements.txt")
        
        response = input("\n❓ Would you like me to install PyPDF2 now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if not install_dependencies():
                return
        else:
            print("\n💡 Please install PyPDF2 and run again:")
            print("   pip install PyPDF2")
            return
    
    # Check if structure exists
    missing = check_structure()
    
    if missing:
        print(f"\n❌ Missing: {', '.join(missing)}")
        print("\nExpected directory structure:")
        print("Project/")
        print("├── Input/")
        print("│   ├── PDFs/          <- PUT YOUR PDF FILES HERE")
        print("│   └── challenge1b_input.json")
        print("└── Output/")
        print("    └── challenge1b_output.json (generated)")
        
        # Ask if user wants to create structure
        response = input("\n❓ Would you like to create the required structure? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            create_structure()
        return
    
    # Process documents
    process_documents()

if __name__ == "__main__":
    print("Persona-Driven Document Intelligence System")
    print("Works with Input/Output folder structure")
    
    # Show quick start if no arguments
    if len(sys.argv) == 1:
        show_quick_start()
    
    print("\n📋 Directory Structure Required:")
    print("Project/")
    print("├── Input/")
    print("│   ├── PDFs/                    <- PUT YOUR PDF FILES HERE")
    print("│   │   ├── document1.pdf")
    print("│   │   ├── document2.pdf")
    print("│   │   └── document3.pdf")
    print("│   └── challenge1b_input.json   <- Configure persona and job")
    print("└── Output/")
    print("    └── challenge1b_output.json  <- Generated results")
    print("\n🚀 Usage:")
    print("1. Install dependencies: pip install PyPDF2")
    print("2. Put your PDF files in Input/PDFs/")
    print("3. Edit Input/challenge1b_input.json with your persona and job")
    print("4. Run: python run_example.py")
    print("5. Check results in Output/challenge1b_output.json")
    print("\nStarting document processing...\n")
    run_example()
