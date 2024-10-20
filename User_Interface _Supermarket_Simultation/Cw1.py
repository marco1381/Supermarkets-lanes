from datetime import datetime
import random
import time
import threading


# A class which represents the customers in the supermarket
class Customer:
    # I have assigned customer identifier, so we can recognise the customers in the lanes.
    customer_identifier = 1
    customers = []

    # Creates a new customer when class is called.
    def __init__(self):
        self.__basket_size = self.basket_size()
        self.__lottery_ticket = self.generate_lottery_ticket()
        self.identifier = Customer.customer_identifier
        Customer.customer_identifier += 1
        Customer.customers.append(self)

    # This function generates a basket size randomly between 1 and 30.
    def basket_size(self):
        self.__basket_size = random.randint(1, 30)
        return self.__basket_size

    # Generates lottery ticket if basket size is greater than 10, has a chance of 1 in 30.
    def generate_lottery_ticket(self):
        return self.__basket_size > 10 and random.randint(1, 30) == 1

    # This function assigns the checkout times according to the lane type. Checks out customer in that time.
    # Then displays the checkout information accordingly.
    def checkout(self, lane_type, customer_identifier):
        start_time = time.time()  # Record the start time of checkout

        if lane_type == "Regular":
            checkout_time = 4 * self.__basket_size
            time.sleep(checkout_time)
        elif lane_type == "SelfService":
            checkout_time = 6 * self.__basket_size
            time.sleep(checkout_time)

        end_time = time.time()  # Record the end time of checkout
        actual_checkout_time = end_time - start_time

        if lane_type == "Regular":
            print(f"\n[Regular Lane] | Customer {self.identifier} with basket size {self.__basket_size} CHECKED OUT in"
                  f" {actual_checkout_time:.2f} seconds.")
        elif lane_type == "SelfService":
            print(
                f"\n[Self Service Lane] | Customer {self.identifier} with basket size {self.__basket_size} CHECKED OUT in"
                f" {actual_checkout_time:.2f} seconds.")

        if self.__lottery_ticket:
            print(f"CONGRATULATIONS! Customer {self.identifier} you have won the lottery!")

        return self.identifier  # Return the identifier of the checked-out customer

    # Displays customer details including basket size and lottery win
    def customer_details(self):
        print(f"Basket: {self.__basket_size} items{' - Lottery Winner!' if self.__lottery_ticket else ' '}")

    # Return a string containing the customer identifier
    def __str__(self):
        return f"{self.identifier}"


# This class represents the lanes in the supermarket.
class Lanes:
    def __init__(self, lane_type, lane_capacity, lane_number):
        self.lane_type = lane_type
        self.lane_capacity = lane_capacity
        self.lane_status = "Closed"
        self.timestamp = datetime.now()
        self.lane_number = lane_number
        self.customers = []

    # This function sets the lane status to open
    def lane_open(self):
        self.lane_status = "Open"
        return self.lane_status

    # This function sets the lane status to closed
    def lane_closed(self):
        self.lane_status = "Closed"
        return self.lane_status

    # This function adds customer to the lane.
    def lane_add_customer(self, customer):
        self.customers.append(customer)

    # This function removes customer from the lane.
    def lane_remove_customer(self, lane_type, customer_identifier=None):
        if lane_type == "Regular":
            if not self.empty_lane():
                self.customers.pop(0)
        elif lane_type == "SelfService" and customer_identifier is not None:
            for customer in self.customers:
                if customer.identifier == customer_identifier:
                    self.customers.remove(customer)
                    break

    # Checks if the lane is full
    def lane_full(self):
        return len(self.customers) >= self.lane_capacity

    # Checks if the lane is empty
    def empty_lane(self):
        return len(self.customers) == 0

    # Displays the lane status
    def show_lane_status(self):
        customers_str = ' '.join(str(customer) for customer in self.customers)
        status = f"{self.lane_type} | ({self.lane_number}) | {self.lane_status} | Customers In Lane ==> {customers_str}"
        return status


