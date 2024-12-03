def is_square(corners, tolerance=1e-2):
    import numpy as np

    if len(corners) != 4:
        print("Not a square: Incorrect number of corners.")
        return False

    # Calculate edge lengths
    def calculate_distance(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    edges = [
        calculate_distance(corners[0], corners[1]),
        calculate_distance(corners[1], corners[2]),
        calculate_distance(corners[2], corners[3]),
        calculate_distance(corners[3], corners[0])
    ]

    if not all(abs(edges[0] - edge) < tolerance for edge in edges):
        print("Not a square: Edges are not equal.")
        return False

    # Calculate angles
    def calculate_angle(v1, v2):
        dot_product = np.dot(v1, v2)
        magnitude = np.linalg.norm(v1) * np.linalg.norm(v2)
        return np.degrees(np.arccos(dot_product / magnitude))

    vectors = [
        np.array(corners[1]) - np.array(corners[0]),
        np.array(corners[2]) - np.array(corners[1]),
        np.array(corners[3]) - np.array(corners[2]),
        np.array(corners[0]) - np.array(corners[3])
    ]

    angles = [
        calculate_angle(vectors[0], vectors[1]),
        calculate_angle(vectors[1], vectors[2]),
        calculate_angle(vectors[2], vectors[3]),
        calculate_angle(vectors[3], vectors[0])
    ]

    if not all(abs(angle - 90) < tolerance for angle in angles):
        print("Not a square: Angles are not 90 degrees.")
        return False

    print("The shape is a square!")
    return True