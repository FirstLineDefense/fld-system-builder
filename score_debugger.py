def print_score_breakdown(result):
    print()
    print("SCORE BREAKDOWN")
    print("----------------")

    print(
        "OVERALL:",
        result.get("overall_score")
    )

    print()

    categories = result.get(
        "categories",
        {}
    )

    weights = result.get(
        "weights",
        {}
    )

    total_contribution = 0

    for name, value in categories.items():
        score = value[0]
        note = value[1]

        weight = weights.get(name, 0)

        contribution = round(
            score * weight,
            2
        )

        total_contribution += contribution

        print(
            f"{name}"
            f" | score={score}"
            f" | weight={weight}"
            f" | contribution={contribution}"
        )

        print(
            f"notes: {note}"
        )

        print()

    print("----------------")
    print(
        "TOTAL CONTRIBUTION:",
        round(total_contribution, 2)
    )
