class CaesarCypher:
    def __init__(self, step):
        self.step = step

    def encode(self, message):
        encoded = ""
        for character in message:
            encoded += chr(ord(character) + self.step)
        return encoded

    def decode(self, message):
        decoded = ""
        for character in message:
            decoded += chr(ord(character) - self.step)
        return decoded