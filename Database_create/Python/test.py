from shift import shift
from private import private

if __name__ == '__main__':
    s = shift(shift_name='Shift test', start_time='10:00', end_time='11:30')
    s.print_shift()
    p = private(shift_name='Private test', start_time='9:00', end_time='10:00')
    p.print_shift()
