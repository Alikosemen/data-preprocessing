def format_output(columns, encoded_data, column_width=15):
    header_line = " | ".join([f"{col:>{column_width}}" for col in columns])
    output = header_line + "\n" + "-" * len(header_line) + "\n"

    for row in encoded_data:
        row_line = " | ".join([f"{str(val):>{column_width}}" for val in row])
        output += row_line + "\n"

    return output
