def calcul(inpstr):
    tokens = []
    i = 0
    while i < len(inpstr):
        elem = inpstr[i]
        if elem == " ":
            i += 1
        elif inpstr[i:i + 2] == "<=":
            tokens.append("<=")
            i += 2
        elif inpstr[i:i + 5] == "floor":
            tokens.append("floor")
            i += 5
        elif elem in ".0123456789":
            number = ""
            while i < len(inpstr) and (inpstr[i] in ".0123456789"):
                number += inpstr[i]
                i += 1
            if number == "." or number.count(".") > 1:
                print("ERROR: неправильная запись")
                return None
            tokens.append(float(number))
        elif elem in "+-*/()":
            tokens.append(elem)
            i += 1
        else:
            print("ERROR: неизвестный символ")
            return None
        if len(tokens) == 0:
            print("ERROR: пустое выражение")
            return None

    pos = 0
    def num():
        nonlocal pos
        if pos < len(tokens) and tokens[pos] == "+":
            pos += 1
            return num()
        if pos < len(tokens) and tokens[pos] == "-":
            pos += 1
            result = num()
            if result is None:
                return None
            return -result
        if pos < len(tokens) and tokens[pos] == "floor":
            pos += 1
            if pos < len(tokens) and tokens[pos] == "(":
                pos += 1
                result = value()
                if result is None:
                    return None
                if pos < len(tokens) and tokens[pos] == ")":
                    pos += 1
                else:
                    print("ERROR: у floor нет закрывающей скобки")
                    return None
                whole = int(result)
                if result < whole:
                    whole -= 1
                return whole
            print("ERROR: у floor нет открывающей скобки")
            return None
        if pos < len(tokens) and tokens[pos] == "(":
            pos += 1
            result = value()
            if result is None:
                return None
            if pos < len(tokens) and tokens[pos] == ")":
                pos += 1
                return result
            print("ERROR: нет закрывающей скобки")
            return None
        if pos < len(tokens) and isinstance(tokens[pos], float):
            result = tokens[pos]
            pos += 1
            return result
        print("ERROR: ожидалось число")
        return None

    def mult():
        nonlocal pos
        result = num()

        if result is None:
            return None
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            oper = tokens[pos]
            pos += 1
            right = num()

            if right is None:
                return None
            if oper == "*":
                result *= right
            else:
                if right == 0:
                    print("ERROR: деление на ноль")
                    return None
                result /= right
        return result

    def addit():
        nonlocal pos
        result = mult()

        if result is None:
            return None

        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            right = mult()

            if right is None:
                return None
            if op == "+":
                result += right
            else:
                result -= right

        return result

    def value():
        nonlocal pos
        result = addit()

        if result is None:
            return None
        if pos < len(tokens) and tokens[pos] == "<=":
            pos += 1
            right = addit()
            if right is None:
                return None
            result = result <= right
        return result

    answer = value()
    if answer is not None and pos != len(tokens):
        print("ERROR: неправильное выражение")
        return None
    return answer


work = input("Введите выражение: ")
ans = calcul(work)

if ans is not None:
    print("Ответ:", ans)
