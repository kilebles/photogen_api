def to_camel(string: str) -> str:
    """snake_case -> camelCase"""
    parts = string.split("_")
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])