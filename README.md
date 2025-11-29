# cyber-multiagent-adk
Multi-agent AI assistant using Google ADK

1) Clone the repo:

  
   git clone https://github.com/<your-username>/cyber-multiagent-adk.git
   cd cyber-multiagent-adk
 

2) Create venv + install:


   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -U pip
   pip install -e .


3) Set Gemini key:

  
   export GOOGLE_API_KEY="YOUR_KEY"
   export GOOGLE_GENAI_USE_VERTEXAI="FALSE"
  

4) Start ADK Web UI:

   adk web --port 8000

5) Open `http://localhost:8000` → select the `cyber_agent` / `CyberCoordinator` agent and start chatting.
