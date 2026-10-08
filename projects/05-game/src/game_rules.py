"""Synthetic, in-memory game domain skeleton; no player saves or assets."""
from copy import deepcopy
from dataclasses import dataclass, field
import json


@dataclass
class Player:
    materials: int = 4
    equipment: list = field(default_factory=list)
    receipts: set = field(default_factory=set)
    revision: int = 0


def craft(player, receipt, cost=2, fail_validation=False):
    if receipt in player.receipts:
        return False
    if cost <= 0 or player.materials < cost:
        raise ValueError("recipe cannot be funded")
    before = deepcopy(player)
    try:
        player.materials -= cost
        player.equipment.append("synthetic_sword")
        player.receipts.add(receipt)
        player.revision += 1
        if fail_validation:
            raise ValueError("synthetic validation failure")
    except Exception:
        player.__dict__.update(before.__dict__)
        raise
    return True


def restore(player, snapshot):
    if snapshot.revision < player.revision:
        raise ValueError("stale snapshot cannot overwrite progress")
    player.__dict__.update(deepcopy(snapshot.__dict__))


def layout(window_height, card_height):
    if window_height < card_height + 80:
        raise ValueError("unsupported dimensions")
    controls_top = window_height - 36
    card_bottom = controls_top - 12
    card_top = card_bottom - card_height
    interaction_bottom = card_top - 12
    return {"interaction_bottom": interaction_bottom, "card_top": card_top,
            "card_bottom": card_bottom, "controls_top": controls_top}


if __name__ == "__main__":
    player = Player()
    stale = deepcopy(player)
    assert craft(player, "craft-1")
    assert not craft(player, "craft-1")
    assert player.materials == 2 and len(player.equipment) == 1
    before = deepcopy(player)
    try:
        craft(player, "craft-2", fail_validation=True)
    except ValueError:
        pass
    else:
        raise AssertionError("failure injection was accepted")
    assert player == before
    try:
        restore(player, stale)
    except ValueError:
        pass
    else:
        raise AssertionError("stale progress accepted")
    for height in (600, 720, 900, 1080):
        for card_height in (96, 160):
            bounds = layout(height, card_height)
            assert 0 < bounds['interaction_bottom'] < bounds['card_top'] < bounds['card_bottom'] < bounds['controls_top'] < height
    print(json.dumps({"synthetic": True, "craft_once": True, "validation_rollback": True,
                      "stale_snapshot_rejected": True, "layout_checks": 8,
                      "scope": "in-memory contract only; no Godot runtime or real saves"}))
