from cypher import CaesarCypher

def create_password():
    password = get_pasword()
    cypher = CaesarCypher(int(input("Set the step for cypher: ")))
    encoded = cypher.encode(password)
    with open("password.txt", "w") as f:
        f.write(encoded)

def get_pasword():
    valid = False
    while not valid:
        password = input("Insert password to create it (example: t-r-t is triangle then rectangle then triangle): ")
        if len(password)%2 == 1:
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
                    if i >1 and password[i-1] not in "tr" or i < len(password) and password[i + 1] not in "tr":
                        print("Invalid password, the password has to have - in between the letters")
                        break
            else:
                valid = True
    return password

def read_password():
    cypher = CaesarCypher(int(input("Set the step for cypher: ")))
    with open("password.txt", "r") as f:
        encoded = f.readline()
    password = cypher.decode(encoded)
    return password
    
if __name__ == "__main__":
    create_password()