from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import cv2

from capture import ScreenCapture
from detector import BallDetector
from geometry import GeometryCalculator
from controller import PoolController

class PoolAimApp(App):
    """
    Main Kivy application for the 8 Ball Pool Visual Assist & Practice Tool on Android.
    Integrates capture, detection, geometry, and controller with a Kivy GUI.
    """
    def build(self):
        self.title = "8 Ball Pool Aim Assist"
        
        # Initialize core modules
        self.capture_manager = ScreenCapture(roi=(100, 100, 800, 500))
        self.detector = BallDetector(min_radius=8, max_radius=30)
        self.controller = PoolController(roi_offset=(100, 100))

        self.is_running = False
        self.default_pockets = [
            (35, 30),     # Top-Left
            (400, 25),    # Top-Middle
            (765, 30),    # Top-Right
            (35, 470),    # Bottom-Left
            (400, 475),   # Bottom-Middle
            (765, 470)    # Bottom-Right
        ]

        # Layout setup
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        self.lbl_status = Label(
            text="الحالة: متوقف (Stopped)",
            font_size=18,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.lbl_status)

        self.btn_toggle = Button(
            text="تشغيل المساعد (Start Aim Assist)",
            font_size=18,
            size_hint_y=None,
            height=60
        )
        self.btn_toggle.bind(on_press=self.toggle_assistant)
        layout.add_widget(self.btn_toggle)

        self.btn_calibrate = Button(
            text="معايرة الشاشة (Calibrate Screen)",
            font_size=18,
            size_hint_y=None,
            height=60
        )
        self.btn_calibrate.bind(on_press=self.calibrate)
        layout.add_widget(self.btn_calibrate)

        self.btn_test = Button(
            text="تنفيذ تسديدة تجريبية (Test Shot)",
            font_size=18,
            size_hint_y=None,
            height=60
        )
        self.btn_test.bind(on_press=self.test_shot)
        layout.add_widget(self.btn_test)

        self.lbl_telemetry = Label(
            text="بيانات القياس والزوايا ستظهر هنا...",
            font_size=16,
            halign='center',
            valign='middle'
        )
        self.lbl_telemetry.bind(size=self.lbl_telemetry.setter('text_size'))
        layout.add_widget(self.lbl_telemetry)

        return layout

    def toggle_assistant(self, instance):
        if not self.is_running:
            self.is_running = True
            self.btn_toggle.text = "إيقاف المساعد (Stop Aim Assist)"
            self.lbl_status.text = "الحالة: يعمل (Running)"
            Clock.schedule_interval(self.main_loop, 1.0 / 30.0)
        else:
            self.is_running = False
            self.btn_toggle.text = "تشغيل المساعد (Start Aim Assist)"
            self.lbl_status.text = "الحالة: متوقف (Stopped)"
            Clock.unschedule(self.main_loop)

    def main_loop(self, dt):
        if not self.is_running:
            return

        frame = self.capture_manager.capture_frame()
        if frame is None or frame.size == 0:
            return

        cue_ball, target_balls = self.detector.detect_balls(frame)
        shot = GeometryCalculator.evaluate_shot(cue_ball, target_balls, self.default_pockets)

        if shot:
            self.lbl_telemetry.text = (
                f"الكرة البيضاء: {shot['cue']}\n"
                f"الكرة المستهدفة: {shot['target']}\n"
                f"الكرة الوهمية (Ghost): {shot['ghost']}\n"
                f"زاوية التسديد: {shot['angle_deg']:.1f}°\n"
                f"المسافة: {shot['distance_cue_ghost']:.1f} px | القوة: {shot['power']}%"
            )
        else:
            self.lbl_telemetry.text = "جاري البحث عن الكرات..."

    def calibrate(self, instance):
        self.lbl_telemetry.text = "تم استدعاء معايرة الشاشة (ROI Calibration)."

    def test_shot(self, instance):
        success = self.controller.auto_shoot(100, 200, 300, 400)
        if success:
            self.lbl_telemetry.text = "تم تنفيذ التسديدة التجريبية بنجاح عبر ADB."
        else:
            self.lbl_telemetry.text = "فشل تنفيذ التسديدة التجريبية."

if __name__ == "__main__":
    PoolAimApp().run()
