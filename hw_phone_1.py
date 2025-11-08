class Car:
     def __init__(self, id):
         self.id = id
         
         #WIP
         #self.model = model
         #self.color = color
         
     def available(self):
         pass
         
     def rent(self):
         pass
         
     def unrent(self):
         pass
         
class RentalConfirmation:
    def __init__(self, user_data, car_id, date_start, date_finish):
        self.user_data = user_data
        self.car_id = car_id
        self.date_start = date_start
        self.date_finish = date_finish
        cars[car_id].rent()
        
    def generate_confirmation(self):
        pass
        
    def print_confirmation(self):
        pass
        
       
cars = []


car_id = input("Enter a car id: ")
car = Car(car_id)
cars.append(car)


if car.available:
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    address = input("Enter your address: ")
    date_start = input("Enter date start rent: ")
    date_finish = input("Enter date finish rent: ")
    user_data = (name, surname, address)
    conf1 = RentalConfirmation(user_data, int(car_id), date_start, date_finish)
    conf1.generate_confirmation()
    
    if input("Print confirmation? (y/n): ") == "y":
        conf1.print_confirmation
