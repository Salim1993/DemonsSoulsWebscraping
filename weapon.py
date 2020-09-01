class Weapon:
    def __init__(self, weapon_type, name, phys_atk, phys_def, mag_atk, mag_def, fire_atk, fire_def, aux_damage,
                 aux_type, attack_type, str_req, str_bonus, dex_req, dex_bonus,
                 faith_req, faith_bonus, critical_damage, guard_break_reduction, weight, durability, location):
        self.weapon_type = weapon_type
        self.name = name
        self.phys_atk = phys_atk
        self.phys_def = phys_def
        self.mag_atk = mag_atk
        self.mag_def = mag_def
        self.fire_atk = fire_atk
        self.fire_def = fire_def
        self.aux_damage = aux_damage
        self.aux_type = aux_type
        self.attack_type = attack_type
        self.str_req = str_req
        self.str_bonus = str_bonus
        self.dex_req = dex_req
        self.dex_bonus = dex_bonus
        self.faith_req = faith_req
        self.faith_bonus = faith_bonus
        self.critical_damage = critical_damage
        self.guard_break_reduction = guard_break_reduction
        self.weight = weight
        self.durability = durability
        self.location = location

    def __repr__(self):
        return "<Weapon type:%s name:%s>" % (self.weapon_type, self.name)
