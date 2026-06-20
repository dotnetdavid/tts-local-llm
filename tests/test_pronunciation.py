from local_tts.pronunciation import PronunciationRule, apply_pronunciations, load_pronunciation_rules


def test_apply_pronunciations_replaces_ordered_phrases():
    rules = [
        PronunciationRule(source="Mara Vey", replacement="Mara Vay"),
        PronunciationRule(source="Rec Center", replacement="wreck center"),
    ]

    text = "Mara Vey went to the Rec Center. Mara Vey stayed there."

    assert apply_pronunciations(text, rules) == (
        "Mara Vay went to the wreck center. Mara Vay stayed there."
    )


def test_load_pronunciation_rules_accepts_dict_rows():
    rows = [
        {"source": "Mara Vey", "replacement": "Mara Vay"},
        {"source": "Calliope", "replacement": "Cal-eye-oh-pee"},
    ]

    rules = load_pronunciation_rules(rows)

    assert rules == [
        PronunciationRule(source="Mara Vey", replacement="Mara Vay"),
        PronunciationRule(source="Calliope", replacement="Cal-eye-oh-pee"),
    ]
