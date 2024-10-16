import os

DATASET_PATH = "/home/aliksmn/PycharmProjects/machine_learning/datasets"


def load_datasets():
    try:
        return [f for f in os.listdir(DATASET_PATH) if f.endswith(".txt")]
    except Exception as e:
        raise Exception(f"Error loading datasets: {str(e)}")


def read_dataset(file_name):
    file_path = os.path.join(DATASET_PATH, file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        headers = lines[0].strip().split()

        data = []
        for line in lines[1:]:
            values = line.strip().split()
            if len(values) == len(headers):
                entry = {header: value for header, value in zip(headers, values)}
                data.append(entry)

        return headers, data
