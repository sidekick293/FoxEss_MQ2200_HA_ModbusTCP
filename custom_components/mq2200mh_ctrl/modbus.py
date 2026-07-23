"""MQ2200MH Modbus TCP client using raw sockets. No external dependencies."""

import socket
import struct
import logging

_LOGGER = logging.getLogger(__name__)


def read_registers(host, port, address, count, device_id=1):
    """Read holding registers (function code 0x03)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        sock.connect((host, port))

        request = bytes([
            0x00, 0x01, 0x00, 0x00, 0x00, 0x06, device_id, 0x03,
            (address >> 8) & 0xFF, address & 0xFF,
            (count >> 8) & 0xFF, count & 0xFF,
        ])

        sock.send(request)
        response = sock.recv(2048)
        sock.close()

        if len(response) > 9:
            byte_count = response[8]
            data = response[9:9 + byte_count]
            return [struct.unpack('>H', data[i:i+2])[0] for i in range(0, len(data), 2)]

        return None

    except Exception as e:
        _LOGGER.warning("Modbus read %s error: %s", address, e)
        try:
            sock.close()
        except Exception:
            pass
        return None


def write_registers(host, port, address, values, device_id=1):
    """Write multiple registers (function code 0x10)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    try:
        sock.connect((host, port))

        reg_count = len(values)
        byte_count = reg_count * 2

        header = bytes([
            0x00, 0x01, 0x00, 0x00,
            ((7 + byte_count) >> 8) & 0xFF, (7 + byte_count) & 0xFF,
            device_id, 0x10,
            (address >> 8) & 0xFF, address & 0xFF,
            (reg_count >> 8) & 0xFF, reg_count & 0xFF,
            byte_count,
        ])

        payload = b''
        for v in values:
            payload += struct.pack('>H', v & 0xFFFF)

        sock.send(header + payload)
        response = sock.recv(2048)
        sock.close()

        if len(response) >= 9 and response[7] == 0x10:
            return True

        if len(response) >= 9 and response[7] == 0x90:
            _LOGGER.error("Modbus write %s exception code %s", address, response[8])

        return False

    except Exception as e:
        _LOGGER.error("Modbus write %s error: %s", address, e)
        try:
            sock.close()
        except Exception:
            pass
        return False


def combine_i32(high, low):
    """Combine 2 registers into a signed 32-bit integer."""
    value = (high << 16) | low
    if value >= 0x80000000:
        value -= 0x100000000
    return value


def combine_u32(high, low):
    """Combine 2 registers into an unsigned 32-bit integer."""
    return (high << 16) | low


def i32_to_registers(value):
    """Convert a signed 32-bit integer into 2 register values."""
    if value < 0:
        value += 0x100000000
    return [(value >> 16) & 0xFFFF, value & 0xFFFF]
