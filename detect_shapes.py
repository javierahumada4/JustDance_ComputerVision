import numpy as np

def sort_corners(corners):
    """
    Sorts the corners of a shape based on their angle relative to the centroid.
    
    Args:
        corners (list of tuples): A list of corner points represented as (x, y) tuples.

    Returns:
        list: The sorted corners, ordered by their angle from the centroid.
    """
    corners = [corner[0] for corner in corners]
    # Calculate the centroid of the corners
    centroid = np.mean(corners, axis=0)

    # Sort corners by angle relative to the centroid
    def angle_from_centroid(point):
        vector = np.array(point) - centroid
        return np.arctan2(vector[1], vector[0])  # Y-axis, X-axis

    sorted_corners = sorted(corners, key=lambda x: angle_from_centroid(x))
    return sorted_corners

def is_rectangle(corners, tolerance=1e-2):
    """
    Checks if a given set of corners represents a rectangle.

    Args:
        corners (list of tuples): A list of 4 corner points representing a shape.
        tolerance (float): The tolerance used to check distances and angles (default is 1e-2).

    Returns:
        bool: True if the corners form a rectangle, False otherwise.
    """
    if len(corners) != 4:
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
        return False

    return True

def is_triangle(corners, tolerance=1e-2):
    """
    Checks if a given set of corners represents a triangle.

    Args:
        corners (list of tuples): A list of 3 corner points representing a shape.
        tolerance (float): The tolerance used to check angles (default is 1e-2).

    Returns:
        bool: True if the corners form a triangle, False otherwise.
    """
    if len(corners) != 3:
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
        return False

    return True

def is_empty(corners, tolerance=1e-2):
    """
    Checks if a set of corners is degenerate or empty.

    Args:
        corners (list of tuples): A list of corner points.
        tolerance (float): The tolerance used for checking degeneracy (default is 1e-2).

    Returns:
        bool: True if the corners represent an empty or degenerate shape, False otherwise.
    """
    if len(corners) == 0:
        return True

    # Check if all points are degenerate (e.g., all zeros or the same point)
    if all(np.allclose(np.array(corner), 0, atol=tolerance) for corner in corners):
        return True
    
    functions = [is_triangle, is_rectangle]
    for func in functions:
        if func(corners, tolerance):
            break
    else:
        return True

    return False

def functions():
    """
    Returns a dictionary of shape detection functions.

    Returns:
        dict: A dictionary mapping shape names to their corresponding detection functions.
    """
    return {
        "rectangle": is_rectangle,
        "triangle": is_triangle,
        "empty": is_empty
    }

def detect_shape(corners, tolerance = 50):
    """
    Detects the shape of a set of corners.

    Args:
        corners (list of tuples): A list of corner points.
        tolerance (float): The tolerance for shape detection (default is 50).

    Returns:
        str: The name of the detected shape ("rectangle", "triangle", "empty", or "unknown").
    """
    for shape, func in functions().items():
        result = func(corners, tolerance)
        if result:
            return shape
    return "unknown"
