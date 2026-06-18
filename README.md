# Lumina Health — Clinically-Grounded AI Health Coach

[![Watch Health Coach Walkthrough](https://cdn.loom.com/sessions/thumbnails/b417dbfbe04f426da3fb769e9d872040-with-play.gif)](https://www.loom.com/share/b417dbfbe04f426da3fb769e9d872040)

Lumina Health is a thoughtful, secure, and clinically-grounded AI Health Coach and wellness companion built with the **Google Antigravity SDK** and powered by **Gemini 3.5 Flash**. 

It is designed to automatically ingest wearable metrics, provide fitness coaching backed by medical guidelines, support health checkups by ordering laboratory kits, and strictly maintain medical boundary safety protocols.

---

## 🚀 Key Features

* **Wearable HealthKit Integration**: Automatically reads simulated metrics (steps, sleep, HRV, heart rate, active calories) from local database.
* **Grounded Clinical Advice**: Evaluates recommendations against an authoritative database of clinical source guidelines (NIH, WHO, Harvard Health, American Academy of Sleep Medicine).
* **Safe Checkup Checkout**: Facilitates checkouts and checkout approvals for laboratory test kits (Vitamin D, Thyroid, General Wellness Panels).
* **Strict Medical Safety Gating**: Refuses to diagnose conditions or prescribe medications, referring patients to emergency services (e.g., 911) or clinical professionals when high-risk patterns are detected.
* **Premium User Interface**: Features a beautiful glassmorphic dark-mode web console with real-time streaming, collapsible reasoning thoughts, and dynamic activity charts.

---

## 📁 Repository Structure

```
lumina_health/
├── app.py                  # FastAPI Application and SSE streaming endpoints
├── agent.py                # Antigravity Agent definition & identity prompts
├── tools.py                # HealthKit metrics retriever, grounding rules, and checkout tools
├── health_metrics.json     # Mock daily HealthKit tracker database
├── pyproject.toml          # Declarative dependency configurations
├── start-lumina-health     # Background launch script on port 8001
├── stop-lumina-health      # Service teardown script
└── static/                 # Premium HTML UI & Vanilla CSS stylesheets
```

---

## 🛠️ Local Quickstart

### Prerequisites
Make sure you have `uv` installed (Python package manager). If not, install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Configure Secrets
Create a `.env` file in the workspace root or this directory with your Gemini API key:
```bash
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Start the Server
Run the launch helper to start the service on port `8001` in the background:
```bash
chmod +x start-lumina-health stop-lumina-health
./start-lumina-health
```

### 3. Open the Interface
Navigate to:
👉 **[http://localhost:8001](http://localhost:8001)**

### 4. Stop the Server
When you are done, clean up all background services with:
```bash
./stop-lumina-health
```

---

## 🔒 Security & Refusal Containment
This agent contains strict safety rules which are programmatically evaluated using `test_security.py` in the workspace root. It safely refuses to:
* **Prescribe Medications**: Rejects instruction bypasses and refuses to recommend drug dosages.
* **Diagnose Conditions**: Declines definitive clinical diagnostics and prompts immediate emergency action (`911`) for symptoms of severe chest pain or shortness of breath.
