#!/usr/bin/env python3
"""
Startup script for AI Agentic Workflow Orchestrator
Provides a simple way to start the application with proper configuration.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured."""
    print("🔧 Checking environment...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from template...")
        if Path("env.example").exists():
            subprocess.run(["cp", "env.example", ".env"])
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env and add your GEMINI_API_KEY")
            return False
        else:
            print("❌ env.example not found")
            return False
    
    # Check if GEMINI_API_KEY is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("⚠️  OPENAI_API_KEY not configured in .env file")
            print("   Please edit .env and add your actual API key")
            return False
        else:
            print("✅ OPENAI_API_KEY is configured")
    except ImportError:
        print("⚠️  python-dotenv not installed")
        return False
    
    return True

def check_dependencies():
    """Check if all dependencies are installed."""
    print("📦 Checking dependencies...")
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("requests", "requests"), 
        ("python-dotenv", "dotenv"),
        ("openai", "openai"),
        ("pydantic", "pydantic")
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed")
        return True

def start_application():
    """Start the application."""
    print("🚀 Starting AI Agentic Workflow Orchestrator...")
    print("=" * 50)
    
    # Check environment and dependencies
    if not check_environment():
        print("\n❌ Environment not properly configured.")
        print("Please fix the issues above and try again.")
        return 1
    
    if not check_dependencies():
        print("\n❌ Dependencies not installed.")
        print("Please run: pip install -r requirements.txt")
        return 1
    
    print("\n✅ Environment ready!")
    print("\n🌐 Starting application...")
    print("   The application will be available at:")
    print("   - Main: http://localhost:8502")
    print("   - About: http://localhost:8502")
    print("\n⏳ Starting Streamlit server (this may take a few seconds)...")
    
    try:
        # Start the Streamlit application
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", 
            "app.py",
            "--server.port", "8502",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        return 1

def main():
    """Main function."""
    print("🤖 AI Agentic Workflow Orchestrator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        return 1
    
    return start_application()

if __name__ == "__main__":
    sys.exit(main())
