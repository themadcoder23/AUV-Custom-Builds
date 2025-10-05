def decimal_to_binary(decimal):#Logic behind bin()function
    for i in range(1,decimal + 1):
        if 2**i > decimal:
            break
    binary = ""
    for j in range(i-1,-1,-1):
        if decimal >= 2**j:
            binary += "1"
            decimal -= 2**j
        else:
            binary += "0"
    return binary

def binary_to_decimal(binary):
    decimal = 0
    length = len(binary)
    for i in range(length):
        decimal += int(binary[length - i - 1])* (2 ** i)
    return decimal

def decimal_to_hexadecimal(decimal):
    hexadecimal = ""
    hex_chars = "0123456789ABCDEF"
    for i in range(1, decimal + 1):
        if 16**i > decimal:
            break
    for j in range(i - 1, -1, -1):
        hex_value = decimal // (16 ** j)
        hexadecimal += hex_chars[hex_value]
        decimal -= hex_value * (16 ** j)
    return hexadecimal

def hexadecimal_to_decimal(hexadecimal):
    decimal = 0
    hex_chars = "0123456789ABCDEF"
    length = len(hexadecimal)
    for i in range(len(hexadecimal)):
        decimal += hex_chars.index(hexadecimal[length - i - 1]) * (16 ** i)
    return decimal

def decimal_to_octal(decimal):
    octal_chars = "01234567"
    octal = ""
    for i in range(1, decimal + 1):
        if 8**i > decimal:
            break
    for j in range(i-1,-1,-1):
        oct_value = decimal//(8**j)
        octal += octal_chars[oct_value]
        decimal -= oct_value * (8**j)
    return octal

def octal_to_decimal(octal):
    decimal = 0
    octal_chars = "01234567"
    length = len(octal)
    for i in range(length):
        decimal += octal_chars.index(octal[length - i - 1]) * (8 ** i)
    return decimal

def octal_to_hexadecimal(octal):
    decimal = octal_to_decimal(octal)
    return decimal_to_hexadecimal(decimal)

def hexadecimal_to_octal(hexadecimal):
    decimal = hexadecimal_to_decimal(hexadecimal)
    return decimal_to_octal(decimal)

def binary_to_hexadecimal(binary):
    decimal = binary_to_decimal(binary)
    return decimal_to_hexadecimal(decimal)
def hexadecimal_to_binary(hexadecimal):
    decimal = hexadecimal_to_decimal(hexadecimal)
    return decimal_to_binary(decimal)
def binary_to_octal(binary):
    decimal = binary_to_decimal(binary)
    return decimal_to_octal(decimal)
def octal_to_binary(octal):
    decimal = octal_to_decimal(octal)
    return decimal_to_binary(decimal)
print("-------------------------------------------------")
print("------------- CONVERSION CALCULATOR -------------")
print("-------------------------------------------------")
print("Select the conversion you want to perform:")
print("Enter 1 for decimal to binary conversion")
print("Enter 2 for binary to decimal conversion")
print("Enter 3 for decimal to hexadecimal conversion")
print("Enter 4 for hexadecimal to decimal conversion")
print("Enter 5 for decimal to octal conversion")
print("Enter 6 for octal to decimal conversion")
print("Enter 7 for octal to hexadecimal conversion")
print("Enter 8 for hexadecimal to octal conversion")
print("Enter 9 for binary to hexadecimal conversion")
print("Enter 10 for hexadecimal to binary conversion")
print("Enter 11 for binary to octal conversion")
print("Enter 12 for octal to binary conversion")
print("Enter 13 to exit the program")
print("-------------------------------------------------")
print("-------------------------------------------------")
while True:
    choice = (input("Enter your choice (1-13): "))

    if choice.isdigit():
        choice = int(choice)
    elif choice.isalpha():
        choice = choice.lower()

    if choice == 1:
        decimal = int(input("Enter the decimal number: "))
        print("Binary:",decimal_to_binary(decimal))
    elif choice == 2:
        binary = input("Enter the binary number: ")
        print("Decimal:",binary_to_decimal(binary))
    elif choice == 3:
        decimal = int(input("Enter the decimal number: "))
        print("Hexadecimal:",decimal_to_hexadecimal(decimal))
    elif choice == 4:
        hexadecimal = input("Enter the hexadecimal number: ")
        print("Decimal:",hexadecimal_to_decimal(hexadecimal))
    elif choice == 5:
        decimal = int(input("Enter the decimal number: "))
        print("Octal:",decimal_to_octal(decimal))
    elif choice == 6:
        octal = input("Enter the octal number: ")
        print("Decimal:",octal_to_decimal(octal))
    elif choice == 7:
        octal = input("Enter the octal number: ")
        print("Hexadecimal:",hexadecimal_to_octal(octal))
    elif choice == 8:
        hexadecimal = input("Enter the hexadecimal number: ")
        print("Octal:",hexadecimal_to_octal(hexadecimal))
    elif choice == 9:
        binary = input("Enter the binary number: ")
        print("Hexadecimal:",binary_to_hexadecimal(binary))
    elif choice == 10:
        hexadecimal = input("Enter the hexadecimal number: ")
        print("Binary:",hexadecimal_to_binary(hexadecimal))
    elif choice == 11:
        binary = input("Enter the binary number: ")
        print("Octal:",binary_to_octal(binary))
    elif choice == 12:
        octal = input("Enter the octal number: ")
        print("Binary:",octal_to_binary(octal))
    elif choice == 13:
        print("Exiting the program.")
        break