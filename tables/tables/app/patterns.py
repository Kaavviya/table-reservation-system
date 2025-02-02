available_seats = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29', 'c30', 'c31', 'c32']
reserved_seat = []
client_history = {}
client_details = {}

import json
def serialize(file_name,obj):
    with open(file_name,'w') as f:
        json.dump(obj,f)
        print('Serialization successful')

serialize('availableSeat.json',available_seats)
serialize('reservedSeat.json',reserved_seat)

## STATE PATTERN

from abc import ABC,abstractmethod
class State(ABC):
    @abstractmethod
    def reserve_seat(self):
        pass

    @abstractmethod
    def return_seat(self):
        pass


class Availale(State):
    global reserved_seat

    def reserve_seat(self, details, seat_number):
        seats_taken = available_seats[:seat_number]
        if details in client_details:
            already_book = client_details[details]
            already_book.extend(seats_taken)
            client_details[details] = already_book
        else:
            client_details[details] = seats_taken
        reserved_seat.extend(seats_taken)
        print('available',reserved_seat)
        del available_seats[:seat_number]
        serialize('reservedSeat.json',reserved_seat)
        serialize('availableSeat.json',available_seats)
        return self 

    def return_seat(self, client_detail):
        return Reserved() 


class Reserved(State):
    def reserve_seat(self, details, seat_number):
        return self 

    def return_seat(self, detail):
        global available_seats
        global reserved_seat
        detail = tuple(detail)

        if detail in client_details:
            result = list(client_details[detail])
            client_history[detail] = result
            reserved_seat[:] = [x for x in reserved_seat if x not in result]
            print('reserved',reserved_seat)
            del client_details[detail]
            available_seats.extend(result)

        else:
            print('no detail')

        available_seats = sorted(available_seats, key=lambda x: int(x[1:]))
        serialize('reservedSeat.json',reserved_seat)
        serialize('availableSeat.json',available_seats)
        return Availale()


# OBSERVER PATTERN

class Observer:
    def update(self, event):
        pass

class UserObserver(Observer):
    def __init__(self):
        self.notification = []

    def update(self, event):
        self.notification.append(event)

class ManagerObserver(Observer):
    def __init__(self):
        self.notification = []            

    def update(self, event):
        self.notification.append(event)

class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.update(event)



# SINGLETON PATTERN FOR MANAGER
    
   
class ManagerSingleton(ManagerObserver):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def update_payment(self, client_detail, payment_done, table):
        table.current_state = Reserved()
        if client_detail in client_details:
            if payment_done:
                table.return_seat(client_detail)
                notification = PaymentDoneNotification()
                table.observer.notify_observers(notification.style_notification(f'{client_detail[0].upper()} payment done successfully'))

    def get_manager_notifications(self, table):
        return table.observer.observers[0].notification
    
    def get_client_history(self):
        return client_history

#DECORATOR PATTERN
    
class NotificationDecorator(ABC):
    @abstractmethod
    def style_notification(self,msg):
        pass

class RserervedNotification(NotificationDecorator):
    def style_notification(self,msg):
        return f"🪑 {msg} 🪑"
    

class PaymentDoneNotification(NotificationDecorator):
    def style_notification(self,msg):
        return f"✔️ {msg} ✔️"
    
class RserervedCancelledNotification(NotificationDecorator):
    def style_notification(self,msg):
        return f"❌ {msg} ❌"
    
class PaymentModeNotification(NotificationDecorator):
    def style_notification(self, msg):
        return f"💵 {msg} 💵"
    
notification = RserervedNotification()

#COMMAND PATTERN
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandInvoker:
    def __init__(self):
        self.commands = []

    def execute_command(self, command):
        command.execute()
        self.commands.append(command)

class ReserveSeatCommand(Command):
    def __init__(self, table, details, num_seats):
        self.table = table
        self.details = details
        self.num_seats = num_seats

    def execute(self):
        self.table.reserve_seat(self.details, self.num_seats)

class CancelReservationCommand(Command):
    def __init__(self, table, details):
        self.table = table
        self.details = details

    def execute(self):
        self.table.return_seat(self.details)

# STRATEGY PATTERN
class Payment:
    def __init__(self, user_detail, price, payment_mode=None):
        self.price = price
        self.payment_mode = payment_mode
        self.user_detail = user_detail
        self.notification = PaymentModeNotification()

        self.payment_strategy = self.get_payment_strategy(payment_mode)

    def get_payment_strategy(self, payment_mode):
        if payment_mode == 'UPI':
            return UPIPaymentStrategy()
        elif payment_mode == 'card':
            return CardPaymentStrategy()
        elif payment_mode == 'cash':
            return CashPaymentStrategy()

    def push_notification(self):
        if self.payment_strategy:
            self.payment_strategy.apply_strategy(self)
        return self.notification.style_notification(f"{self.user_detail.upper()} requested to pay his bill in {self.payment_mode}")

class PaymentModeStrategy:
    def apply_strategy(self, payment):
        pass

class UPIPaymentStrategy(PaymentModeStrategy):
    def apply_strategy(self, payment):
        payment.payment_mode = 'UPI'

class CardPaymentStrategy(PaymentModeStrategy):
    def apply_strategy(self, payment):
        payment.payment_mode = 'card'

class CashPaymentStrategy(PaymentModeStrategy):
    def apply_strategy(self, payment):
        payment.payment_mode = 'cash'


# Main class 
class Table:
    def __init__(self):
        self.current_state = Availale()
        self.observer = Observable()

    def reserve_seat(self, details, seat_number):
        self.current_state = self.current_state.reserve_seat(details, seat_number)
        self.observer.notify_observers(notification.style_notification(f"{details[0].upper()} your seats reserved successfully"))

    def return_seat(self,detail):
        self.current_state = self.current_state.return_seat(detail)



table = Table()
invoker = CommandInvoker()

user_observer = UserObserver()

table.observer.add_observer(user_observer)
