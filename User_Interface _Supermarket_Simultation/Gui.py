from Cw1 import *
from tkinter import Tk, ttk
from threading import Thread, Event
import os


# Create a panel control for the simulation
class SimulationControl:
    def __init__(self, simulation):
        self.simulation = simulation
        self.stop_event = Event()  # Event to signal the simulation thread to stop

        self.gui = Tk()
        self.gui.title("Supermarket Simulation Control Panel")  # Set the title
        self.gui.configure(bg="#FDFFEF")  # Set background color

        self.gui.geometry("660x80")

        # Create the start button to start the simulation
        start_button = ttk.Button(self.gui, text="Start Simulation", command=self.gui_start_simulation, style="TButton")
        start_button.grid(row=0, column=0, pady=12, padx=12)

        # Create the display button to display the status
        display_status_button = ttk.Button(self.gui, text="Display Status", command=self.gui_display_status,
                                           style="TButton")
        display_status_button.grid(row=0, column=1, pady=12, padx=12)

        # Create a stop simulation button to stop the simulation
        stop_button = ttk.Button(self.gui, text="Stop Simulation", command=self.gui_stop_simulation, style="TButton")
        stop_button.grid(row=0, column=2, pady=12, padx=12)

        # Create a button to exit the simulation
        exit_button = ttk.Button(self.gui, text="Exit", command=self.gui_exit_simulation, style="TButton")
        exit_button.grid(row=0, column=3, pady=12, padx=12)

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=10, background="#9FE6FF", borderwidth=5,
                        font=("Arial", 12, "bold"))

        # Change text color when the cursor is on it
        style.map("TButton", foreground=[("active", "#B8B8B8"), ("pressed", "white")], background=[("active",
                                                                                                    "#93A5FF"),
                                                                                                   ("pressed", "black")])

    # Start the simulation
    def gui_start_simulation(self):
        total_simulation_duration = 300  # Total duration of the simulation
        customer_generation_duration = 60  # Duration of customers generation
        display_status_interval = 30  # Interval between the displayed status

        # Run simulation in a separate thread
        simulation_thread = Thread(target=self.simulation.run_simulation, args=(
        total_simulation_duration, customer_generation_duration, display_status_interval, self.stop_event))
        simulation_thread.start()

    # Display the status
    def gui_display_status(self):
        self.simulation.lane_manager.display_status()

    # Stop the simulation
    def gui_stop_simulation(self):
        # Set the stop_event to signal the simulation thread to stop
        self.stop_event.set()
        print("\nThe simulation will stop in few seconds, after the first costumers checked out")

    # Exit the application
    def gui_exit_simulation(self):
        # Set the stop_event to signal the simulation thread to stop
        os._exit(0)
        self.gui.destroy()
        print("\nExiting..")


# Keep the simulation running
if __name__ == "__main__":
    try:
        regular_lane = regular_lanes
        self_service_lane = ss1
        lane_manager = LaneManager(regular_lane, self_service_lane)

        simulation = SupermarketSimulation(lane_manager)

        simulation_control = SimulationControl(simulation)
        simulation_control.gui.mainloop()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Stopping simulation...")