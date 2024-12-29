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
        password = input("Insert password to create it (ex: t-s-c-t): ")
        if len(password)%2 == 0 or len(password) > 1 and "-" not in password:
            print("Invalid password.")
            continue
        for i in password:
            if i not in "t-sc":
                print("Invalid password")
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