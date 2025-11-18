import pandas as pd
import hashlib
import qrcode_terminal


df_cars = pd.read_csv("cars.csv", dtype={"id": str})

class Car:
    def __init__(self, id):
        self.id = id
        self.make = df_cars.loc[df_cars["id"] == self.id, "make"].squeeze()
        self.model = df_cars.loc[df_cars["id"] == self.id, "model"].squeeze()
        self.color = df_cars.loc[df_cars["id"] == self.id, "color"].squeeze()

    def __str__(self):
        return f'{self.make}, {self.model}, {self.color}'

    def available(self):
        available = df_cars.loc[df_cars["id"] == self.id, "available"].squeeze()
        try:
            if available == "yes":
                return True
            else:
                return False
        except ValueError:
            print("This ID is not exist!")
            exit()

    def rent(self):
        df_cars.loc[df_cars["id"] == self.id, "available"] = "no"
        df_cars.to_csv("cars.csv", index=False)


class RentalConfirmation:
    def __init__(self, user_data, car, date_start, date_finish, playlist_name=None, playlist_link=None):
        self.user_data = user_data
        self.car = car
        self.date_start = date_start
        self.date_finish = date_finish
        self.playlist_name = playlist_name
        self.playlist_link = playlist_link
        self.ticket = "The ticket has been not created yet"
        self.hash_code = self.generate_hash()
        car.rent()

    def generate_hash(self):
        data = f"{self.user_data}, {self.car}, {self.date_start}, {self.date_finish}"
        data = data.encode("utf-8")
        data_hash = hashlib.sha256(data)
        data_return = data_hash.hexdigest()
        return data_return

    def generate_confirmation(self):
        addition = ''
        if self.playlist_link:
            addition = f"""
        \n      Option "Perfect Playlist":
            "{self.playlist_name}"
            link: {self.playlist_link}"""

        self.ticket = f"""
        Thank you for your reservation.
        Here is your rent data:
        Customer: {self.user_data}.
        Car: {self.car.make} {self.car.model}, color: {self.car.color}
        
        Valid from {self.date_start} to {self.date_finish}
        
        Hash-code: {self.hash_code}
        {addition}
        """

    def print_confirmation(self):
        print(self.ticket)

class PlaylistService:
    def __init__(self):
        self.playlists = pd.read_csv("playlists.csv", dtype={"id": str})

    def return_playlist(self, id):
        self.playlist_name = self.playlists.loc[self.playlists["id"] == id, "name"].squeeze()
        self.playlist_link = self.playlists.loc[self.playlists["id"] == id, "link"].squeeze()
        return (self.playlist_name, self.playlist_link)

    def print_qrcode(self):
        qrcode_terminal.draw(self.playlist_link)


def main():
    print(df_cars, '\n')

    car_id = input("Enter a car id: ")
    car = Car(car_id)
    playlists_serv = PlaylistService()

    if car.available():
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        address = input("Enter your address: ")
        date_start = input("Enter date start rent: ")
        date_finish = input("Enter date finish rent: ")
        user_data = f"{name} {surname}, {address}"
        playlist = input("Would you like to add the 'Perfect Playlist' option? (y/n): ")
        if playlist == 'y': # я хотів злегка інакше зробити все завдання (ну тобто завдання те ж, просто інший клас і по іншому написано все), але подумав що ви докопаєтесь до цього)))  злякався))
            print(playlists_serv.playlists[['id', 'name']])
            playlist_id = input('Enter playlist id: ')
            print('Link added to confirmation\n')
            playlist_name, playlist_link = playlists_serv.return_playlist(playlist_id)
            conf1 = RentalConfirmation(user_data, car, date_start, date_finish, playlist_name, playlist_link)
        else:
            conf1 = RentalConfirmation(user_data, car, date_start, date_finish)

        conf1.generate_confirmation()
        if input("Print confirmation? (y/n): ") == "y":
            conf1.print_confirmation()
            if playlist == 'y' and input('Want to get QR-Code for playlist? (y/n): ') == 'y':
                playlists_serv.print_qrcode()
    else:
        print('Sorry, the car is not available to rent')

if __name__ == "__main__":
    main()