import random

MODELS = {
    "model_v1": {"accuracy": 0.80},
    "model_v2": {"accuracy": 0.90}
}


def run_model(model_name: str, data: dict):
    age = data.get("age", 50)
    smoking = data.get("smoking", 0)

    score = (0.3 * age + 0.7 * smoking) / 100

    if score > 0.5:
        risk = "High Risk"
    else:
        risk = "Low Risk"

    return {
        "model": model_name,
        "prediction": risk,
        "confidence": round(score + random.uniform(0, 0.1), 2)
    }


def compare_models(data: dict):
    results = []

    for model_name in MODELS:
        result = run_model(model_name, data)
        results.append(result)

    best = max(results, key=lambda x: x["confidence"])

    return {
        "all_results": results,
        "best_model": best
    }