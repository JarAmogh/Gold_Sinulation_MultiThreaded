"""
Utility to display racks.
"""

def display_racks(label, racks):
    print(f"--- {label} ---")
    for i, rack in enumerate(racks, start=1):
        print(f"Rack #{i}: {rack}")
    print()