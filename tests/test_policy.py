from app.policy import evaluate_policy

def test_confidential_external_is_denied():
    result = evaluate_policy(
        audience = "external",
        data_classification = "confidential",
        pii_detected = False
    )

    assert result.decision == "DENY"
    assert "Confidential data cannot be processed" in result.reasons[0]
