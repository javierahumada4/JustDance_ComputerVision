from cypher import CaesarCypher

def create_password():
    """
    Create and save an encoded password using Caesar Cypher.

    This function prompts the user to enter a password, encodes it using a specified step for the Caesar Cypher,
    and saves the encoded password to a file.
    """
    password = get_pasword()
    cypher = CaesarCypher(int(input("Set the step for cypher: ")))
    encoded = cypher.encode(password)
    with open("password.txt", "w") as f:
        f.write(encoded)

def get_pasword():
    """
    Prompt the user to input a valid password.

    The password must consist of 't' and 'r' separated by '-' and follow specific format rules.
    Returns the valid password.

    Returns:
    str: The validated password.
    """
    valid = False
    while not valid:
        password = input("Insert password to create it (example: t-r-t is triangle then rectangle then triangle): ")
        if len(password) % 2 == 1:
            print("Invalid password, the password has to have - in between the letters")
            continue
        if len(password) == 2:
            if password[0] == "-" and password[1] in "tr":
                valid = True
        else:
            for i, letter in enumerate(password):
                if letter not in "t-r":
                    print("Invalid password, some of the letters weren't correct")
                    break
                if letter == "-":
                    if i > 1 and password[i-1] not in "tr" or i < len(password) - 1 and password[i + 1] not in "tr":
                        print("Invalid password, the password has to have - in between the letters")
                        break
            else:
                valid = True
    return password

def read_password():
    """
    Read and decode a password from a file using Caesar Cypher.

    This function reads the encoded password from a file, decodes it using a specified step for the Caesar Cypher,
    and returns the decoded password.

    Returns:
    str: The decoded password.
    """
    cypher = CaesarCypher(int(input("Set the step for cypher: ")))
    with open("password.txt", "r") as f:
        encoded = f.readline()
    password = cypher.decode(encoded)
    return password

if __name__ == "__main__":
    create_password()
