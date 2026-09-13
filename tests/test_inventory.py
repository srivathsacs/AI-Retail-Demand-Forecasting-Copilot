from inventory.inventory_position import InventoryPosition


def test_inventory_position_calculation():
    inventory = InventoryPosition(
        current_inventory=100,
        forecast_demand=80,
        safety_stock=20,
        lead_time_days=5,
    )

    inventory.calculate()

    assert inventory.projected_inventory == 20
    assert inventory.inventory_gap == 0