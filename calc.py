class calc:
    def add(self, num1, num2):
        return num1 + num2

    def sub(self, num1, num2):
        return num1 - num2

    def mul(self, num1, num2):
        return num1 * num2

    def div(self, num1, num2):
        return num1 / num2


calculator = calc()


def run_console():
    while True:
        try:
            print("==========WELCOME TO CALCULATOR==========")
            print("1. ADDITION")
            print("2. SUBTRACTION")
            print("3. MULTIPLY")
            print("4. DIVISION")

            op = int(input("CHOOSE A OPERATION NUMBER: "))
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if op == 1:
                result = calculator.add(num1, num2)
                operator = "+"
            elif op == 2:
                result = calculator.sub(num1, num2)
                operator = "-"
            elif op == 3:
                result = calculator.mul(num1, num2)
                operator = "*"
            elif op == 4:
                result = calculator.div(num1, num2)
                operator = "/"
            else:
                print("Invalid input")
                continue

            print(f"Result: {result}")
            with open("history.txt", "a", encoding="utf-8") as file:
                file.write(f"{num1}{operator}{num2}={result}\n")

        except ZeroDivisionError:
            print("Zero cannot be divisible")
        except ValueError:
            print("Enter numbers only")

        con = input("Continue (Y/N) or see history (H): ").strip().upper()
        if con == "N":
            break
        elif con == "H":
            print("\n========== HISTORY ==========")
            with open("history.txt", "a+", encoding="utf-8") as file:
                file.seek(0)
                print(file.read())


if __name__ == "__main__":
    run_console()



  
        
