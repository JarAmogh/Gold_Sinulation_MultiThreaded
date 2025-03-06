"""

 Selection logic (Source rack selectio algorithm) 

 min remaining capacity 
 1) select rack greater that have gold greater than required gold
 2) amoght those rack choose min remaining capacity

"""

def select_source_rack(racks,required_amount):

    participant=None
    min_ramaining=None

    for rack in racks:
        if rack.quantity >= required_amount:
            remaining_after=rack.quantity-required_amount
            
            if min_ramaining is None or remaining_after < min_ramaining:
                min_ramaining=remaining_after
                participant=rack
    
    
    return participant

""" Destination rack selection algoritm 
    logic : max remaining capacity
    1) pick the rack with enough space for required gold
    2) then in those rack select the rack wiht most remaining capacity

"""

def select_destination_rack(racks,required_amount):

    participant =None
    max_remaining_capacity= None

    for rack in racks:
        if rack.remaining_capacity()>=required_amount:

            remaining_cap_after=rack.capacity-(rack.quantity + required_amount)
            if max_remaining_capacity is None or remaining_cap_after>max_remaining_capacity:
                max_remaining_capacity=remaining_cap_after
                participant=rack

    return participant






    
