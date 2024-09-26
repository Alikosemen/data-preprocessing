text = open('sample_dataset.txt', 'r')

lines = text.readlines()

headers = lines[0].strip().split()

my_target = "Marka"

data = []
for line in lines[1:]:
    values = line.strip().split()
    if len(values) != len(headers):
        continue

    entry = {}
    for i, header in enumerate(headers):
        entry[header] = values[i]
    data.append(entry)
    


str_to_encode = {}


def encode_value(column_name, value):
    if column_name not in str_to_encode:
        str_to_encode[column_name] = {}
    if value not in str_to_encode[column_name]:
        str_to_encode[column_name][value] = len(str_to_encode[column_name]) + 1
    return str_to_encode[column_name][value]



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



columns = [header for header in headers if header != my_target] + [f"Class_{i}" for i in range(1, len(targets) + 1)]


for item in data:
    encoded_item = []

    for header in headers:
        if header == my_target:
            continue
        elif header in numeric_columns:
            try:
                encoded_item.append(int(item[header]))
            except ValueError:
                encoded_item.append(float(item[header]))
        else:
            encoded_item.append(encode_value(header, item[header]))


    target_code = encode_target(item[my_target])
    for i in range(1, len(targets) + 1):
        if i == target_code:
            encoded_item.append(1)
        else:
            encoded_item.append(0)

    encoded_data.append(encoded_item)



column_width = 15


header_line = " | ".join([f"{col:>{column_width}}" for col in columns])
print(header_line)
print("-" * len(header_line))


for row in encoded_data:
    row_line = " | ".join([f"{str(val):>{column_width}}" for val in row])
    print(row_line)
