def convert_to_custom_language(tree):
    if isinstance(tree, dict):  # Åñëè ýòî ñëîâàðü
        out = "'("
        for k, v in tree.items():
            out += f" {k} {convert_to_custom_language(v)}"
        out += " )"
        return out.strip()
    elif isinstance(tree, list):  # Åñëè ýòî ñïèñîê
        out = "'("
        for i in tree:
            out += f" {convert_to_custom_language(i)}"
        out += " )"
        return out.strip()
    elif isinstance(tree, str):  # Åñëè ýòî ñòðîêà
        return f"[[{tree}]]"
    elif isinstance(tree, (int, float)):  # Åñëè ýòî ÷èñëî
        return str(tree)
    else:
        raise ValueError(f"Unsupported data type: {type(tree)}")

