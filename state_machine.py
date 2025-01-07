from detect_shapes import functions
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
        mapping = {'t': 'triangle', 's': 'square', 'c': 'circle', '-': 'empty'}
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
        state_functions = functions()

        current_state = self.password[self.current_index]

        if current_state not in state_functions:
            raise ValueError(f"Invalid state '{current_state}' in password sequence.")

        # Stay in the current state if the current shape matches
        if state_functions[current_state](corners):
            return 0  # Don't progress yet; wait for the next state

        # Move to the next state if the next shape matches
        if self.current_index < len(self.password) - 1:
            next_state = self.password[self.current_index + 1]
            if state_functions[next_state](corners):
                self.current_index += 1
                if self.current_index == len(self.password) - 1:
                    print("Access Granted!")
                    self.reset()
                    return 2
                else:
                    return 1
            return -1

        # Reset only if the shape doesn't match current or next state
        print(f"Incorrect shape. Expected: {current_state}.")
        self.reset()
        return False





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
