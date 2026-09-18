import numpy as np
import math

class GeometryCalculator:
    """
    Performs mathematical calculations for 8 Ball Pool aiming,
    including Ghost Ball placement, angle calculation, and distance/power estimation.
    """
    @staticmethod
    def calculate_distance(p1, p2):
        """Calculates Euclidean distance between two points (x1, y1) and (x2, y2)."""
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    @staticmethod
    def calculate_angle(p1, p2):
        """Calculates angle in degrees from p1 to p2."""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        rad = math.atan2(dy, dx)
        deg = math.degrees(rad)
        return deg

    @staticmethod
    def compute_ghost_ball(target_pos, pocket_pos, ball_radius):
        """
        Computes the Ghost Ball position.
        
        Parameters:
            target_pos: tuple (x, y) of the target ball center.
            pocket_pos: tuple (x, y) of the destination pocket center.
            ball_radius: float/int radius of the balls.
            
        Returns:
            ghost_pos: tuple (x, y) where the cue ball must impact.
        """
        T = np.array(target_pos, dtype=float)
        P = np.array(pocket_pos, dtype=float)
        
        # Vector from Target to Pocket
        TP = P - T
        distance_tp = np.linalg.norm(TP)
        
        if distance_tp == 0:
            return target_pos # Fallback
            
        # Normalized direction vector from Target to Pocket
        u_tp = TP / distance_tp
        
        # Ghost ball is positioned behind the target ball at a distance of 2 * radius along u_tp
        # G = T - (2 * radius) * u_tp
        G = T - (2.0 * ball_radius) * u_tp
        
        return (int(G[0]), int(G[1]))

    @staticmethod
    def evaluate_shot(cue_ball, target_balls, pockets, ball_radius=12):
        """
        Evaluates potential shots by finding the best combination of (cue ball, target ball, pocket).
        
        Parameters:
            cue_ball: tuple (x, y, radius)
            target_balls: list of tuples (x, y, radius)
            pockets: list of tuples (x, y) representing table pockets
            ball_radius: default radius if not specified
            
        Returns:
            best_shot: dict containing target, ghost, pocket, angle, distance, power score, etc., or None.
        """
        if not cue_ball or not target_balls or not pockets:
            return None

        C = (cue_ball[0], cue_ball[1])
        radius = cue_ball[2] if len(cue_ball) > 2 else ball_radius

        best_shot = None
        min_score = float('inf')

        for t_ball in target_balls:
            T = (t_ball[0], t_ball[1])
            
            for pocket in pockets:
                # Ghost ball position for this target ball and pocket
                G = GeometryCalculator.compute_ghost_ball(T, pocket, radius)
                
                # Distance from Cue to Ghost (aiming distance)
                dist_cg = GeometryCalculator.calculate_distance(C, G)
                # Distance from Target to Pocket
                dist_tp = GeometryCalculator.calculate_distance(T, pocket)
                
                # Heuristic score: lower is better (shorter cue-to-ghost + target-to-pocket)
                # Ensure line of sight or valid geometry check if needed
                score = dist_cg + (dist_tp * 0.5)

                if score < min_score:
                    min_score = score
                    angle = GeometryCalculator.calculate_angle(C, G)
                    
                    # Power estimation based on total distance
                    total_dist = dist_cg + dist_tp
                    power = min(100, max(15, int((total_dist / 400.0) * 100)))

                    best_shot = {
                        "cue": C,
                        "target": T,
                        "ghost": G,
                        "pocket": pocket,
                        "angle_deg": angle,
                        "distance_cue_ghost": dist_cg,
                        "distance_target_pocket": dist_tp,
                        "power": power
                    }

        return best_shot
