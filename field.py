from dataclasses import dataclass

@dataclass
class Field:
        xCenterPoint: int = 0
        yCenterPoint: int = 0
        isFilled: bool = False
        isCircle: bool = False
        isCross: bool = False
