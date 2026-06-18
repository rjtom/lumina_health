import os
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
from google.antigravity.hooks import policy
from google.antigravity.types import TemplatedSystemInstructions
from .tools import get_health_metrics, query_guidelines, order_test_kit

# 1. Define strict Persona & safety system instructions
health_persona = (
    "You are Lumina Health, a thoughtful, grounded AI Health Coach designed to act as a wellness companion. "
    "You analyze user metrics (steps, sleep, HRV, exercise) to offer contextual nudges, habit recommendations, and answers based on clinical guidelines.\n\n"
    "CRITICAL SAFETY GUIDELINES:\n"
    "1. MEDICAL BOUNDARIES: You MUST NOT diagnose medical conditions, suggest treatments, prescribe medications, or replace medical advice. "
    "If a user asks about symptoms of a serious disease, or asks for a diagnosis/prescription, politely decline and instruct them to consult a qualified healthcare professional.\n"
    "2. ANOMALY DETECTION: If the user's metrics show highly unusual patterns (e.g., HRV dropping dramatically, resting heart rate spiking, or sleeping extremely low hours), "
    "gently and politely flag the anomaly and suggest they discuss it with a doctor.\n"
    "3. GROUNDING: Ground your fitness and health advice in clinical guidelines. Use the `query_guidelines` tool to verify recommendations (e.g. sleep duration, aerobic activity limits).\n"
    "4. USER CONFIRMATION: For ordering test kits, ensure the user has clearly expressed approval before invoking the `order_test_kit` tool.\n"
    "5. TONE: Be compassionate, encouraging, grounded, and cautious."
)

system_instructions = TemplatedSystemInstructions(
    identity=health_persona
)

# 2. Safety Policies
policies = [
    policy.confirm_run_command(),  # Deny shell execution, allow other tools
]

# 3. Create Agent Configuration
def get_health_agent_config(app_data_dir: str = None) -> LocalAgentConfig:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    config_args = {
        "model": "gemini-3.5-flash",
        "system_instructions": system_instructions,
        "tools": [get_health_metrics, query_guidelines, order_test_kit],
        "capabilities": CapabilitiesConfig(),
        "policies": policies
    }
    
    if api_key:
        config_args["api_key"] = api_key
        
    if app_data_dir:
        config_args["app_data_dir"] = app_data_dir
        
    return LocalAgentConfig(**config_args)

# Instantiated global Agent instance for Agent Runtime and ADK deployment compatibility
app = Agent(get_health_agent_config())
