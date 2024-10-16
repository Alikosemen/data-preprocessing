def get_mode(values):
    value_counts = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1
    return max(value_counts, key=value_counts.get)
