from src.tasks.BaseGfTask import BaseGfTask,stamina_re
from src.image.hsv_config import HSVRange as hR

class TestTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试用"
    def run(self):
        result = self.ocr(match="下一步", frame_processor=self.make_hsv_isolator(hR.WHITE),log=True)
        if result:
            self.click(result)
            self.wait_pop_up()
