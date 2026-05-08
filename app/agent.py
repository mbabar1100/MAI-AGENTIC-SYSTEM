from typing import Dict, Any, List

# ------------------------------------------------
# MODEL 1 (AGE-FOCUSED)
# ------------------------------------------------
def model_v1(features: Dict[str, float]) -> Dict[str, Any]:

    age = features.get("age", 0)
    smoking = features.get("smoking", 0)

    # weighted score
    score = 0.6 * (age / 100) + 0.4 * (smoking / 10)

    prediction = "High Risk" if score >= 0.5 else "Low Risk"

    return {
        "model": "model_v1",
        "prediction": prediction,
        "confidence": round(score, 2)
    }


# ------------------------------------------------
# MODEL 2 (SMOKING-FOCUSED)
# ------------------------------------------------
def model_v2(features: Dict[str, float]) -> Dict[str, Any]:

    age = features.get("age", 0)
    smoking = features.get("smoking", 0)

    # weighted score
    score = 0.4 * (age / 100) + 0.6 * (smoking / 10)

    prediction = "High Risk" if score >= 0.5 else "Low Risk"

    return {
        "model": "model_v2",
        "prediction": prediction,
        "confidence": round(score, 2)
    }


# ------------------------------------------------
# COMPARE MODELS
# ------------------------------------------------
def compare_models(features: Dict[str, float]) -> Dict[str, Any]:

    results: List[Dict[str, Any]] = [
        model_v1(features),
        model_v2(features)
    ]

    # select best model
    best = max(results, key=lambda x: x["confidence"])

    explanation = (
        f"{best['model']} selected because it has the highest "
        f"confidence score ({best['confidence']}). "
        f"Age contribution: {round(features.get('age', 0)/100, 2)}, "
        f"Smoking contribution: {round(features.get('smoking', 0)/10, 2)}."
    )

    best_model = dict(best)
    best_model["explanation"] = explanation

    return {
        "type": "comparison",
        "results": results,
        "best_model": best_model
    }


# ------------------------------------------------
# SINGLE ANALYSIS
# ------------------------------------------------
def analyze_single(features: Dict[str, float]) -> Dict[str, Any]:

    result = model_v1(features)

    explanation = (
        "Prediction based on weighted contribution of age and smoking. "
        f"Age={features.get('age')}, "
        f"Smoking={features.get('smoking')}."
    )

    result["explanation"] = explanation

    return result


# ------------------------------------------------
# MAIN HANDLER
# ------------------------------------------------
def handle_query(payload: Dict[str, Any]) -> Dict[str, Any]:

    query = payload.get("query", "").lower().strip()

    features = {
        "age": payload.get("age", 0),
        "smoking": payload.get("smoking", 0)
    }

    # --------------------------------------------
    # INVALID QUERY
    # --------------------------------------------
    if "compare" not in query and "analysis" not in query:

        return {
            "type": "message",
            "message": (
                "Please enter a valid command:\n\n"
                "• compare models\n"
                "• data analysis"
            )
        }

    # --------------------------------------------
    # COMPARE MODELS
    # --------------------------------------------
    if "compare" in query:

        return compare_models(features)

    # --------------------------------------------
    # SINGLE ANALYSIS
    # --------------------------------------------
    return analyze_single(features)