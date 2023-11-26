from PyQt6.QtGui import QImage
from Widgets.Game.Entity.LivingEntity import LivingEntity

# BaseEnemy, add some stuff specific to enemies. (Target, Pathfinding?, Search Radius, Movement speed, etc)
class BaseEnemy(LivingEntity):
    def __init__(self, img: QImage, health):
        super().__init__(img, health)
