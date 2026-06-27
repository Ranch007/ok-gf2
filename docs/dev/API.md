# ok-gf2 API 参考文档

> 面向开发者的详细 API 参考，涵盖核心基类、工具类及数据层的所有公共接口。

---

## 目录

1. [BaseGfTask](#1-basegftask)
   - [截图与特征匹配](#11-截图与特征匹配)
   - [OCR 识别](#12-ocr-识别)
   - [点击与交互](#13-点击与交互)
   - [按键操作](#14-按键操作)
   - [场景判断](#15-场景判断)
   - [UI 等待](#16-ui-等待)
   - [日志与状态](#17-日志与状态)
   - [图像处理](#18-图像处理)
2. [ScreenPosition](#2-screenposition)
3. [CommunityMixin](#3-communitymixin)

---

## 1. BaseGfTask

所有任务的公共基类，封装了截图、识别、交互等核心能力。

```python
from src.tasks.BaseGfTask import BaseGfTask
```

### 1.1 截图与特征匹配

#### `find_feature`

```python
def find_feature(
    self,
    feature_name,
    *,
    box=None,
    threshold=0,
    use_gray_scale=False,
    horizontal_variance=0,
    vertical_variance=0,
    ...
)
```

在当前帧中进行模板匹配，返回匹配到的 `Box` 列表（未匹配时返回空列表）。
`feature_name` 可传入 `FeatureList` 枚举成员或字符串（图片文件名，不含 `.png`）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `feature_name` | `FeatureList` \| `str` | 特征名 |
| `box` | `Box \| None` | 限制搜索区域 |
| `threshold` | `float` | 匹配阈值，默认 `0`（使用框架默认值） |

```python
boxes = self.find_feature(fL.not_clear_one, box=map_ocr_box)
```

#### `find_one`

```python
def find_one(self, feature_name, **kwargs) -> Box | None
```

`find_feature` 的简化版：返回第一个匹配的 `Box`，未匹配时返回 `None`。

### 1.2 OCR 识别

> 以下方法继承自 `ok-script` 框架的 `BaseTask`。

#### `ocr`

```python
def ocr(
    self,
    box=None,
    match=None,
    name=None,
    threshold=0,
    target_height=0,
    use_grayscale=False,
    log=False,
    frame_processor=None,
    lib='default',
) -> list[dict]
```

对指定区域进行 OCR 识别，返回结果列表，每项包含 `text`、`box` 等字段。

| 参数 | 类型 | 说明 |
|------|------|------|
| `box` | `Box \| None` | 识别区域；`None` 为全屏 |
| `match` | `str \| re.Pattern \| None` | 文本过滤条件（字符串子串或正则） |
| `name` | `str \| None` | 日志标签 |
| `threshold` | `float` | 置信度阈值 |
| `frame_processor` | `callable \| None` | 图像预处理函数 |

```python
result = self.ocr(box=self.box.bottom, match=re.compile(r"\d+"))
```

#### `wait_ocr`

```python
def wait_ocr(self, match, box=None, time_out=5, **kwargs) -> list[dict] | None
```

阻塞等待直到 OCR 匹配成功或超时。成功返回结果列表，超时返回 `None`。

```python
result = self.wait_ocr(match="确认", box=self.box.center, time_out=10)
```

#### `wait_click_ocr`

```python
def wait_click_ocr(
    self,
    match=None,
    box=None,
    time_out=0,
    after_sleep=0,
    raise_if_not_found=False,
    ...
)
```

等待 OCR 匹配成功后点击匹配区域。成功返回匹配结果，超时返回 `None`。

```python
self.wait_click_ocr(match="开始", box=self.box.bottom, time_out=8)
```

#### `wait_ocr_until_count`

```python
def wait_ocr_until_count(self, match, box=None, min_count=2, timeout=5, interval=0.5, **kwargs)
```

固定时间内循环 OCR，检测到对象数 >= min_count 立即返回，否则超时。

### 1.3 点击与交互

#### `click`

```python
def click(self, x=-1, y=-1, *, box=None, name=None, interval=-1, move=True, down_time=0.01, after_sleep=0, key='left')
```

点击指定坐标或 `Box` 中心。

```python
self.click(0.5, 0.5)          # 屏幕中心（比例）
self.click(box=confirm_box)   # 点击 Box 中心
```

#### `click_with_key`

```python
def click_with_key(self, key, box)
```

按住指定修饰键再点击，常用于物品转移等需要组合键的操作。

```python
self.click_with_key('alt', result)
```

#### `back`

返回/退出当前界面。

### 1.4 按键操作

#### `press_keys_sequence`

```python
def press_keys_sequence(self, keys, down_times, sleep_between=0.5)
```

依次按住多个按键指定时长后松开。

```python
self.press_keys_sequence(['a', 'w', 'd'], [1.087, 1.4, 0.5], sleep_between=0.5)
```

### 1.5 场景判断

#### `ensure_main`

```python
def ensure_main(self, recheck_time=1, time_out=30, esc=True)
```

确保当前位于游戏主界面，否则尝试返回主界面。超时抛异常。

#### `is_main`

判断当前是否处于游戏主界面。

#### `skip_dialogs`

```python
def skip_dialogs(self, end_match, end_box=None, time_out=120, has_dialog=True, raise_if_not_found=True)
```

跳过剧情对话直到匹配到目标文本。

#### `wait_pop_up`

等待并关闭弹窗（如"点击空白处关闭"等）。

### 1.6 UI 等待

#### `wait_until`

```python
def wait_until(self, condition, time_out=30) -> bool
```

等待条件函数返回 True，超时返回 False。

### 1.7 日志与状态

#### `log_info` / `log_debug` / `log_error`

日志输出方法。

#### `info_set`

设置当前任务状态信息。

### 1.8 图像处理

#### `isolate_by_hsv_ranges`

```python
def isolate_by_hsv_ranges(self, frame, ranges, invert=True, kernel_size=2)
```

按 HSV 范围提取颜色区域。

#### `make_hsv_isolator`

```python
def make_hsv_isolator(self, ranges)
```

生成固定 HSV 范围的图像处理函数。

```python
processor = self.make_hsv_isolator(hR.WHITE)
```

#### `get_role_by_name`

```python
def get_role_by_name(self, name)
```

根据角色名称返回其属性（物理/燃烧/电导/冷凝/浊刻/酸蚀）。

---

## 2. ScreenPosition

屏幕坐标工具，提供常用区域定位。

```python
from src.interaction.ScreenPosition import ScreenPosition
```

### 常用区域

| 属性 | 说明 |
|------|------|
| `top_right` | 屏幕右上区域 |
| `bottom_right` | 屏幕右下区域 |
| `bottom_left` | 屏幕左下区域 |
| `center` | 屏幕中央区域 |

```python
self.box = ScreenPosition(self)
result = self.wait_ocr(match="确认", box=self.box.center)
```

---

## 3. CommunityMixin

社区每日任务 API 客户端 Mixin。

```python
from src.tasks.CommunityClient import CommunityMixin
```

### 方法

#### `login`

```python
def login(self, account: str, password: str, source: str = "phone") -> Optional[str]
```

通过社区 API 登录，返回 token。

#### `run_community_flow`

```python
def run_community_flow(self, user: str, pwd: str)
```

执行社区每日任务完整流程（签到等）。
