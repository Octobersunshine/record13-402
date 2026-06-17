DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _parse_digit(ch: str, base: int) -> int:
    digit = DIGITS.find(ch)
    if digit == -1 or digit >= base:
        raise ValueError(f"字符 '{ch}' 在 {base} 进制中无效")
    return digit


def to_decimal(value: str, from_base: int) -> float:
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
    parts = value.split(".")
    if len(parts) > 2:
        raise ValueError("输入值包含多个小数点")
    int_part, frac_part = parts[0], parts[1] if len(parts) == 2 else ""
    if not int_part and not frac_part:
        raise ValueError("输入值不能只包含小数点")
    int_result = 0
    for ch in int_part:
        int_result = int_result * from_base + _parse_digit(ch, from_base)
    frac_result = 0.0
    if frac_part:
        power = 1.0 / float(from_base)
        for ch in frac_part:
            frac_result += _parse_digit(ch, from_base) * power
            power /= float(from_base)
    total = float(int_result) + frac_result
    return -total if negative else total


def from_decimal(num: float, to_base: int, precision: int = 10) -> str:
    if not (2 <= to_base <= 36):
        raise ValueError(f"目标进制必须在 2-36 之间，当前为 {to_base}")
    if precision < 0:
        raise ValueError(f"精度不能为负数，当前为 {precision}")
    eps = 1e-12
    if abs(num) < eps:
        return "0"
    negative = num < 0
    num = abs(num)
    int_part = int(round(num, 10))
    frac_part = num - float(int_part)
    if abs(frac_part) < eps:
        frac_part = 0.0
    if int_part == 0:
        int_str = "0"
    else:
        chars = []
        n = int_part
        while n > 0:
            chars.append(DIGITS[n % to_base])
            n //= to_base
        int_str = "".join(reversed(chars))
    if frac_part == 0 or precision == 0:
        result = int_str
    else:
        frac_chars = []
        remaining = frac_part
        for _ in range(precision):
            remaining *= to_base
            digit = int(round(remaining, 10))
            if digit >= to_base:
                digit = to_base - 1
            frac_chars.append(DIGITS[digit])
            remaining -= digit
            if abs(remaining) < eps or abs(remaining - 1.0) < eps:
                break
        frac_str = "".join(frac_chars).rstrip("0")
        result = int_str + ("." + frac_str if frac_str else "")
    return "-" + result if negative else result


def convert(value: str, from_base: int, to_base: int, precision: int = 10) -> str:
    decimal = to_decimal(value, from_base)
    return from_decimal(decimal, to_base, precision=precision)


if __name__ == "__main__":
    examples = [
        ("1010", 2, 10, None),
        ("ff", 16, 10, None),
        ("255", 10, 16, None),
        ("-42", 10, 2, None),
        ("1001", 2, 8, None),
        ("zz", 36, 10, None),
        ("35", 10, 36, None),
        ("0", 10, 2, None),
        ("-ff", 16, 10, None),
        ("-101010", 2, 10, None),
        ("-255", 10, 16, None),
        ("-1295", 10, 36, None),
        ("+42", 10, 2, None),
        ("-0", 10, 16, None),
        ("  -42  ", 10, 8, None),
        ("-1a", 16, 2, None),
        ("0.5", 10, 2, 4),
        ("0.1", 10, 2, 8),
        ("0.75", 10, 2, None),
        ("10.101", 2, 10, None),
        ("-3.14", 10, 2, 8),
        ("ff.8", 16, 10, None),
        ("0.a", 16, 10, None),
        ("1.5", 10, 16, 4),
        ("77.77", 8, 10, 4),
        (".5", 10, 2, 4),
        ("5.", 10, 2, None),
        ("-0.1", 10, 8, 6),
    ]
    print("=== 进制转换测试 ===")
    for val, src, dst, prec in examples:
        kwargs = {} if prec is None else {"precision": prec}
        result = convert(val, src, dst, **kwargs)
        print(f"{val!r:>14} ({src:>2}) -> {result!r:>20} ({dst:>2})")

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
        ("1.2.3", 10, "多个小数点"),
        (".", 10, "只有小数点"),
        ("0.5", 10, 2, -1, "负精度"),
    ]
    for case in error_cases:
        try:
            if len(case) == 3:
                val, src, desc = case
                convert(val, src, 10)
            elif len(case) == 4:
                val, src, dst, desc = case
                convert(val, src, dst)
            else:
                val, src, dst, prec, desc = case
                convert(val, src, dst, precision=prec)
            print(f"FAIL [{desc}]: 未抛出异常")
        except ValueError as e:
            print(f"OK   [{desc}]: {e}")
        except Exception as e:
            print(f"FAIL [{desc}]: 意外异常 {type(e).__name__}: {e}")
