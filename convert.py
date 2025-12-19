import serial
import time
import sys


SERIAL_PORT = 'COM12'   # พอร์ต
BAUD_RATE = 113000      # ความเร็ว


def invert_byte(byte_val):
    """ฟังก์ชันกลับบิต (Software Invert) 0->1, 1->0"""
    return ~byte_val & 0xFF

try:
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.1
    )
    
    print(f"[-] Connected to {SERIAL_PORT} @ {BAUD_RATE}")
    print("[-] Waiting for data... (Press Ctrl+C to exit)")
    print("==============================================")

    while True:
        if ser.in_waiting > 0:
            raw_data = ser.read(ser.in_waiting)
            
            decoded_text = ""
            for byte in raw_data:
                inverted_byte = invert_byte(byte)
                if 32 <= inverted_byte <= 126 or inverted_byte in [10, 13]:
                    decoded_text += chr(inverted_byte)
                else:
                    decoded_text += "." 
            sys.stdout.write(decoded_text)
            sys.stdout.flush()
            
        time.sleep(0.01)

except serial.SerialException as e:
    print(f"\n[!] Error: Could not open port {SERIAL_PORT}. Make sure PuTTY is CLOSED.")
except KeyboardInterrupt:
    print("\n[-] Exiting...")
    if 'ser' in locals() and ser.is_open:
        ser.close()