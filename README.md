# CrewAI & OpenRouter Workspace

A professional, high-performance workspace for developing, testing, and orchestrating multi-agent systems using the **CrewAI** framework and **OpenRouter** LLM models.

---

## 📂 Project Structure

```text
Crew-ai-repo/
├── .venv/            # Python 3.13 isolated virtual environment
├── .env              # Environment secrets and model configurations (git-ignored)
├── req.txt           # Python package dependencies
├── main.py           # Multi-agent sequential orchestration entry point
├── README.md         # Developer documentation (this file)
└── GEMINI.md         # AI Agent workspace behavior & coding standards
```

---

## 🚀 Getting Started & Installation

This project is built using **Python 3.13** to avoid version conflicts with CrewAI dependencies under newer Python versions (such as Python 3.14).

### 1. Set Up the Virtual Environment

Create and activate the virtual environment:

```bash
# Recreate if needed, or simply activate
python3.13 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies

Install the pinned stable dependencies:

```bash
pip install --upgrade pip
pip install -r req.txt
```

### 3. Environment Variables Configuration

Duplicate or edit the `.env` file at the root of the project:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openrouter/google/gemini-2.5-flash
OTEL_SDK_DISABLED=true
```

---

## 💻 Execution

To run the sample multi-agent execution (sequential research and writing flow):

```bash
# Ensure the virtual environment is used
.venv/bin/python main.py
```

---

## 🛠️ Key Technologies Used

- **[CrewAI](https://github.com/crewAIInc/crewAI):** Leading multi-agent orchestration framework.
- **[OpenRouter](https://openrouter.ai/):** Unified API routing for elite open-source and proprietary language models.
- **[python-dotenv](https://github.com/theofidry/django-dotenv-filename):** Easy management of environment variables.
