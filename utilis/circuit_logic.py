def series_circuit_calc(voltage, r1, r2):
    """Simple series circuit: battery, R1, R2 in series."""
    total_resistance = r1 + r2
    current = voltage / total_resistance
    v_r1 = current * r1
    v_r2 = current * r2
    return {
        "total_resistance": total_resistance,
        "current": current,
        "voltage_r1": v_r1,
        "voltage_r2": v_r2,
    }

def parallel_circuit_calc(voltage, r1, r2):
    """Simple parallel circuit: battery, R1 and R2 in parallel."""
    total_resistance = 1 / ((1 / r1) + (1 / r2))
    total_current = voltage / total_resistance
    current_r1 = voltage / r1
    current_r2 = voltage / r2
    return {
        "total_resistance": total_resistance,
        "total_current": total_current,
        "current_r1": current_r1,
        "current_r2": current_r2,
    }