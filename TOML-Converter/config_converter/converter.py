def convert_to_custom_language(tree):
    if isinstance(tree, dict):  # ���� ��� �������
        out = "("
        for k, v in tree.items():
            out += f" {k} {convert_to_custom_language(v)}"
        out += " )"
        return out.strip()
    elif isinstance(tree, list):  # ���� ��� ������
        out = "("
        for i in tree:
            out += f" {convert_to_custom_language(i)}"
        out += " )"
        return out.strip()
    elif isinstance(tree, str):  # ���� ��� ������
        return f"[[{tree}]]"
    elif isinstance(tree, (int, float)):  # ���� ��� �����
        return str(tree)
    else:
        raise ValueError(f"Unsupported data type: {type(tree)}")

