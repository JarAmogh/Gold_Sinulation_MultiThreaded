""" 
1) Creating a rack class

2) Create rack object mannualy and putting value in it 


"""

import config 

class Rack:
    def __init__(self,capacity,quantity):

        self.capacity = float(capacity)
        self.quantity = float(quantity)


    def is_full(self):
        return self.quantity >= self.capacity
    
    def remaining_capacity(self):
        return self.capacity - self.quantity
    

    # creating a desctiption fuction to print it or keep track of things 
    def __repr__(self):
        return f"Rack(Capacity: {self.capacity}, Quantity: {round(self.quantity, 3)}, Full: {self.is_full()})"


        
"""Creating a warehouse from details i put in config file """


warehouse= Rack(config.warehouse_capacity,config.warehouse_quantity)


"""Creating racks manually"""


# IN rack configuration (15 racks)
in_config = {
    "num": 15,
    "racks": [
        Rack(10.0, 5.0),
        Rack(20.0, 10.0),
        Rack(30.0, 15.0),
        Rack(40.0, 20.0),
        Rack(50.0, 25.0),
        Rack(60.0, 10.0),
        Rack(15.0, 7.0),
        Rack(25.0, 5.0),
        Rack(35.0, 17.0),
        Rack(45.0, 12.0),
        Rack(55.0, 10.0),
        Rack(10.0, 0.0),
        Rack(75.0, 30.0),
        Rack(30.0, 15.0),
        Rack(25.0, 5.0)
    ]
}

# OUT rack configuration (15 racks)
out_config = {
    "num": 15,
    "racks": [
        Rack(12.0, 6.0),
        Rack(22.0, 12.0),
        Rack(32.0, 8.0),
        Rack(42.0, 20.0),
        Rack(52.0, 26.0),
        Rack(10.0, 5.0),
        Rack(60.0, 50.0),
        Rack(20.0, 18.0),
        Rack(30.0, 5.0),
        Rack(40.0, 25.0),
        Rack(55.0, 10.0),
        Rack(15.0, 14.0),
        Rack(35.0, 10.0),
        Rack(45.0, 20.0),
        Rack(25.0, 5.0)
    ]
}