# These two classes are using inheritance from class lanes. These classes assign the properties of the lanes to them.
class RegularLane(Lanes):
    def __init__(self, lane_number):
        super().__init__("Regular Lane", lane_capacity=5, lane_number=lane_number)


class SelfServiceLane(Lanes):
    def __init__(self, lane_number):
        super().__init__("Self Service Lane", lane_capacity=15, lane_number=lane_number)


# Assigning names to all the lanes required.
regular_lanes = [RegularLane(i) for i in range(1, 6)]
ss1 = SelfServiceLane(1)


# This class Manages the opening, closing, and assignment of customers to check out lanes.
class LaneManager:
    def __init__(self, regular_lane, self_service_lane):
        self.regular_lane = regular_lane
        self.self_service_lane = self_service_lane
        self.simulation_start_time = datetime.now()

    # Closes empty regular lanes and self-service lane
    def close_lanes(self):
        for regular_lane in self.regular_lane:
            if regular_lane.empty_lane() and regular_lane.lane_status == "Open":
                regular_lane.lane_closed()

        if ss1.empty_lane() and ss1.lane_status == "Open":
            ss1.lane_closed()

    # Opens regular lanes and self-service lane according to availability and capacity
    def open_lanes(self):
        self.regular_lane[0].lane_open()  # Sets regular lane 1 to open at start
        ss1.lane_open()  # Sets Self Service lane 1 to open at start
        lanes = regular_lanes  # placed al regular lanes in list to manage it easily.

        # Assigning i to assign current lane and previous lane
        for i in range(0, len(lanes)):
            current_lane = lanes[i]
            previous_lane = lanes[i - 1]

            #  opens new lanes if the lane is full and the next lane is closed.
            if not current_lane.lane_full() and current_lane.lane_status == "Open":
                current_lane.lane_open()
            elif previous_lane.lane_full() and current_lane.lane_status == "Closed":
                current_lane.lane_open()
            if self.regular_lane[-1].lane_full() and self.regular_lane[-1].lane_status == "Open":
                print(f" {Customer.customer_identifier} All Regular Lanes are FULL. Please wait!")
            if ss1.lane_full():
                print(f" {Customer.customer_identifier} Self Service Lane is FULL. Please wait or move to Regular Lane")

    # Assigns the customers to the lanes according to their basket size and lane availability.
    def assign_customer_to_lane(self, customer):
        if customer.basket_size() < 10:
            # Assign to self-service lane if basket size is less than 10
            if not self.self_service_lane.lane_full():
                self.self_service_lane.lane_add_customer(customer)
            elif self.self_service_lane.lane_full():
                self.assign_to_regular_lane(customer)
        else:
            # Assign to regular lane if basket size is 10 or more
            self.assign_to_regular_lane(customer)

    # Assigns the customer to the first available regular lane
    def assign_to_regular_lane(self, customer):
        for lane in self.regular_lane:
            if not lane.lane_full() and lane.lane_status == "Open":
                lane.lane_add_customer(customer)
                break

    def simulate_checkout(self):
        checkout_threads = []

        # Simulate checkout for regular lanes
        for lane in self.regular_lane:
            if not lane.empty_lane():
                customer_to_checkout = lane.customers[0]
                checkout_thread = threading.Thread(target=self.checkout_and_remove,
                                                   args=("Regular", customer_to_checkout))
                checkout_threads.append(checkout_thread)
                checkout_thread.start()

        # Simulate checkout for self-service lane
        if not self.self_service_lane.empty_lane():
            customers_to_checkout = self.self_service_lane.customers[:]

            # Start threads for each customer in the self-service lane
            for customer_to_checkout in customers_to_checkout:
                checkout_thread = threading.Thread(target=self.checkout_and_remove,
                                                   args=("SelfService", customer_to_checkout))
                checkout_threads.append(checkout_thread)
                checkout_thread.start()

        # Wait for all threads to finish
        for thread in checkout_threads:
            thread.join()

    # Simulates the checkout process and removes the customer from the lane
    def checkout_and_remove(self, lane_type, customer):
        customer_identifier = customer.checkout(lane_type, customer.identifier)

        if lane_type == "Regular":
            for lane in self.regular_lane:
                if not lane.empty_lane() and lane.customers[0].identifier == customer_identifier:
                    lane.lane_remove_customer("Regular", customer_identifier)
                    break
        elif lane_type == "SelfService":
            if len(self.self_service_lane.customers) <= 15:
                self.self_service_lane.lane_remove_customer("SelfService", customer_identifier)

    # Displays the time since simulation started
    def display_simulation_time(self):
        time_passed = datetime.now() - self.simulation_start_time
        str_time = str(time_passed).split(".")[0]  # Format the elapsed time
        return str_time

    # This function displays the whole status menu
    def display_status(self):
        current_time = self.display_simulation_time()

        # Calculate the total number of customers in all lanes
        total_customers = sum(len(lane.customers) for lane in self.regular_lane) + len(self.self_service_lane.customers)

        print(f"\n **** Current Lane Status | Elapsed Time: {current_time} | Total Customers: {total_customers} ****")
        print("---------------------------------------------------------------------------------")
        for lane in self.regular_lane:
            print(lane.show_lane_status())
        print(ss1.show_lane_status())


