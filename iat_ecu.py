import time, random

BASE_PULSE_MS, IDEAL_IAT_C, CORR_FACTOR_10C = 2.5, 20.0, 0.03

class IATSensor:
    def __init__(self, temp=25.0): self.temp = temp
    def read(self):
        self.temp += random.uniform(-0.2, 0.2)
        self.temp = max(-10, min(90, self.temp))
        return self.temp
class ECU:
    def __init__(self, base_ms, ideal_iat, corr_factor):
        self.base, self.ideal_iat, self.corr = base_ms, ideal_iat, corr_factor
        self.history = []
    def calc_pulse(self, current_iat):
        diff = current_iat - self.ideal_iat
        correction = 1.0 + ((-diff / 10.00) * self.corr)
        correction = max(0.6, min(1.4, correction))
            
        final_pulse = self.base * correction
        final_pulse = max(0.8, min(1.4, correction))
            
        self.history.append(round(final_pulse, 3))
        print(f"  IAT:{current_iat:5.1f}°C -> Düzeltme:{correction:5.3f}x -> Enj.Süre:{final_pulse:5.3f}ms")
        return final_pulse
    
def log_call(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    print("--- IAT & Enjektör Sim (Kompakt) ---")
    iat_sensor = IATSensor(temp=15.0)
    ecu_sim = ECU(BASE_PULSE_MS, IDEAL_IAT_C, CORR_FACTOR_10C)
    
    print(f"Temel Enj.Süresi: {ecu_sim.base}ms, İdeal IAT: {ecu_sim.ideal_iat}°C\n")
    
    for step in range(6):
        print(f"Adım {step+1}:")
        temp_now = iat_sensor.read()
        final_time = ecu_sim.calc_pulse(temp_now)
        
        if step == 2: iat_sensor.temp = 40.0
        time.sleep(0.3)
        
    print("\n--- Sim Bitti ---")
    if ecu_sim.history:
        long_pulses = [p for p in ecu_sim.history if p > BASE_PULSE_MS * 1.05]
        short_pulses = [p for p in ecu_sim.history if p < BASE_PULSE_MS * 0.95]
        
        print(f"Uzun Atımlar (> {BASE_PULSE_MS*1.05:.2f}ms): {long_pulses or 'Yok'}")
        print(f"Kısa Atımlar (< {BASE_PULSE_MS*0.95:.2f}ms): {short_pulses or 'Yok'}")

        print(f"Tüm Kayıtlı Süreler: {ecu_sim.history}")
    
            