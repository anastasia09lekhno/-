import yaml

def save_yaml(data, file_path):
    with open(file_path, "w") as f:
        yaml.dump(data, f)

def format_memory(memory):
    """
    ����������� ������ ������ � ������� ��� ��� ������ ��� ����������.
    """
    return [f"0x{val:08X}" for val in memory]

def parse_memory_range(range_str):
    """
    ������ �������� ������ �� ������ ������� "start-end".
    """
    try:
        start, end = map(int, range_str.split('-'))
        if start > end:
            raise ValueError("Start address must be less than or equal to end address.")
        return start, end
    except Exception as e:
        raise ValueError(f"Invalid memory range: {range_str}. Error: {e}")


