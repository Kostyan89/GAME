from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Type, Optional
from random import randint
from game.equipment import Weapon, Armor
from game.personages import Personage


BASE_STAMINA_PER_ROUND = 0.4


class Hero(ABC):
    def __init__(self, class_: Type[Personage], weapon: Weapon, armor: Armor, name: str):
        self.class_ = class_
        self.weapon = weapon
        self.armor = armor
        self._stamina = self.class_.max_stamina
        self._hp = self.class_.max_health
        self.skill_used: bool = False
        self.name = name

    @property
    def hp(self):
        return round(self._hp, 1)

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def _total_armor(self) -> float:
        if self.stamina >= self.armor.stamina_per_turn:
            self.stamina -= self.armor.stamina_per_turn
            return self.armor.defence * self.class_.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        if self.stamina < self.weapon.stamina_per_hit:
            return None
        hero_damage = self.weapon.damage * self.class_.attack
        dealt_damage = hero_damage - target._total_armor
        self.stamina -= self.weapon.stamina_per_hit
        if dealt_damage < 0:
            return 0

        return round(dealt_damage, 1)

    def take_hit(self, damage: float):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def regenerate_stamina(self):
        delta_stamina = BASE_STAMINA_PER_ROUND * self.class_.stamina
        if self.stamina + delta_stamina <= self.class_.stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.class_.max_stamina

    def use_skill(self) -> Optional[float]:
        if not self.skill_used and self.stamina - self.class_.skill.stamina >= 0:
            self.skill_used = True
            return round(self.class_.skill.damage, 1)
        return None

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Enemy(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        if random.randint(1, 100) < 11 and self.stamina >= self.class_.skill.stamina and not self.skill_used:
            self.use_skill()
        return self._hit(target)


class Player(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)

