def alt_n_generator(n: int) -> str:
    if n < 1:
        raise ValueError("n must be >= 1")

    if n==2:
        return "#p_1^#(~p_1|p_2)"
    
    parts = []

    # First conjunct
    parts.append("#p_1")

    # Remaining conjuncts
    for k in range(1, n):
        negs = "|".join(f"~p_{i}" for i in range(1, k + 1))
        parts.append(f"#({negs}|p_{k+1})")

    return "^".join(parts)
