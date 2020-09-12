from sqlalchemy import Column, Integer, String, Numeric
from database import Base


class MeeleeWeapon(Base):
    __tablename__ = "meelee_weapons"

    name = Column(String, primary_key=True)
    weapon_type = Column(String)
    phys_atk = Column(Integer)
    phys_def = Column(Integer)
    mag_atk = Column(Integer)
    mag_def = Column(Integer)
    fire_atk = Column(Integer)
    fire_def = Column(Integer)
    aux_damage = Column(Integer)
    aux_type = Column(String)
    types_string = Column(String)
    str_req = Column(Integer)
    str_bonus = Column(String)
    dex_req = Column(Integer)
    dex_bonus = Column(String)
    faith_req = Column(Integer)
    faith_bonus = Column(String)
    critical_damage = Column(Integer)
    guard_break_reduction = Column(Integer)
    weight = Column(Numeric)
    durability = Column(Integer)
    location = Column(String)

    def create_dict_for_update(self):
        return {"weapon_type": self.weapon_type, "phys_atk": self.phys_atk, "phys_def": self.phys_def,
                "mag_atk": self.mag_atk, "mag_def": self.mag_def, "fire_atk": self.fire_atk, "fire_def": self.fire_def,
                "aux_damage": self.aux_damage, "aux_type": self.aux_type, "types_string": self.types_string, "str_req": self.str_req,
                "str_bonus": self.str_bonus, "dex_req": self.dex_req, "dex_bonus": self.dex_bonus, "faith_req": self.faith_req,
                "faith_bonus": self.faith_bonus, "critical_damage": self.critical_damage, "guard_break_reduction": self.guard_break_reduction,
                "weight": self.weight, "durability": self.durability, "location": self.location}

    def __str__(self):
        return "<MeeleeWeapon name:%s weapon_type:%s>" % (self.name, self.weapon_type)

    """
    https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
    """
