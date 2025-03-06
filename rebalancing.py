"""

Rebalace OUT racks =>  Warehouse
Rebalacen IN racks => shuffling IN rack quantity


"""

"""
Rebalance Out rack 

1) If not single out rack has gold >= required amount => take gold from warehouse
2) If out rack does not hage enough space to keep gold during buying process then can put some
    gold in warehouse 
"""



"""BIy transaction: bring gold form warehouse if no required qunatitty"""
def rebalance_out_for_gold(racks,required_amount,warehouse):

    best_rack=None
    max_quantity_under=-1

    for rack in racks:
        if rack.quantity < required_amount:
            if rack.quantity > max_quantity_under:
                max_quantity_under=rack.quantity
                best_rack=rack

    # if i cannot find the best rack

    if best_rack is None:
        return False
    

    needed=required_amount-best_rack.quantity
    if warehouse.quantity>=needed:
        warehouse.quantity-=needed
        best_rack.quantity+=needed
        return True
    else:
        return False
    
""" For selling transaction: put in warehouse to create space in out rack"""

def rebalance_out_for_capacity(racks, required_amount, warehouse):
    
    candidate=None
    max_capacity= -1

    #finding the rack with mopst reamaining capacity

    for rack in racks:
        if rack.remaining_capacity()<required_amount:
            if rack.capacity>max_capacity:
                max_capacity=rack.capacity
                candidate=rack
    # if i ccannot find any rack 

    if candidate is None:
        return False
    
    # calculatr the amount to free up from the candidate rack

    to_free=required_amount -candidate.remaining_capacity()
    if to_free <=0:
        return True
    
    # put the gold from warehosue to thr rack

    if candidate.quantity < to_free:
        to_free=candidate.quantity
    candidate.quantity -= to_free
    warehouse.quantity+=to_free


    return candidate.remaining_capacity() >=required_amount




"""
Rebalance IN rack:

1) if not a single rack has enught gold so can take gold fomr other in rack to full fill 
    requirement 

2) if not a single rack has enough reming capcity during buyinh then can craete space 
    by giving gold fomnr rack to other inrack so aquire all gold from out rack 
    

"""



"""Rebalacen in racks : selling (taking enough gold from other rack to fullfill req)"""

def rebalance_in_for_gold(racks,required_amount):
    
    best_rack =None
    max_gold_under=-1


    #find the best rackl wiht largest quantity 

    for rack in racks:
        if rack.quantity < required_amount:
            if rack.quantity > max_gold_under:
                best_rack=rack

    
    # false case if not suitable rack is found 
    if best_rack is None:
        return False
    
    #calcute shortfall 

    needed_to_gather = required_amount-best_rack.quantity

    for other in racks:
        if other is best_rack:
            continue
        
        if other.quantity<=0:
            continue
        

        can_take =other.quantity
        if can_take > needed_to_gather:
            can_take=needed_to_gather

        best_rack.quantity +=can_take
        other.quantity -= can_take
        needed_to_gather-=can_take


        if needed_to_gather <=0:
            break
        
    return best_rack.quantity>=required_amount



""" In rack: creating sapce for in rack : using readjsuting inrack"""

def rebalance_in_for_capacity(racks, required_amount):
   
    candidate = None  
    max_capacity = -1  

    #cehckign for best rack 

    for rack in racks:
        if rack.remaining_capacity() < required_amount:  
            if rack.capacity > max_capacity:  
                max_capacity = rack.capacity  
                candidate = rack 

    if candidate is None:  
        return False

    to_free = required_amount - candidate.remaining_capacity()  
    if to_free <= 0:
        return True

    for other in racks:
        if other is candidate:  
            continue
        free_space = other.remaining_capacity()  
        if free_space <= 0:  
            continue

        can_move = candidate.quantity  
        if can_move > to_free:  
            can_move = to_free  
        if can_move > free_space:  
            can_move = free_space  

        candidate.quantity -= can_move  
        other.quantity += can_move  
        to_free -= can_move  

        if to_free <= 0:   
            break

    return candidate.remaining_capacity() >= required_amount 


    





