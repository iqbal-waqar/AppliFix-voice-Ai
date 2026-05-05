from typing import Dict, Any

APPLIANCE_DIAGNOSTICS: Dict[str, Dict[str, Any]] = {
    "washer": {
        "common_issues": ["not spinning", "leaking", "loud noise", "won't start", "error code"],
        "quick_checks": [
            "Check if the washer lid/door is fully closed and latched.",
            "Verify the water supply valves behind the washer are fully open.",
            "Inspect the drain hose for kinks or blockages.",
            "Check if the load is unbalanced — redistribute clothes evenly.",
            "Look for any error codes on the display panel.",
        ],
        "severity_keywords": {
            "urgent": ["smoke", "sparks", "burning smell", "flooding", "no power"],
            "moderate": ["loud bang", "error code", "won't drain", "won't spin"],
            "minor": ["noise", "vibration", "slow fill"],
        },
    },
    "dryer": {
        "common_issues": ["not heating", "takes too long", "loud noise", "won't start", "overheating"],
        "quick_checks": [
            "Clean the lint filter — a clogged filter reduces airflow significantly.",
            "Check the exhaust vent outside your home is not blocked.",
            "Make sure the dryer is plugged in and the circuit breaker hasn't tripped.",
            "Verify the door switch clicks when you close the door.",
            "Check if there's a thermal fuse that may have blown.",
        ],
        "severity_keywords": {
            "urgent": ["smoke", "burning smell", "fire", "sparks"],
            "moderate": ["not heating", "takes too long", "error code"],
            "minor": ["noise", "vibration", "takes slightly longer"],
        },
    },
    "refrigerator": {
        "common_issues": ["not cooling", "ice maker broken", "leaking water", "loud noise", "freezer frost"],
        "quick_checks": [
            "Check the temperature settings — fridge should be 37°F, freezer 0°F.",
            "Clean the condenser coils at the bottom or back of the fridge.",
            "Ensure the door seals are tight — place a dollar bill in the door, if it slides out easily the seal needs replacing.",
            "Check that the fridge is not overpacked, blocking air circulation.",
            "Verify the water line connection if the ice maker is not working.",
        ],
        "severity_keywords": {
            "urgent": ["sparks", "burning smell", "completely not cooling", "food spoiling"],
            "moderate": ["not cooling well", "ice maker broken", "leaking"],
            "minor": ["noise", "frost buildup", "slight temperature issue"],
        },
    },
    "dishwasher": {
        "common_issues": ["not cleaning well", "leaking", "won't drain", "loud noise", "error code"],
        "quick_checks": [
            "Clean the filter at the bottom of the dishwasher.",
            "Check the spray arms for clogged holes — clear with a toothpick.",
            "Verify you are using the correct dishwasher detergent.",
            "Inspect the door gasket for cracks or food debris.",
            "Check the drain hose for kinks.",
        ],
        "severity_keywords": {
            "urgent": ["flooding", "sparks", "burning smell"],
            "moderate": ["won't drain", "not cleaning", "leaking"],
            "minor": ["noise", "spots on dishes"],
        },
    },
    "oven": {
        "common_issues": ["not heating", "uneven cooking", "error code", "self-clean issue", "door not closing"],
        "quick_checks": [
            "Check if the oven is in self-clean mode, which locks the door.",
            "Test a different burner if one is not working (gas) or check the element for damage (electric).",
            "Verify the oven temperature using an oven thermometer.",
            "Check the oven door gasket for damage.",
            "Look for any error codes on the display.",
        ],
        "severity_keywords": {
            "urgent": ["gas smell", "sparks", "fire", "smoke"],
            "moderate": ["not heating", "error code", "door won't open"],
            "minor": ["uneven cooking", "slight temperature issue"],
        },
    },
    "hvac": {
        "common_issues": ["not cooling", "not heating", "unusual noise", "poor airflow", "error code"],
        "quick_checks": [
            "Replace or check the air filter — a dirty filter is the #1 cause of HVAC issues.",
            "Check the thermostat settings and batteries.",
            "Verify all vents are open and not blocked by furniture.",
            "Check the circuit breaker for the HVAC system.",
            "Inspect the outdoor unit for debris or ice buildup.",
        ],
        "severity_keywords": {
            "urgent": ["gas smell", "burning smell", "smoke", "sparks", "carbon monoxide"],
            "moderate": ["not cooling", "not heating", "unusual noise"],
            "minor": ["poor airflow", "slight temperature issue"],
        },
    },
}

class TroubleshootingInteractor:
    def get_troubleshooting_steps(self, appliance_type: str, symptoms: str) -> Dict[str, Any]:
        """
        Given an appliance type and symptom description, return diagnostic guidance.
        """
        appliance_lower = appliance_type.lower().strip()

        # Fuzzy match appliance
        matched_key = None
        for key in APPLIANCE_DIAGNOSTICS:
            if key in appliance_lower or appliance_lower in key:
                matched_key = key
                break

        if not matched_key:
            return {
                "appliance": appliance_type,
                "severity": "unknown",
                "steps": [
                    "Please describe the problem in more detail.",
                    "Note any error codes, unusual sounds, or smells.",
                    "Check if the appliance has power and is properly plugged in.",
                ],
                "recommendation": "A technician visit is recommended for diagnosis.",
            }

        diag = APPLIANCE_DIAGNOSTICS[matched_key]
        symptoms_lower = symptoms.lower()

        # Determine severity
        severity = "minor"
        for level in ["urgent", "moderate", "minor"]:
            for keyword in diag["severity_keywords"][level]:
                if keyword in symptoms_lower:
                    severity = level
                    break
            if severity == level and level in ["urgent", "moderate"]:
                break

        steps = diag["quick_checks"]

        if severity == "urgent":
            recommendation = (
                "⚠️ This sounds like it could be a safety issue. "
                "Please stop using the appliance immediately and schedule an urgent technician visit."
            )
        elif severity == "moderate":
            recommendation = (
                "This issue requires professional attention. "
                "Try the quick checks above, but scheduling a technician visit is strongly recommended."
            )
        else:
            recommendation = (
                "Try the quick checks above. "
                "If the problem persists after these steps, a technician can do a deeper diagnosis."
            )

        return {
            "appliance": matched_key,
            "severity": severity,
            "steps": steps,
            "recommendation": recommendation,
        }
