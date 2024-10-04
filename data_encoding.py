# For GUI
def get_headers(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        headers = first_line.split()
    return headers


def process_file(file_path, my_target):
    text = open(file_path, 'r')

    lines = text.readlines()
    headers = lines[0].strip().split()

    data = []
    for line in lines[1:]:
        values = line.strip().split()
        if len(values) != len(headers):
            continue

        entry = {}
        for i, header in enumerate(headers):
            entry[header] = values[i]
        data.append(entry)

    totals = {}
    counts = {}
    for row in data:
        for key, value in row.items():
            if value.isdigit():
                if key not in totals:
                    totals[key] = 0
                    counts[key] = 0
                totals[key] += int(value)
                counts[key] += 1

    mean = {key: totals[key] / counts[key] for key in totals}

    for row in data:
        for key, value in row.items():
            if value == "?" and key in mean:
                row[key] = round(mean[key])

    str_to_encode = {}

    def encode_value(value):
        if value not in str_to_encode:
            str_to_encode[value] = len(str_to_encode) + 1
        return str_to_encode[value]

    numeric_columns = []

    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    for header in headers:
        if all(is_numeric(item[header]) for item in data):
            numeric_columns.append(header)

    targets = {}

    def encode_target(target):
        if target not in targets:
            targets[target] = len(targets) + 1
        return targets[target]

    for item in data:
        encode_target(item[my_target])

    encoded_data = []
    columns = [header for header in headers if header != my_target] + \
              [f"Class_{i}" for i in range(1, len(targets) + 1)]

    encoded_columns = {header: [] for header in headers}
    for header in headers:
        if header == my_target:
            continue

        for item in data:
            if header in numeric_columns:
                try:
                    encoded_columns[header].append(int(item[header]))
                except ValueError:
                    encoded_columns[header].append(float(item[header]))
            else:
                encoded_columns[header].append(encode_value(item[header]))

    for item in data:
        encoded_item = []

        for header in headers:
            if header == my_target:
                continue
            encoded_item.append(encoded_columns[header][data.index(item)])

        target_code = encode_target(item[my_target])
        for i in range(1, len(targets) + 1):
            if i == target_code:
                encoded_item.append(1)
            else:
                encoded_item.append(0)

        encoded_data.append(encoded_item)

    column_width = 15
    header_line = " | ".join([f"{col:>{column_width}}" for col in columns])
    output = header_line + "\n" + "-" * len(header_line) + "\n"

    for row in encoded_data:
        row_line = " | ".join([f"{str(val):>{column_width}}" for val in row])
        output += row_line + "\n"

    return output
