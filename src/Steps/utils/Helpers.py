def is_emoji(char: str) -> bool:
    
    code = ord(char)

    return (
        0x1F300 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
    )