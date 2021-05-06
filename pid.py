from datetime import datetime, timedelta


class PidDuty:
    _set_point = 0.0
    _Kp = 0.0005
    _Ki = 0.005
    _Kd = 0.00005
    _integral = 0.0
    _last_error = 0.0
    _duty = 0.0

    def __init__(self):
        self.last_time = datetime.now()

    def set_point(self, new_set_point):
        self._set_point = new_set_point

    def set_duty(self, new_duty):
        self._duty = new_duty

    def set_kp(self, new_kp):
        self._Kp = new_kp

    def set_ki(self, new_ki):
        self._Ki = new_ki

    def set_kd(self, new_kd):
        self._Kd = new_kd

    def control_loop(self, measurement, time=None):
        error = self._set_point - measurement
        if time is None:
            now = datetime.now()
        else:
            now = time
        dt = (now - self.last_time) / timedelta(microseconds=1)
        self._integral = error * dt
        _p = self._Kp * error
        _i = self._Ki * self._integral
        _d = self._Kd * (error - self._last_error) / dt
        # print("Err: {:.2f} - P={:.2f} I={:.2f} D={:.2f}".format(error, _p, _i, _d))
        self._duty = max(min(_p + _i + _d, 1.0), 0.0)
        self._last_error = error
        self.last_time = now
        return self._duty
