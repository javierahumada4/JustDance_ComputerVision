import numpy as np

def calculate_centroid(corners):
    """
    Calculate the centroid of the given corners.

    Parameters:
    corners (list of tuples): List of corner points.

    Returns:
    np.ndarray: The centroid of the corners.
    """
    return np.mean(corners, axis=0)

def calculate_distance(p1, p2):
    """
    Calculate the distance between two points.

    Parameters:
    p1, p2 (tuple): Points to calculate the distance between.

    Returns:
    float: The distance between p1 and p2.
    """
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_angle(v1, v2):
    """
    Calculate the angle between two vectors.

    Parameters:
    v1, v2 (np.ndarray): Vectors to calculate the angle between.

    Returns:
    float: The angle in degrees between v1 and v2.
    """
    dot_product = np.dot(v1, v2)
    magnitude = np.linalg.norm(v1) * np.linalg.norm(v2)
    return np.degrees(np.arccos(dot_product / magnitude))

def sort_corners(corners):
    """
    Sort corners in a consistent order by angle relative to their centroid.

    Parameters:
    corners (list of tuples): List of corner points.

    Returns:
    list of tuples: Sorted corners.
    """
    centroid = calculate_centroid([corner[0] for corner in corners])
    sorted_corners = sorted(corners, key=lambda x: np.arctan2(x[0][1] - centroid[1], x[0][0] - centroid[0]))
    return sorted_corners

def is_rectangle(corners, tolerance=1e-2):
    """
    Determine if the given corners form a rectangle.

    Parameters:
    corners (list of tuples): List of corner points.
    tolerance (float): Tolerance for numerical comparisons.

    Returns:
    bool: True if the corners form a rectangle, False otherwise.
    """
    if len(corners) != 4:
        return False
    corners = sort_corners(corners)
    edges = [calculate_distance(corners[i], corners[(i + 1) % 4]) for i in range(4)]
    if not (abs(edges[0] - edges[2]) < tolerance and abs(edges[1] - edges[3]) < tolerance):
        return False
    vectors = [np.array(corners[(i + 1) % 4]) - np.array(corners[i]) for i in range(4)]
    angles = [calculate_angle(vectors[i], vectors[(i + 1) % 4]) for i in range(4)]
    return all(abs(angle - 90) < tolerance for angle in angles)

def is_triangle(corners, tolerance=1e-2):
    """
    Determine if the given corners form a triangle.

    Parameters:
    corners (list of tuples): List of corner points.
    tolerance (float): Tolerance for numerical comparisons.

    Returns:
    bool: True if the corners form a triangle, False otherwise.
    """
    if len(corners) != 3:
        return False
    corners = sort_corners(corners)
    angles = [
        calculate_angle(np.array(corners[(i + 1) % 3]) - np.array(corners[i]), 
                        np.array(corners[(i + 2) % 3]) - np.array(corners[i])) for i in range(3)
    ]
    return abs(sum(angles) - 180) < tolerance

def is_empty(corners, tolerance=1e-2):
    """
    Check if the given corners represent an empty or degenerate shape.

    Parameters:
    corners (list of tuples): List of corner points.
    tolerance (float): Tolerance for numerical comparisons.

    Returns:
    bool: True if the corners are empty or degenerate, False otherwise.
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
    Retrieve the shape-checking functions.

    Returns:
    dict: A dictionary mapping shape names to their corresponding functions.
    """
    return {
        "rectangle": is_rectangle,
        "triangle": is_triangle,
        "empty": is_empty
    }

def detect_shape(corners, tolerance=50):
    """
    Detect the shape formed by the given corners.

    Parameters:
    corners (list of tuples): List of corner points.
    tolerance (float): Tolerance for numerical comparisons.

    Returns:
    str: The name of the detected shape ("rectangle", "triangle", "empty", or "unknown").
    """
    if is_empty(corners, tolerance):
        return "empty"
    shape_functions = functions()
    for shape, func in shape_functions.items():
        if func(corners, tolerance):
            return shape
    return "unknown"
