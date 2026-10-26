"""Pure planar reveal from an inner image to its surrounding painted-world frame.

Dependencies: NumPy and OpenCV. No file I/O, time line, asset names, fonts, audio,
runtime path changes, or implicit installation. This is two homographies, not 3D.

Coordinates are outer-image pixel centres: x right, y down, 0..width-1 and
0..height-1. The quadrilateral is TL, TR, BR, BL clockwise in this coordinate
system. For this upright-canvas contract, TL is the unique vertex minimizing
x/(width-1) + y/(height-1); cyclic rotations and reversed order are rejected.
"""

from __future__ import annotations

from numbers import Real

import cv2
import numpy as np

__all__ = ["reveal_painted_world"]


def _rgb(value: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 3 or array.shape[2] != 3:
        raise ValueError(f"{name} must have shape (height, width, 3); RGBA is not accepted")
    if min(array.shape[:2]) < 2:
        raise ValueError(f"{name} width and height must each be at least 2 pixels")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array, dtype=np.float32) / np.float32(255)
    if not np.issubdtype(array.dtype, np.floating):
        raise TypeError(f"{name} must be uint8 RGB or floating RGB in [0, 1]")
    if not np.isfinite(array).all() or array.min() < 0 or array.max() > 1:
        raise ValueError(f"{name} floating values must be finite and within [0, 1]")
    return np.ascontiguousarray(array, dtype=np.float32)


def _unit_interval(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real scalar in [0, 1]")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise TypeError(f"{name} must be a real scalar in [0, 1]") from error
    if not np.isfinite(number) or not 0 <= number <= 1:
        raise ValueError(f"{name} must be finite and within [0, 1]")
    return number


def _quad(value: np.ndarray, width: int, height: int) -> np.ndarray:
    try:
        points = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise ValueError("canvas_quad must be a finite (4, 2) array") from error
    if points.shape != (4, 2) or not np.isfinite(points).all():
        raise ValueError("canvas_quad must be a finite (4, 2) array")
    if ((points < 0).any() or (points[:, 0] > width - 1).any()
            or (points[:, 1] > height - 1).any()):
        raise ValueError("canvas_quad must lie within outer-image pixel-centre bounds")
    edges = np.roll(points, -1, axis=0) - points
    following = np.roll(edges, -1, axis=0)
    crosses = edges[:, 0] * following[:, 1] - edges[:, 1] * following[:, 0]
    # Positive crosses enforce convexity and TL/TR/BR/BL winding in y-down space.
    tolerance = max(1e-7, (width - 1) * (height - 1) * 1e-9)
    area = .5 * np.sum(points[:, 0] * np.roll(points[:, 1], -1)
                       - points[:, 1] * np.roll(points[:, 0], -1))
    if (crosses <= tolerance).any() or area < 1.0:
        raise ValueError("canvas_quad must be strictly convex, clockwise, and nondegenerate (area >= 1 pixel²)")
    corner_scores = points[:, 0] / (width - 1) + points[:, 1] / (height - 1)
    if (corner_scores[1:] <= corner_scores[0] + 1e-7).any():
        raise ValueError("canvas_quad must start at its unambiguous top-left corner, followed by TR, BR, BL")
    return points.astype(np.float32)


def _homography(source: np.ndarray, destination: np.ndarray) -> np.ndarray:
    matrix = cv2.getPerspectiveTransform(source, destination)
    if not np.isfinite(matrix).all() or np.linalg.cond(matrix) > 1e12:
        raise ValueError("canvas_quad produces an unstable or singular homography")
    return matrix


def reveal_painted_world(
    inner_rgb: np.ndarray,
    outer_rgb: np.ndarray,
    canvas_quad: np.ndarray,
    progress: float,
    *,
    live_inner_rgb: np.ndarray | None = None,
    live_weight: float = 1.0,
) -> np.ndarray:
    """Return an outer-sized float32 RGB frame in [0, 1], without changing inputs.

    ``inner_rgb`` and ``outer_rgb`` can have different dimensions. Each must be
    H×W×3 uint8 [0, 255] or floating [0, 1], with H,W >= 2. RGBA is rejected so
    alpha conventions cannot be silently confused. Pre-composite any intended
    transparency before calling, and apply any foreground occluder afterwards.

    ``canvas_quad`` uses the outer-image pixel coordinates and validated corner
    order described in the module docstring. It must be wholly inside the outer
    image, strictly convex, and have area >= 1 square pixel. Rotated/ambiguous
    top-left labelling, crossing/concave/degenerate quads raise ValueError.

    ``progress`` is already-eased progress in [0, 1]: 0 fills the output with the
    canvas; 1 reveals the entire outer image with the inner image on its canvas.
    No easing, time, fade or camera depth is inferred. Input ranges are checked,
    not silently clipped. Only final floating roundoff is clipped to [0, 1].

    Optional ``live_inner_rgb`` must match the inner image's shape; it is mixed
    with the still inner image using ``live_weight`` in [0, 1]. A caller can fade
    live_weight to zero to freeze the image without changing the reveal geometry.

    Both texture and all-ones alpha are warped with the same linear filter. The
    constant-black warped RGB already contains edge coverage (premultiplied),
    so it is added once, not multiplied by the warped mask a second time.
    The whole composite then uses BORDER_REPLICATE to preserve the established
    two-stage resampling behaviour. Arbitrary oblique canvases can stretch edge
    pixels where the requested view extends beyond the available outer image.
    No unseen scene, reverse surface, perspective parallax or 3D is generated.
    """
    inner = _rgb(inner_rgb, "inner_rgb")
    outer = _rgb(outer_rgb, "outer_rgb")
    amount = _unit_interval(progress, "progress")
    weight = _unit_interval(live_weight, "live_weight")
    if live_inner_rgb is not None:
        live = _rgb(live_inner_rgb, "live_inner_rgb")
        if live.shape != inner.shape:
            raise ValueError("live_inner_rgb must match inner_rgb dimensions")
        inner = inner * np.float32(1 - weight) + live * np.float32(weight)
    height, width = outer.shape[:2]
    ih, iw = inner.shape[:2]
    quad = _quad(canvas_quad, width, height)
    inner_rect = np.float32([[0, 0], [iw - 1, 0], [iw - 1, ih - 1], [0, ih - 1]])
    output_rect = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    insertion = _homography(inner_rect, quad)
    warped = cv2.warpPerspective(inner, insertion, (width, height), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    mask = cv2.warpPerspective(np.ones((ih, iw), np.float32), insertion, (width, height),
                              flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    composite = outer * (1 - mask[:, :, None]) + warped
    target = output_rect * (1 - amount) + quad * amount
    # The interpolation itself must also remain a valid upright convex view.
    _quad(target, width, height)
    reveal = _homography(quad, target)
    output = cv2.warpPerspective(composite, reveal, (width, height), flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_REPLICATE)
    return np.clip(output, 0, 1).astype(np.float32, copy=False)
