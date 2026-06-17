DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_decimal(value: str, from_base: int) -> int:
    if not (2 <= from_base <= 36):
        raise ValueError(f"源进制必须在 2-36 之间，当前为 {from_base}")
    value = value.strip().lower()
    if not value:
        raise ValueError("输入值不能为空")
    negative = value.startswith("-")
    positive = value.startswith("+")
    if negative or positive:
        value = value[1:]
    if not value:
        raise ValueError("输入值不能只包含符号")
    result = 0
    for ch in value:
        digit = DIGITS.find(ch)
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
        ("-ff", 16, 10),
        ("-101010", 2, 10),
        ("-255", 10, 16),
        ("-1295", 10, 36),
        ("+42", 10, 2),
        ("-0", 10, 16),
        ("  -42  ", 10, 8),
        ("-1a", 16, 2),
    ]
    print("=== 进制转换测试 ===")
    for val, src, dst in examples:
        result = convert(val, src, dst)
        decimal = to_decimal(val, src)
        roundtrip = from_decimal(decimal, src)
        print(f"{val!r:>12} ({src:>2}) -> {result!r:>14} ({dst:>2})  |  roundtrip: {roundtrip!r}")

    print("\n=== 异常测试 ===")
    error_cases = [
        ("102", 2, "二进制不允许字符'2'"),
        ("", 10, "空字符串"),
        ("-", 10, "只有负号"),
        ("+", 10, "只有正号"),
        ("xyz", 10, "十进制不允许字母"),
        ("10", 1, "无效源进制"),
        ("10", 37, "无效源进制"),
        ("a", 10, 38, "无效目标进制"),
    ]
    for case in error_cases:
        try:
            if len(case) == 3:
                val, src, desc = case
                convert(val, src, 10)
            else:
                val, src, dst, desc = case
                convert(val, src, dst)
            print(f"FAIL [{desc}]: 未抛出异常")
        except ValueError as e:
            print(f"OK   [{desc}]: {e}")
        except Exception as e:
            print(f"FAIL [{desc}]: 意外异常 {type(e).__name__}: {e}")
