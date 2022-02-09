class Unit:
    def __init__(self, name, max_health, armor=0):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.full_armor = armor
        self.armor = armor
        self.is_active = True
        self.is_dead = False
        self.is_poison = False
        self.is_burn = False

    def gain_health(self, value):
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health
    
    def lose_health(self, value):
        if self.armor > 0:
            if value >= self.armor:
                value -= self.armor
                self.armor = 0    
            else:
                self.armor -= value
                return
        self.health -= value
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
        


    

