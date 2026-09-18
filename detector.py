import cv2
import numpy as np

class BallDetector:
    """
    Detects cue ball and target balls in 8 Ball Pool using HSV color filtering,
    contour analysis, circularity filtering, and radius constraints.
    """
    def __init__(self, min_radius=8, max_radius=30):
        self.min_radius = min_radius
        self.max_radius = max_radius

        # HSV color ranges for Cue Ball (White)
        # High value (brightness), low saturation
        self.cue_lower = np.array([0, 0, 200], dtype=np.uint8)
        self.cue_upper = np.array([180, 45, 255], dtype=np.uint8)

        # HSV color ranges for Target Balls (general colored balls range: Saturation > 50, Value > 50)
        self.target_lower = np.array([0, 50, 50], dtype=np.uint8)
        self.target_upper = np.array([180, 255, 255], dtype=np.uint8)

    def set_radius_bounds(self, min_r, max_r):
        self.min_radius = int(min_r)
        self.max_radius = int(max_r)

    def _filter_contours(self, thresh, frame_shape):
        """
        Filters contours based on area, circularity, and radius constraints.
        Returns a list of tuples: (center_x, center_y, radius, contour)
        """
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_balls = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < np.pi * (self.min_radius ** 2) * 0.4:
                continue

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue

            # Circularity metric: 4 * pi * Area / (Perimeter^2)
            circularity = (4 * np.pi * area) / (perimeter ** 2)

            # Pool balls should be quite circular (circularity > 0.7)
            if circularity < 0.65:
                continue

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if self.min_radius <= radius <= self.max_radius:
                valid_balls.append((int(x), int(y), float(radius), cnt))

        return valid_balls

    def detect_balls(self, frame):
        """
        Processes frame and returns:
            cue_ball: (x, y, radius) or None
            target_balls: list of (x, y, radius)
        """
        if frame is None or frame.size == 0:
            return None, []

        try:
            # Apply slight Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(frame, (5, 5), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # 1. Detect Cue Ball (White)
            mask_cue = cv2.inRange(hsv, self.cue_lower, self.cue_upper)
            # Morphological operations to clean noise
            kernel = np.ones((3, 3), np.uint8)
            mask_cue = cv2.morphologyEx(mask_cue, cv2.MORPH_OPEN, kernel)
            mask_cue = cv2.morphologyEx(mask_cue, cv2.MORPH_CLOSE, kernel)

            cue_candidates = self._filter_contours(mask_cue, frame.shape)
            cue_ball = None
            if cue_candidates:
                # Pick the most prominent/circular or first valid candidate as cue ball
                # Sort by circularity or proximity to expected center if needed, here take largest valid
                cue_candidates.sort(key=lambda b: b[2], reverse=True)
                cx, cy, cr, _ = cue_candidates[0]
                cue_ball = (cx, cy, cr)

            # 2. Detect Target Balls (Colored balls)
            mask_target = cv2.inRange(hsv, self.target_lower, self.target_upper)
            # Exclude cue ball region from target mask if cue ball detected
            if cue_ball:
                cv2.circle(mask_target, (cue_ball[0], cue_ball[1]), int(cue_ball[2] * 1.5), 0, -1)

            mask_target = cv2.morphologyEx(mask_target, cv2.MORPH_OPEN, kernel)
            mask_target = cv2.morphologyEx(mask_target, cv2.MORPH_CLOSE, kernel)

            target_candidates = self._filter_contours(mask_target, frame.shape)
            target_balls = [(tx, ty, tr) for tx, ty, tr, _ in target_candidates]

            return cue_ball, target_balls

        except Exception as e:
            print(f"[Detector Error] Error during ball detection: {e}")
            return None, []
