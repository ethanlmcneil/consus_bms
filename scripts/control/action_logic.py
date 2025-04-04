


class ActionController:
    """
    Control logic for a single battery. Extend or configure for more advanced decision rules.
    """
    
    def __init__(self, battery_data: dict):
        self.data = battery_data
        self.identifier = battery_data.get("identifier")
        self.state_of_charge = battery_data.get("state_of_charge")
        self.temperature = battery_data.get("temperature")
        self.status = battery_data.get("status")
        self.timestamp = battery_data.get("last_seen")
        self.flag = battery_data.get("flag")
        self.power_kw = battery_data.get("power_kw")
        self.voltage = battery_data.get("voltage")
        self.location = battery_data.get("location")
        self.capacity_kwh = battery_data.get("capacity_kwh")
        self.postal_code = battery_data.get("postal_code")

        self.IP_address = battery_data.get("IP_address")
        
        # Configurable thresholds (could be passed in dynamically)
        self.min_soc = 20.0
        self.max_soc = 80.0
        self.max_temp = 45.0
        self.min_temp = 0.0

    def decide(self) -> str:
        """
        Determines the control action for the battery based on its current state.
        Returns one of: 'charge', 'discharge', 'idle', 'error'

        Should use the battery IP address to send commands to the battery.
        """
        if self.state_of_charge is None or self.temperature is None:
            return "error"
        
        if self.temperature > self.max_temp or self.temperature < self.min_temp:
            return "error"
        
        if self.state_of_charge < self.min_soc:
            return "charge"
        
        if self.state_of_charge > self.max_soc:
            return "discharge"

        return "idle"


