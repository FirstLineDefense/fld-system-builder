def calculate_flow(input_data):
    devices = input_data.get("devices", [])

    total_flow = 0
    total_device_count = 0
    device_breakdown = []

    for device in devices:
        name = device.get("name", "Unnamed Device")
        flow_gpm = float(device.get("flow_gpm", 0))
        quantity = int(device.get("quantity", 1))

        line_flow = flow_gpm * quantity

        total_flow += line_flow
        total_device_count += quantity

        device_breakdown.append({
            "name": name,
            "flow_gpm": flow_gpm,
            "quantity": quantity,
            "line_flow_gpm": line_flow
        })

    return {
        "device_count": total_device_count,
        "total_flow_gpm": total_flow,
        "device_breakdown": device_breakdown,
        "notes": "Total flow = sum of each device flow multiplied by quantity."
    }