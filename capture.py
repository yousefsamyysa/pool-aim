import cv2
import numpy as np
import os

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

class ScreenCapture:
    """
    Manages dynamic Region of Interest (ROI) screen capture for Android (via adb screencap)
    and desktop fallback (via mss).
    """
    def __init__(self, roi=None):
        self.roi = roi if roi else (0, 0, 800, 600)
        self.sct = mss.mss() if MSS_AVAILABLE else None

    def set_roi(self, x, y, width, height):
        """Sets the active Region of Interest."""
        self.roi = (int(x), int(y), int(width), int(height))

    def get_roi(self):
        """Returns current ROI coordinates."""
        return self.roi

    def capture_frame(self):
        """
        Captures the screen within the defined ROI and returns an OpenCV BGR numpy array.
        """
        x, y, w, h = self.roi
        try:
            # 1. Try Android adb screencap
            os.system("adb exec-out screencap -p > screen.png")
            if os.path.exists("screen.png") and os.path.getsize("screen.png") > 0:
                frame = cv2.imread("screen.png")
                if frame is not None and frame.size > 0:
                    if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                        x2 = min(x + w, frame.shape[1])
                        y2 = min(y + h, frame.shape[0])
                        cropped = frame[y:y2, x:x2]
                        if cropped.size > 0:
                            return cropped
                    return frame

            # 2. Fallback to mss (desktop)
            if self.sct:
                monitor = {"top": y, "left": x, "width": w, "height": h}
                sct_img = self.sct.grab(monitor)
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                return frame

        except Exception as e:
            print(f"[Capture Error] Failed to capture screen: {e}")

        # Fallback return black frame
        return np.zeros((h, w, 3), dtype=np.uint8)

    def __del__(self):
        if self.sct:
            self.sct.close()
