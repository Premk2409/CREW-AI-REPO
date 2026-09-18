# Workspace Instructions for Gemini CLI & Collaborating Agents
@AGENTS.md

Welcome, Agent. This file outlines critical development instructions, architectural guardrails, and conventions specific to this workspace. You MUST read and strictly adhere to these instructions when modifying or creating code in this repo.

---

## 🐍 1. Python Environment Management
- **Target Version:** This workspace is built exclusively on **Python 3.13** (located at `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`).
- **Do Not Use Python 3.14:** Global `python3` or standard installers may resolve to Python 3.14, which lacks pre-compiled wheels for key dependencies of CrewAI (e.g., `chromadb`, `tiktoken`), leading to Rust compiler errors.
- **Virtual Environment:** Always execute files, run tests, and manage dependencies using the local virtual environment:
  - Python Path: `.venv/bin/python`
  - Pip Path: `.venv/bin/pip`
- **Commands:** Prior to executing any python script, verify your pathing. E.g., `.venv/bin/python main.py` rather than `python3 main.py`.

---

## 🌐 2. OpenRouter Integration Guide
All CrewAI LLM integrations in this repo use **OpenRouter**. Adhere to the following conventions when instantiating language models:

1. **Model Prefix:** Always prepend the model name with `openrouter/` (e.g., `openrouter/google/gemini-2.5-flash` or `openrouter/anthropic/claude-3.7-sonnet`).
2. **Explicit LLM Configurations:** Never rely on default OpenAI parameters. Always instantiate an explicit `LLM` object from the `crewai` library and assign it to agents:
   ```python
   from crewai import LLM
   
   llm = LLM(
       model=os.getenv("OPENROUTER_MODEL"),
       base_url="https://openrouter.ai/api/v1",
       api_key=os.getenv("OPENROUTER_API_KEY"),
       temperature=0.7,
   )
   ```
3. **Telemetry Tracing:** To prevent bloated opentelemetry exception logging, ensure `OTEL_SDK_DISABLED=true` is set in the active process environment.

---

## ⚠️ 3. Memory & Embedding Constraints
- **Do Not Enable Default Memory:** CrewAI has memory capability enabled by setting `memory=True` on a Crew. However, enabling this tries to download and use OpenAI's default embedding model, which will immediately fail if `OPENAI_API_KEY` is not present in `.env`.
- **Embedder Configuration:** If memory features are requested, you *must* explicitly define a custom embedder provider (such as local Ollama, HuggingFace, or a compatible provider) instead of the default.

---

## 🧪 4. Testing & Validation Rules
- **Dry-run verification:** Before finishing any ticket or feature addition, run the entry point file (`.venv/bin/python main.py` or the specific module) to verify syntactic and runtime correctness.
- **Environment Isolation:** Do not write files that import dependencies not present in `req.txt`. If you add dependencies, update `req.txt` immediately.
