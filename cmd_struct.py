import struct

# Little endian: int, float, int
struct_format_str = '<ifi'

cmd_enum = {
    'invalid_cmd'   : 0,
    'move_forward'  : 1,
    'move_backward' : 2,
    'rotate_right'  : 3,
    'rotate_left'   : 4,
    'rotate_around' : 5,
    'cancel'        : 6,
    'continue'      : 7
}

speed_enum = {
    'invalid_speed'   : 0,
    'slow_speed'      : 1,
    'medium_speed'    : 2,
    'fast_speed'      : 3,
    'no_speed_update' : 4
}

def pack_cmd(cmd_str, val=0.0, speed_str='no_speed_update'):
    cmd = cmd_enum[cmd_str]
    speed = speed_enum[speed_str]
    return struct.pack(struct_format_str, cmd, val, speed)

def unpack_cmd(data):
    cmd, val, spd = struct.unpack(struct_format_str, data)
    cmd_str = list(cmd_enum.keys())[list(cmd_enum.values()).index(cmd)]
    spd_str = list(speed_enum.keys())[list(speed_enum.values()).index(spd)]
    return cmd_str, val, spd_str


def main():
    # Set command
    cmd = 'invalid_cmd'
    val = 0
    speed = 'no_speed_update'
    if len(argv) > 1 and argv[1] in cmd_enum.keys(): cmd = argv[1]
    if len(argv) > 2: val = float(argv[2])
    if len(argv) > 3 and argv[3] in speed_enum.keys(): speed = argv[3]

    cmd_packed = pack_cmd(cmd, val, speed)
    print()
    print('Packed data:')
    print(cmd_packed)
    print()

    # Read back data
    read_cmd, read_val, read_speed = unpack_cmd(cmd_packed)
    print(f'Command type = "{read_cmd}", float value = "{read_val}", speed = "{read_speed}".')

if __name__ == '__main__':
    from sys import argv
    main()