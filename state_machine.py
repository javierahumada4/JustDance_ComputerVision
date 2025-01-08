from detect_shapes import detect_shape
class SecurityStateMachine:
    def __init__(self, password):
        """
        Initialize the state machine with the password sequence.

        :param password: String representing the password (e.g., "t-s-c-t")
        """
        self.password = self.parse_password(password)
        self.current_index = 0

    @staticmethod
    def parse_password(password):
        """
        Parse the password string into a list of states.

        :param password: String representing the password (e.g., "t-s-c-t")
        :return: List of states (e.g., ['triangle', 'square', 'empty', 'circle', 'triangle'])
        """
        mapping = {'t': 'triangle', 'r': "rectangle", '-': 'empty'}
        return [mapping[char] for char in password]

    def reset(self):
        """Reset the state machine to the initial state."""
        self.current_index = 0

    def process_corners(self, corners):
        """
        Process the given corners and validate the current state.

        :param corners: The corners to process.
        :return: True if the current state matches the expected state and the sequence completes, False otherwise.
        """
        # Map state names to corresponding validation functions
        shape  = detect_shape(corners)
        current_state = self.password[self.current_index]

        # Stay in the current state if the current shape matches
        if shape == current_state:
            return 0  # Don't progress yet; wait for the next state

        # Move to the next state if the next shape matches
        if self.current_index < len(self.password) - 1:
            next_state = self.password[self.current_index + 1]
            if shape == next_state:
                self.current_index += 1
                if self.current_index == len(self.password) - 1:
                    self.reset()
                    return 2, shape
                else:
                    return 1, shape
            else:
                self.reset()
            return -1, shape

if __name__ == "__main__":
    # Example usage:
    # Define the password as a string
    password = "t-s-c-t"

    # Initialize the security state machine
    security_system = SecurityStateMachine(password)
    # Test sequence
    input_shapes = ["triangle", "empty", "square", "circle", "triangle"]
    for shape in input_shapes:
        if security_system.process_image(shape):
            break
