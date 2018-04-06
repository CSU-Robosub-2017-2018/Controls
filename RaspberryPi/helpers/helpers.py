import serial
import serial.tools.list_ports

def find_arduinos():
    """
    https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
    :return: ports that are registered to an arduino
    """
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduinos found")
    return arduino_ports

def find_serial_num(serial_number):
    """
    https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
    :param serial_number: number that is being looked for.
    :return: the serial port that contains the devise with the serial number.
    """
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            return serial.Serial(pinfo.device)
    raise IOError("Could not find an desired serial number - is it plugged in?")

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
