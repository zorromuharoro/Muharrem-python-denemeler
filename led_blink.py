import random
import time

class SensorDevice:
    def __init__(self, name):
        self.name = name
        self.readings = []
        
    def get_reading(self):
        """
        0 ile 5 Volt arasında rastgele bir okuma üretir.
        Bu, örnek olarak bir voltaj okumasıdır.
        """
        reading = random.uniform(0,5)
        self.readings.append(reading)
        return reading
    
    def print_last_reading(self, count=5):
        """
        Son 'count' kadar okuma değerini yazdırır.
        """
            
        print(f"\n{self.name} cihazının son {count} okuması:")
        for r in self.readings[-count: ]:
            print(f"{r:.2f} V")
            
def check_reading_status(reading):
    if reading < 1.0:
        return "Düşük"
    elif 1.0 <= reading < 3.0:
        return "Normal"
    else:
        return "Yüksek"

voltage_to_percentage = lambda v: (v / 5.0) * 100

def main():
    device = SensorDevice("VoltageSensor1")
    
    count = 0
    while count < 10:
        reading = device.get_reading()
        status = check_reading_status(reading)
        percentage = voltage_to_percentage(reading)
        print(f"Okuma {count+1}: {reading:.2f} V -> {status} ({percentage:.1f}%)")
        
        if status == "Düşük":
            blink_times = 1
        elif status == "Normal":
            blink_times = 3
        else:
            blink_times = 5

        print("LED blink: ", end="")
        for i in range(blink_times):
            print("*", end=" ", flush=True)
            time.sleep(0.2)
        print("\n")
        
        count += 1
    device.print_last_reading()
    
if __name__ == '__main__':
    main()
    
        