
import sys
import os

# Add backend directory to path so we can import main
sys.path.append(os.path.abspath("backend"))

from main import OptionEngine

def test_engine():
    # Payload matching the user request
    payload = {
        "model": "bjerksund93",
        "spot": 90,
        "strike": 100,
        "time": 1,
        "rate": 0.1,
        "dividend": 0.08,
        "volatility": 0.25,
        "type": "call"
    }
    
    print("--- Testing OptionEngine with McKean ---")
    try:
        engine = OptionEngine(payload)
        print(f"Model detected: {engine.model}")
        print(f"Inputs: S={engine.S}, K={engine.K}, r={engine.r}, q={engine.q_or_rf}, sigma={engine.sigma}")
        
        result = engine.calculate()
        print(f"Calculated Price: {result['price']}")
        print(f"Note: {result.get('note')}")
        print(f"Theta: {result['greeks'].get('theta')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_engine()
