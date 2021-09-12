import numpy as np


class Plane:
    def __init__(self, origin: np.array, vector1: np.array, vector2: np.array) -> None:
        self.origin = origin
        self.vector1 = vector1
        self.vector2 = vector2

    def getBarycentricCoordinates(self, point: np.array, direction: np.array):
        a = np.array([self.vector1, self.vector2, -direction]).T
        b = point - self.origin
        sol = np.linalg.solve(a, b)

        return np.array([sol[0], sol[1]])


def getQuadrant(x: float, y: float):
    if x >= 0 and y >= 0:
        return 1
    elif x > 0 and y < 0:
        return 2
    elif x <= 0 and y <= 0:
        return 3
    elif x < 0 and y < 0:
        return 4


def doesLineSegmentIntersectRayFromPoint(
    point: np.array,
    ray_direction: np.array,
    lineSegment_start: np.array,
    lineSegment_end: np.array,
):
    # compute intersection of them and check if it's between line start and end
    # check if ray and line are parallel (if A is invertible)
    A = np.array([(lineSegment_end - lineSegment_start), -ray_direction]).T
    if np.linalg.det(A) == 0:
        return False
    b = point - lineSegment_start
    sol = np.linalg.solve(A, b)
    if sol[0] >= 0 and sol[0] <= 1 and sol[1] >= 0:
        return True
    else:
        return False


def isVertexInsidePolygon2D(vertex: np.array, lines: list):
    # if ray intersects an even number of times, then vertex is outside of polygon
    intersections = 0
    for line in lines:
        if doesLineSegmentIntersectRayFromPoint(
            vertex, np.array([1, 0.1]), line[0], line[1]
        ):
            intersections += 1

    # in theory, we'd have to subtract 1 if the ray goes through an exact point per point, but it's very unlikely so we can ignore it for now

    if intersections % 2 == 0:
        return False
    else:
        return True


def isAnyFaceOverVertex(faces: list, vertex: np.array):
    for face in faces:
        # create the lines between visible vertices of a given face (such that they are in order as given by the face)
        visible_vertices_ordered = face.getPolygonOfSelf()
        visible_lines = [
            (visible_vertices_ordered[i], visible_vertices_ordered[i + 1])
            for i in range(len(visible_vertices_ordered) - 1)
        ] + [(visible_vertices_ordered[-1], visible_vertices_ordered[0])]
        if isVertexInsidePolygon2D(vertex, visible_lines):
            return True

    return False
