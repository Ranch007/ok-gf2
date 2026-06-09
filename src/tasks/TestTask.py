from src.tasks.DailyTask import DailyTask,stamina_re
from src.image.hsv_config import HSVRange as hR

class TestTask(DailyTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试用"
        self.default_config=dict()
    def run(self):
        self.auto_loop()
        self.find_one(feature_name="dog_icon")
        self.find_feature()
        self.wait_click_feature("ggq_can_button")
        self.find_one("")