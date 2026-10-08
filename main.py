import json
import random
from dataclasses import dataclass, asdict
from typing import Any, Dict

# Simulated LLM response generator (replace with actual API call)
def fake_llm(prompt: str) -> str:
    responses = [
        '{"name": "Alice", "age": 30, "email": "alice@example.com"}',
        '{"name": "Bob", "age": "25", "email": "bob@example.com"}',
        '{"name": "Charlie", "age": 35, "email": "invalid"}'
    ]
    return random.choice(responses)

# Define a type-safe schema using dataclass
@dataclass
class User:
    name: str
    age: int
    email: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        # Type validation and conversion
        try:
            name = str(data["name"])
            age = int(data["age"])
            email = str(data["email"])
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid data: {e}")

        # Simple email validation
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError(f"Invalid email format: {email}")

        return cls(name=name, age=age, email=email)

# Function to call LLM and parse with type safety
def safe_llm_call(prompt: str) -> User:
    raw = fake_llm(prompt)
    print(f"Raw LLM output: {raw}")
    try:
        data = json.loads(raw)
        user = User.from_dict(data)
        print(f"Parsed user: {user}")
        return user
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")
        # Fallback or error handling
        return User(name="unknown", age=0, email="unknown")

# Main demo loop
if __name__ == "__main__":
    prompt = "Generate a user profile"
    for _ in range(5):
        result = safe_llm_call(prompt)
        print(f"Result dict: {asdict(result)}\n")
