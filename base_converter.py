DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_decimal(value: str, from_base: int) -> int:
    if not (2 <= from_base <= 36):
        raise ValueError(f"源进制必须在 2-36 之间，当前为 {from_base}")
    value = value.strip().lower()
    if not value:
        raise ValueError("输入值不能为空")
    negative = value.startswith("-")
    if negative:
        value = value[1:]
    if not value:
        raise ValueError("输入值不能只包含负号")
    result = 0
    for ch in value:
        digit = DIGITS.index(ch)
        if digit == -1 or digit >= from_base:
            raise ValueError(f"字符 '{ch}' 在 {from_base} 进制中无效")
        result = result * from_base + digit
    return -result if negative else result


def from_decimal(num: int, to_base: int) -> str:
    if not (2 <= to_base <= 36):
        raise ValueError(f"目标进制必须在 2-36 之间，当前为 {to_base}")
    if num == 0:
        return "0"
    negative = num < 0
    num = abs(num)
    chars = []
    while num > 0:
        chars.append(DIGITS[num % to_base])
        num //= to_base
    result = "".join(reversed(chars))
    return "-" + result if negative else result


def convert(value: str, from_base: int, to_base: int) -> str:
    decimal = to_decimal(value, from_base)
    return from_decimal(decimal, to_base)


if __name__ == "__main__":
    examples = [
        ("1010", 2, 10),
        ("ff", 16, 10),
        ("255", 10, 16),
        ("-42", 10, 2),
        ("1001", 2, 8),
        ("zz", 36, 10),
        ("35", 10, 36),
        ("0", 10, 2),
    ]
    for val, src, dst in examples:
        result = convert(val, src, dst)
        print(f"{val} ({src}) -> {result} ({dst})")
