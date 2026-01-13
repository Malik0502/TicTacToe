from dataclasses import dataclass

@dataclass
class Field:
        xCenterPoint: int = 0
        yCenterPoint: int = 0
        filled: bool = False
        isCircle: bool = False
