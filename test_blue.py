import win32com.client
import time

shutter_address_1 = "ff:ff:bb:0c:fc:87"
shutter_address_2 = "3c:58:c2:da:7b:bc"


def create_bluetooth_connection():
    try:
        # Use the MS Bluetooth API
        bt = win32com.client.Dispatch("Bluetooth.BluetoothClient")
        return bt
    except Exception as e:
        print(f"Error: {e}")
        return None


"""def find_bluetooth_devices():
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  Address: {}, Name: {}".format(addr, name))


def service_finder():
    # Perform service discovery
    services = bluetooth.find_service(address=shutter_address_1)

    if len(services) == 0:
        print(f"No services found on device {shutter_address_1}")
    else:
        print(f"Found {len(services)} services on device {shutter_address_1}")
        for service in services:
            print(f"Service Name: {service['name']}")
            print(f"    Host:        {service['host']}")
            print(f"    Description: {service['description']}")
            print(f"    Provided By: {service['provider']}")
            print(f"    Protocol:    {service['protocol']}")
            print(f"    Channel/Port: {service['port']}")
            print(f"    Service Classes: {service['service-classes']}")
            print(f"    Profiles: {service['profiles']}")
            print()


def connect():
    # Create a Bluetooth socket
    try:
        # Create a Bluetooth socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1
        sock.connect((shutter_address_1, port))
        print(f"Connected to {shutter_address_1} on port {port}.")

        while True:
            # Listen for data from the device
            data = sock.recv(1024)  # Buffer size of 1024 bytes
            if data:
                print(f"Received: {data.decode('utf-8')}")

    except bluetooth.btcommon.BluetoothError as e:
        print(f"Bluetooth error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()"""


def listen_to_bluetooth_data(bt):
    print("Listening for data...")
    while True:
        # Wait for data from the connected Bluetooth device
        if bt.IsConnected:
            data = bt.ReadData()  # Modify this based on your specific data reading method
            if data:
                print(f"Received: {data}")
        time.sleep(1)


if __name__ == '__main__':
    bt = create_bluetooth_connection()
    if bt:
        listen_to_bluetooth_data(bt)
