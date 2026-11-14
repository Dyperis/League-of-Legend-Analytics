def isBuildable(item_id, catalog):
    item = catalog["data"].get(str(item_id))

    if item is None:
        return False

    return (
        item["maps"].get("11", False)
        and item["gold"]["purchasable"]
        and item.get("inStore", True)
        and item.get("requiredChampion") is None
    )