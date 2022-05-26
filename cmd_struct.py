import struct

# Little endian: int, float
struct_format_str = '<if'

cmd_enum = {
    'invalid_cmd'   : 0,
    'move_forward'  : 1,
    'move_bakcward' : 2,
    'rotate_right'  : 3,
    'rotate_left'   : 4,
    'rotate_around' : 5,
    'cancel'        : 6,
    'continue'      : 7
}

def pack_cmd(cmd_str, val):
    cmd = cmd_enum[cmd_str]
    return struct.pack(struct_format_str, cmd, val)

def unpack_cmd(data):
    cmd, val = struct.unpack(struct_format_str, data)
    cmd_str = list(cmd_enum.keys())[list(cmd_enum.values()).index(cmd)]
    return cmd_str, val


def main():
    # Set command
    cmd = 'invalid_cmd'
    val = 0
    if len(argv) > 1 and argv[1] in cmd_enum.keys(): cmd = argv[1]
    if len(argv) > 2: val = float(argv[2])
    
    cmd_packed = pack_cmd(cmd, val)
    print()
    print('Packed data:')
    print(cmd_packed)
    print()

    # Read back data
    read_cmd, read_val = unpack_cmd(cmd_packed)
    print(f'Command type = "{read_cmd}", float value = "{read_val}".')

if __name__ == '__main__':
    from sys import argv
    main()