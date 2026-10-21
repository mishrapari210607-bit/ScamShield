"""Simple, explainable warning-sign checks for suspicious messages."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Signal:
    description: str
    weight: int


_SIGNALS: tuple[tuple[re.Pattern[str], str, int], ...] = (
    (re.compile(r"\b(urgent|immediately|act now|right away|expires today)\b", re.I),
     "Uses urgent or high-pressure language", 20),
    (re.compile(r"\b(password| passcode|one[- ]time code|verification code|otp)\b", re.I),
     "Requests a password or verification code", 35),
    (re.compile(r"\b(gift card|crypto(currency)?|bitcoin|wire transfer)\b", re.I),
     "Mentions a payment method commonly used in scams", 25),
    (re.compile(r"\b(prize|winner|claim your reward|you have been selected)\b", re.I),
     "Promises a prize or unexpected reward", 20),
    (re.compile(r"https?://|www\.", re.I),
     "Contains a web link; verify the destination before opening it", 10),
    (re.compile(r"\b(bank account|credit card|social security|personal information)\b", re.I),
     "Requests sensitive personal or financial information", 25),
)


def analyze_message(message: str) -> dict[str, object]:
    """Return a heuristic risk score, label, and matching warning signs."""
    signals = [
        Signal(description, weight)
        for pattern, description, weight in _SIGNALS
        if pattern.search(message)
    ]
    score = min(100, sum(signal.weight for signal in signals))
    if score >= 60:
        label = "high"
    elif score >= 25:
        label = "suspicious"
    else:
        label = "low"

    return {
        "score": score,
        "risk": label,
        "signals": [signal.description for signal in signals],
        "disclaimer": "This automated check can be wrong. Verify messages independently.",
    }
