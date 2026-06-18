import os
import json
from typing import Dict, List, Any
from google.antigravity import ToolContext

# Database paths
METRICS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "health_metrics.json"))

# Mock authoritative clinical guidelines
GUIDELINES_DB = {
    "sleep": {
        "recommendation": "Adults should aim for 7-9 hours of sleep per night to support cognitive function, cardiovascular health, and metabolic regulation.",
        "source": "American Academy of Sleep Medicine (AASM) & Sleep Research Society (SRS), 2015"
    },
    "steps": {
        "recommendation": "Aiming for 7,000 to 10,000 steps per day is associated with significant reductions in all-cause mortality, cardiovascular events, and risk of Type 2 Diabetes.",
        "source": "JAMA Network Open / National Institutes of Health (NIH), 2021"
    },
    "hrv": {
        "recommendation": "Heart Rate Variability (HRV) is a marker of autonomic nervous system balance. Higher HRV generally indicates good cardiovascular fitness and stress resilience. Sudden drops can indicate fatigue, overtraining, or acute physiological stress.",
        "source": "Harvard Health Publishing / American Heart Association, 2020"
    },
    "cardio": {
        "recommendation": "Adults should engage in at least 150 minutes of moderate-intensity or 75 minutes of vigorous-intensity aerobic physical activity per week, along with muscle-strengthening exercises.",
        "source": "World Health Organization (WHO) Guidelines on Physical Activity, 2020"
    }
}

ORDERED_KITS = []

def get_health_metrics() -> str:
    """Retrieves the user's latest daily health metrics (steps, sleep, HRV, RHR, exercise) from their Apple Watch/HealthKit.
    """
    try:
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, 'r') as f:
                data = json.load(f)
            return json.dumps({"status": "success", "metrics": data}, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "message": "Metrics file not found. Returning empty database."
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def query_guidelines(topic: str) -> str:
    """Answers health and fitness questions by retrieving authoritative clinical guidelines with clear citations.

    Args:
        topic: The topic to look up (e.g. "sleep", "steps", "hrv", "cardio").
    """
    topic_lower = topic.lower().strip()
    match = None
    for key in GUIDELINES_DB:
        if key in topic_lower or topic_lower in key:
            match = key
            break
            
    if match:
        return json.dumps({
            "status": "success",
            "topic": match.title(),
            "recommendation": GUIDELINES_DB[match]["recommendation"],
            "source_citation": GUIDELINES_DB[match]["source"]
        }, indent=2)
    else:
        return json.dumps({
            "status": "partial_success",
            "topic": topic,
            "recommendation": "Consult a primary care physician or certified fitness coach for tailored recommendations on this specific topic.",
            "source_citation": "General Medical Best Practices"
        }, indent=2)

def order_test_kit(kit_type: str, ctx: ToolContext) -> str:
    """Orders a verified, approved health test kit (e.g., Vitamin D check, Thyroid panel, Wellness panel).
    This is an active checkout process. Always verify with the user before executing.

    Args:
        kit_type: The type of test kit to order (e.g. "Vitamin D", "Thyroid Panel", "General Wellness").
    """
    # Load orders state
    orders = ctx.get_state("orders", [])
    
    order_record = {
        "order_id": f"KIT-{len(orders) + 5000}",
        "kit_type": kit_type,
        "status": "ORDER SHIPPED",
        "provider": "Verified Health Labs Inc."
    }
    
    orders.append(order_record)
    ctx.set_state("orders", orders)
    
    # Track globally for FastAPI
    ORDERED_KITS.append(order_record)
    
    return json.dumps({
        "status": "success",
        "message": f"Successfully ordered {kit_type} test kit!",
        "order_details": order_record
    }, indent=2)