# This class will bring all classes together and run the simulation.
class SupermarketSimulation:
    def __init__(self, lane_manager):
        self.lane_manager = lane_manager
        self.customers = []

    def assign_to_lane(self, customer):
        # Assigns a customer to a checkout lane
        self.lane_manager.assign_customer_to_lane(customer)

    def close_lanes(self):
        # Close lanes
        self.lane_manager.close_lanes()

    def simulate_checkout(self):
        # Simulates the checkout process
        self.lane_manager.simulate_checkout()

    # Generates a random number of customers and assigns them to check out lanes
    def generate_random_customers(self):
        num_customers = random.randint(1, 10)
        for i in range(num_customers):
            new_customer = Customer()
            self.assign_to_lane(new_customer)

    # The bottom two function are created to keep the customers getting generated while checkout is taking place.
    def generate_customers_periodically(self, interval, total_simulation_duration):
        start_time = time.time()
        while time.time() - start_time < total_simulation_duration:
            time.sleep(interval)
            self.generate_random_customers()

    def run_generate_customers_thread(self, interval, total_simulation_duration):
        generate_customers_thread = threading.Thread(
            target=self.generate_customers_periodically, args=(interval, total_simulation_duration)
        )
        generate_customers_thread.start()

    # This function runs all the function in the simulation class in order and simulates the supermarket.
    # Added stop event for the GUI simulation
    def run_simulation(self, total_simulation_duration, customer_generation_duration, display_status_interval,
                       stop_event):
        start_time = time.time()
        current_time = start_time

        try:
            self.lane_manager.open_lanes()
            self.generate_random_customers()

            while current_time - start_time < total_simulation_duration:
                if stop_event.is_set():  # Check if the stop_event is set
                    print("\nThe simulation stopped!")
                    break
                if current_time - start_time < customer_generation_duration:
                    # Generate customers every 30 seconds
                    self.run_generate_customers_thread(30, customer_generation_duration)
                    self.lane_manager.open_lanes()
                else:
                    # Display status
                    self.lane_manager.display_status()

                    # Close lanes in a separate thread
                    checkout_thread = threading.Thread(target=self.close_lanes)
                    checkout_thread.start()

                    # Sleep for the specified interval before checking the status again
                    time.sleep(display_status_interval)

                # Display status
                self.lane_manager.display_status()

                # Simulate checkout
                checkout = threading.Thread(target=self.simulate_checkout)
                checkout.start()
                checkout.join()

                time.sleep(display_status_interval)
                current_time = time.time()

        except KeyboardInterrupt:
            print("\nSimulation has been Interrupted, Exiting")
        finally:
            # Clear the event and continue the simulation
            stop_event.clear()

