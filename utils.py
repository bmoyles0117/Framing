def hex2str(val, delimiter = ':'):
    return delimiter.join([hex(ord(x))[2:].rjust(2, '0') for x in val])
