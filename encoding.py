from fill_missing_values import fill_missing_values
from utils import format_output
import file_io

def encode(file_name, my_target):
    headers, data = file_io.read_dataset(file_name)

    data = fill_missing_values(data, my_target)

    str_to_encode = {}
    numeric_columns = []
    targets = {}

    def encode_value(value):
        if value not in str_to_encode:
            str_to_encode[value] = len(str_to_encode) + 1
        return str_to_encode[value]

    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    for header in headers:
        if all(is_numeric(item[header]) for item in data):
            numeric_columns.append(header)

    def encode_target(target):
        if target not in targets:
            targets[target] = len(targets) + 1
        return targets[target]

    for item in data:
        encode_target(item[my_target])

    encoded_data = []
    columns = [header for header in headers if header != my_target] + [
        f"Class_{i}" for i in range(1, len(targets) + 1)
    ]

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
            encoded_item.append(1 if i == target_code else 0)

        encoded_data.append(encoded_item)

    output = format_output(columns, encoded_data, column_width=15)

    return output
