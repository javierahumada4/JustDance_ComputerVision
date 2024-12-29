import numpy as np
def sort_corners(corners):
    corners = [corner[0] for corner in corners]
    # Calculate the centroid of the corners
    centroid = np.mean(corners, axis=0)

    # Sort corners by angle relative to the centroid
    def angle_from_centroid(point):
        vector = np.array(point) - centroid
        return np.arctan2(vector[1], vector[0])  # Y-axis, X-axis

    sorted_corners = sorted(corners, key=lambda x: angle_from_centroid(x))
    return sorted_corners

def is_square(corners, tolerance=1e-2):
    if len(corners) != 4:
        print("Not a square: Incorrect number of corners.")
        return False
    
    corners = sort_corners(corners)

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

def is_rectangle(corners, tolerance=1e-2):
    if len(corners) != 4:
        print("Not a rectangle: Incorrect number of corners.")
        return False
    corners = sort_corners(corners)
    def calculate_distance(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    edges = [
        calculate_distance(corners[0], corners[1]),
        calculate_distance(corners[1], corners[2]),
        calculate_distance(corners[2], corners[3]),
        calculate_distance(corners[3], corners[0])
    ]

    if not abs(edges[0] - edges[2]) < tolerance or not abs(edges[1] - edges[3]) < tolerance:
        print("Not a rectangle: Opposite edges are not equal.")
        return False

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
        print("Not a rectangle: Angles are not 90 degrees.")
        return False

    print("The shape is a rectangle!")
    return True

def is_triangle(corners, tolerance=1e-2):
    if len(corners) != 3:
        print("Not a triangle: Incorrect number of corners.")
        return False
    corners = sort_corners(corners)
    def calculate_angle(a, b, c):
        ab = np.array(b) - np.array(a)
        ac = np.array(c) - np.array(a)
        dot_product = np.dot(ab, ac)
        magnitude = np.linalg.norm(ab) * np.linalg.norm(ac)
        return np.degrees(np.arccos(dot_product / magnitude))

    angles = [
        calculate_angle(corners[0], corners[1], corners[2]),
        calculate_angle(corners[1], corners[2], corners[0]),
        calculate_angle(corners[2], corners[0], corners[1])
    ]

    if not abs(sum(angles) - 180) < tolerance:
        print("Not a triangle: Angles do not sum to 180 degrees.")
        return False

    print("The shape is a triangle!")
    return True

def is_circle(corners, tolerance = 1e-2):
    # TODO
    pass

def is_empty(corners, tolerance = 1e-2):
    # TODO
    pass