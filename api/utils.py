def convert_numeric_string_to_float(numeric_string: str):
    return float(numeric_string.strip().replace(".", "").replace(",", "").replace("-","0").replace("nd","0"))
