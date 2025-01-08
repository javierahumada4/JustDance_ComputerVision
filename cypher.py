class CaesarCipher:
    def __init__(self, step):
        """
        Initializes the CaesarCipher with a specific step.

        Args:
            step (int): The number of positions to shift the characters.
        """
        self.step = step

    def encode(self, message):
        """
        Encodes a message using the Caesar cipher.

        Args:
            message (str): The message to encode.

        Returns:
            str: The encoded message.
        """
        encoded = ""
        for character in message:
            encoded += chr(ord(character) + self.step)
        return encoded

    def decode(self, message):
        """
        Decodes a message encoded with the Caesar cipher.

        Args:
            message (str): The encoded message to decode.

        Returns:
            str: The decoded message.
        """
        decoded = ""
        for character in message:
            decoded += chr(ord(character) - self.step)
        return decoded
