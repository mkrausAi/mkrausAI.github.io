import numpy as np

def is_inside_polygon(x, y, poly_x, poly_y):
    n = len(poly_x)
    inside = False
    p1x, p1y = poly_x[0], poly_y[0]
    for i in range(n + 1):
        p2x, p2y = poly_x[i % n], poly_y[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def compute_signed_distance_vectorized(points, poly_x, poly_y):
    # Ensure poly_x and poly_y have the same length
    min_len = min(len(poly_x), len(poly_y))
    poly_x = poly_x[:min_len]
    poly_y = poly_y[:min_len]
    
    poly_points = np.column_stack((poly_x, poly_y))
    n = len(poly_points)
    
    def point_to_line_segment_distance(p, a, b):
        ab = b - a
        ap = p - a
        epsilon = 1e-10
        projection = np.dot(ap, ab) / (np.dot(ab, ab) + epsilon)
        projection = np.clip(projection, 0, 1)
        closest = a + projection * ab
        return np.linalg.norm(p - closest)
    
    distances = np.array([
        min(point_to_line_segment_distance(p, poly_points[i], poly_points[(i + 1) % n])
            for i in range(n))
        for p in points
    ])
    
    inside = np.array([is_inside_polygon(point[0], point[1], poly_x, poly_y) for point in points])
    
    return np.where(inside, distances, -distances)

def sample_domain(x, y, method='random', n_samples=500, grid_size=(50, 50), dx = 0.1, dy = 0.1):
    """
    Sample points in a domain using either random sampling or grid sampling.

    Parameters:
    - x, y: Lists or arrays of coordinates defining the domain.
    - method: 'random' or 'grid' to specify the sampling method.
    - n_samples: Number of random samples (used only if method='random').
    - grid_size: Tuple specifying the grid size (used only if method='grid').

    Returns:
    - sample_points: A 2D array of sampled points.
    - signed_distances: Signed distances of the sampled points.
    """
    x_min, x_max = min(x) - dx, max(x) + dx
    y_min, y_max = min(y) - dy, max(y) + dy

    if method == 'random':
        # Random sampling
        x_samples = np.random.uniform(x_min, x_max, n_samples)
        y_samples = np.random.uniform(y_min, y_max, n_samples)
        sample_points = np.column_stack((x_samples, y_samples))
    elif method == 'grid':
        # Grid sampling
        grid_size_x, grid_size_y = grid_size
        x_grid = np.linspace(x_min, x_max, grid_size_x)
        y_grid = np.linspace(y_min, y_max, grid_size_y)
        x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
        sample_points = np.column_stack((x_mesh.ravel(), y_mesh.ravel()))
    else:
        raise ValueError("Method must be 'random' or 'grid'.")

    # Compute signed distances using the vectorized function
    signed_distances = compute_signed_distance_vectorized(sample_points, x, y)

    return sample_points, signed_distances
