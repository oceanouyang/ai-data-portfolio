extends Node

# Independent rule skeleton. No game art, accounts, or filesystem persistence.
var materials := 4
var equipment: Array[String] = []
var receipts: Dictionary = {}

func craft(receipt: String, cost: int) -> bool:
    if receipts.has(receipt):
        return false
    if cost <= 0 or materials < cost:
        return false
    materials -= cost
    equipment.append("synthetic_sword")
    receipts[receipt] = true
    return true

func _ready() -> void:
    var first := craft("craft-1", 2)
    var duplicate := craft("craft-1", 2)
    var insufficient := craft("craft-2", 3)
    var passed := first and not duplicate and not insufficient and materials == 2 and equipment.size() == 1
    print(JSON.stringify({"synthetic": true, "craft_once": passed, "scope": "Godot rule skeleton only"}))
    get_tree().quit(0 if passed else 1)
