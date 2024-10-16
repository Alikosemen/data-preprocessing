import get_mode


def fill_missing_values(data, target_variable):
    data = [row for row in data if row[target_variable] != "?"]

    class_data = {}
    class_stats = {}

    for row in data:
        class_value = row[target_variable]
        if class_value not in class_data:
            class_data[class_value] = []
        class_data[class_value].append(row)

    classes_to_remove = []
    for class_value, rows in class_data.items():
        if len(rows) == 1:
            row = rows[0]
            if any(value == "?" for key, value in row.items() if key != target_variable):
                classes_to_remove.append(class_value)

    for class_value in classes_to_remove:
        del class_data[class_value]

    data = [row for rows in class_data.values() for row in rows]

    for class_value, rows in class_data.items():
        numeric_totals = {}
        numeric_counts = {}
        categorical_values = {}

        for row in rows:
            for key, value in row.items():
                if key != target_variable and value != "?":
                    if value.isdigit():
                        if key not in numeric_totals:
                            numeric_totals[key] = 0
                            numeric_counts[key] = 0
                        numeric_totals[key] += int(value)
                        numeric_counts[key] += 1
                    else:
                        if key not in categorical_values:
                            categorical_values[key] = []
                        categorical_values[key].append(value)

        class_stats[class_value] = {
            'numeric': {key: numeric_totals[key] / numeric_counts[key] for key in numeric_totals},
            'categorical': {key: get_mode.get_mode(values) for key, values in categorical_values.items() if values}
        }

    for row in data:
        class_value = row[target_variable]
        for key, value in row.items():
            if value == "?":
                if key in class_stats[class_value]['numeric']:
                    row[key] = str(round(class_stats[class_value]['numeric'][key]))
                elif key in class_stats[class_value]['categorical']:
                    row[key] = class_stats[class_value]['categorical'][key]

    return data