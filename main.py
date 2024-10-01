def get_rcl(r_meas, a, b, c, d):
    rcl = a * r_meas + b

    return rcl


def get_rcp(r_meas, a, b, c, d):
    rcp = a * r_meas ** 3 + b * r_meas ** 2 + c * r_meas + d

    return rcp


def criteria():
    mpe_plus_u = 0.0867
    mpe_pol = 0.3

    if abs(mpe_plus_u) < abs(mpe_pol):
        return True
    else:
        return False