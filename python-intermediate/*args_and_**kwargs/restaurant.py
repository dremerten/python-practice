import random
from datetime import datetime, timedelta

class Guest:
    _party_counter = 1

    def __init__(self, first_name, last_name, party_size=1, vip_status=False, credit_card=None):
        self.first_name = first_name
        self.last_name = last_name
        self.party_size = party_size
        self.vip_status = vip_status
        self.orders = {'food': [], 'drinks': []}
        self.bar_tab = {'drinks': []}
        self.total = 0
        self.arrived_at_bar = False
        self.arrival_time = None
        self.party_number = Guest._party_counter
        Guest._party_counter += 1
        self.credit_card = credit_card if credit_card else self._generate_random_credit_card()

    def _generate_random_credit_card(self):
        number = '-'.join([str(random.randint(1000, 9999)) for _ in range(4)])
        exp_month = str(random.randint(1, 12)).zfill(2)
        exp_year = str(random.randint(datetime.now().year % 100, (datetime.now().year + 5) % 100)).zfill(2)
        security_code = str(random.randint(100, 999))
        return {'number': number, 'expiration': f"{exp_month}/{exp_year}", 'security_code': security_code}

    def add_order(self, category, item, price=0, at_bar=False):
        if at_bar and category == 'drinks':
            self.bar_tab['drinks'].append((item, price))
            self.arrived_at_bar = True
            print(f"Added {item} (${price}) to {self.last_name} party's bar tab.")
        else:
            self.orders[category].append(item)
            self.total += price
            print(f"Added {item} (${price}) to {self.last_name} party's table order.")

    def remove_order(self, category, item, price=0, at_bar=False):
        target = self.bar_tab if at_bar and category == 'drinks' else self.orders
        if category in target:
            if at_bar:
                target[category] = [x for x in target[category] if x[0] != item]
            else:
                if item in target[category]:
                    target[category].remove(item)
                    self.total -= price
            print(f"Removed {item} from {self.last_name} party's {'bar' if at_bar else 'table'} order.")
        else:
            print(f"{item} not found in {self.last_name} party's {'bar' if at_bar else 'table'} order.")

    def transfer_bar_tab_to_table(self):
        for item, price in self.bar_tab['drinks']:
            self.orders['drinks'].append(item)
            self.total += price
        self.bar_tab = {'drinks': []}
        print(f"Transferred bar tab to {self.last_name} party's table. Total is now ${self.total}.")

    def charge_credit_card(self, amount):
        masked_card = f"****-****-****-{self.credit_card['number'][-4:]}"
        print(f"Charged ${amount} to {self.last_name}'s card ({masked_card}) on file.")

class Restaurant:
    def __init__(self, num_tables=7, bar_seats=20):
        self.tables = {i: None for i in range(1, num_tables + 1)}
        self.bar_capacity = bar_seats
        self.bar_seated = []
        self.reservation_queue = []

    def make_reservation(self, guest_instance, table_number, reservation_datetime_str):
        reservation_datetime = datetime.strptime(reservation_datetime_str, "%Y-%m-%d %H:%M")
        self.reservation_queue.append({
            'guest': guest_instance,
            'table_number': table_number,
            'reservation_time': reservation_datetime
        })
        print(f"Reservation made for {guest_instance.last_name} at table {table_number} on {reservation_datetime.strftime('%Y-%m-%d %H:%M')}")

    def assign_table(self, table_number, guest_instance, reservation_time=None, arrival_time=None):
        if arrival_time is None:
            arrival_time = datetime.now().replace(microsecond=0)
        guest_instance.arrival_time = arrival_time
        if isinstance(reservation_time, str):
            reservation_time = datetime.strptime(reservation_time, "%Y-%m-%d %H:%M")
        if reservation_time:
            early_limit = reservation_time - timedelta(minutes=10)
            late_limit = reservation_time + timedelta(minutes=10)
            if early_limit <= arrival_time < reservation_time:
                if sum(g.party_size for g in self.bar_seated) + guest_instance.party_size <= self.bar_capacity:
                    self.bar_seated.append(guest_instance)
                    guest_instance.arrived_at_bar = True
                    seats_left = self.bar_capacity - sum(g.party_size for g in self.bar_seated)
                    print(f"{guest_instance.last_name} party of {guest_instance.party_size} arrived early. Seated at the bar (Seats left: {seats_left})")
                    return
                else:
                    print("Bar is full. Cannot seat early arrival at bar.")
            elif reservation_time <= arrival_time <= late_limit:
                self._seat_guest_at_table(table_number, guest_instance, arrival_time)
                return
            else:
                guest_instance.charge_credit_card(100)
                print(f"{guest_instance.last_name} party is too late. Reservation forfeited.")
                return
        self._seat_guest_at_table(table_number, guest_instance, arrival_time)

    def _seat_guest_at_table(self, table_number, guest_instance, arrival_time):
        if guest_instance in self.bar_seated:
            guest_instance.transfer_bar_tab_to_table()
            self.bar_seated.remove(guest_instance)
        self.tables[table_number] = {
            'guest': guest_instance,
            'arrival_time': arrival_time,
            'end_time': arrival_time + timedelta(hours=3)
        }
        print(f"{guest_instance.last_name} party seated at table {table_number}.")

    def search_guest(self, last_name):
        for guest in self.bar_seated:
            if guest.last_name.lower() == last_name.lower():
                self._print_guest_info(guest, at_bar=True)
                return
        for table_num, table in self.tables.items():
            if table and table['guest'].last_name.lower() == last_name.lower():
                self._print_guest_info(table['guest'], table_num)
                return
        print(f"No guest found with last name '{last_name}'.")

    def _print_guest_info(self, guest, table_num=None, at_bar=False):
        print(f"--- Guest Info: Party #{guest.party_number} - {guest.first_name} {guest.last_name} ---")
        print(f"Party Size: {guest.party_size}")
        masked_card = f"****-****-****-{guest.credit_card['number'][-4:]}"
        print(f"Credit Card: {masked_card}, Exp: {guest.credit_card['expiration']}")
        if at_bar:
            print("Currently at the bar. Table not yet assigned.")
        else:
            print(f"Table: {table_num}")
            remaining_time = guest.arrival_time + timedelta(hours=3) - datetime.now()
            remaining_seconds = max(int(remaining_time.total_seconds()), 0)
            hours, remainder = divmod(remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            parts = []
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
            print(f"Time remaining at table: {', '.join(parts)}")
        print(f"Arrived at bar first? {'Yes' if guest.arrived_at_bar else 'No'}")
        print(f"Food Ordered: {guest.orders['food']}")
        print(f"Drinks Ordered: {guest.orders['drinks']}")
        print(f"Total Bill Owed: ${guest.total}")
        print("--------------------------------------------")

if __name__ == "__main__":
    jones_party = Guest("Bradley", "Nowell", party_size=10, vip_status=True)
    restaurant = Restaurant(bar_seats=20)
    reservation_dt = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
    restaurant.make_reservation(jones_party, table_number=7, reservation_datetime_str=reservation_dt)
    arrival_time = datetime.now().replace(microsecond=0)
    restaurant.assign_table(7, jones_party, reservation_time=reservation_dt, arrival_time=arrival_time)
    jones_party.add_order('drinks', 'Cocktail', 12, at_bar=True)
    restaurant.assign_table(7, jones_party, arrival_time=datetime.now().replace(microsecond=0))
    restaurant.search_guest("Jones")