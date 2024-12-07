from abc import ABC, abstractmethod
from BloomEffect import bloom_effect24, bloom_effect32
import pygame

class Effect(ABC):
    @abstractmethod
    def apply(self, surface):
        raise NotImplementedError("Apply method must be implemented by subclasses")
