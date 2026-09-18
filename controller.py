import os

class PoolController:
    """
    Manages screen input automation for Android using adb shell input,
    replacing pyautogui for mobile execution.
    """
    def __init__(self, roi_offset=(0, 0)):
        self.offset_x, self.offset_y = roi_offset

    def set_roi_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def _to_screen_coords(self, local_x, local_y):
        """Converts local ROI coordinates to absolute screen coordinates."""
        return int(local_x + self.offset_x), int(local_y + self.offset_y)

    def auto_shoot(self, x1, y1, x2, y2, duration=0.3):
        """
        Executes swipe action using adb shell input swipe for Android.
        """
        try:
            abs_x1, abs_y1 = self._to_screen_coords(x1, y1)
            abs_x2, abs_y2 = self._to_screen_coords(x2, y2)
            duration_ms = int(duration * 1000)

            cmd = f"adb shell input swipe {abs_x1} {abs_y1} {abs_x2} {abs_y2} {duration_ms}"
            os.system(cmd)
            print(f"[Controller] Executed: {cmd}")
            return True
        except Exception as e:
            print(f"[Controller Error] Failed to execute swipe: {e}")
            return False

    def human_drag_shot(self, cue_pos, ghost_pos, power_factor=1.0):
        """
        Performs a drag shot from cue ball towards ghost ball / pullback position.
        """
        try:
            dx = ghost_pos[0] - cue_pos[0]
            dy = ghost_pos[1] - cue_pos[1]

            # Pullback opposite to aim vector for power simulation
            pullback_x = cue_pos[0] - (dx * 0.2 * power_factor)
            pullback_y = cue_pos[1] - (dy * 0.2 * power_factor)

            return self.auto_shoot(cue_pos[0], cue_pos[1], int(pullback_x), int(pullback_y), duration=0.3)
        except Exception as e:
            print(f"[Controller Error] Failed to simulate drag shot: {e}")
            return False
