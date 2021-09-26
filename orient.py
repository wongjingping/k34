import pcbnew
import math

# constants
mx_length = 19.05
rotation_deg = 20.0
x_offset = 39.0
x_right_offset = 40
x_diode_offset = 3
x_col_step = mx_length * math.cos(rotation_deg/180*math.pi)
x_row_step = mx_length * math.sin(rotation_deg/180*math.pi)
y_offset = 40
y_diode_offset = 5
y_col_step = mx_length * math.sin(rotation_deg/180*math.pi)
y_row_step = mx_length * math.cos(rotation_deg/180*math.pi)
finger_v_offset = {
  0: 0,
  1: 10,
  2: 14,
  3: 8,
  4: 4
}
thumb_v_offset = {
  3: 0,
  4: -4
}
thumb_h_offset = {
  3: mx_length/2,
  4: mx_length/2 + 3.5,
}


# get 0-indexed col/row coordinates
def get_row_col(ref):
    start_idx = 2 if ref.startswith("MX") else 1
    num = int(ref[start_idx:])
    # split num into (d2,d1). num starts from 1
    col=(num-1)%10
    row=(num-1)//10
    if row==3:
        col += 3
    return (row,col)


# calculate position based on col/row coordinates
def calc_x_y(row, col, diode):
    # calculate initial grid position
    if col >= 5:
        x = x_offset + x_right_offset + x_col_step * col + x_row_step * row
        y = y_offset + y_col_step * (9 - col) + y_row_step * row
    else:
        x = x_offset + x_col_step * col - x_row_step * row
        y = y_offset + y_col_step * col + y_row_step * row
    # customize slant height per finger type :
    finger = col if col < 5 else 9-col
    if row < 3:
        v_steps = finger_v_offset[finger]
        h_steps = 0
    else:
        v_steps = thumb_v_offset[finger]
        h_steps = thumb_h_offset[finger]
    x += math.sin(rotation_deg/180*math.pi) * (v_steps if col < 5 else -v_steps)
    x += math.cos(rotation_deg/180*math.pi) * (h_steps if col < 5 else -h_steps)
    y -= math.cos(rotation_deg/180*math.pi) * v_steps
    y += math.sin(rotation_deg/180*math.pi) * h_steps
    if diode:
        x += x_diode_offset if col >= 5 else (-x_diode_offset)
        y += y_diode_offset
    return (x, y)

def calc_degree(col, diode):
    if row == 3:
        if col == 3:
            deg = -rotation_deg
        elif col == 4:
            deg = -40
        elif col == 5:
            deg = 40
        elif col == 6:
            deg = rotation_deg
    else:
        deg = rotation_deg if col >= 5 else -rotation_deg
    if diode:
        deg += 180 # rotate diode to be closer to col
    return deg

pcb = pcbnew.GetBoard()
for m in pcb.GetModules():
    ref = m.GetReference()
    row, col = get_row_col(ref)
    diode = ref.startswith("D")
    if ref.startswith("U"):
        x = x_offset + x_col_step * 4.5 + x_right_offset / 2
        m.SetPosition(pcbnew.wxPointMM(x, 75))
        m.SetOrientationDegrees(-90)
    else:
        x, y = calc_x_y(row, col, diode)
        deg = calc_degree(col, diode)
        m.SetPosition(pcbnew.wxPointMM(x,y))
        m.SetOrientationDegrees(deg)
        if ref.startswith("MX"):
            print("row %i col %i: x %f, y %f" % (row, col, x, y))
        elif ref.startswith("D"):
            m.Flip(pcbnew.wxPointMM(x,y))

