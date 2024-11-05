import numpy as np

class KalmanFilter1D:
    def __init__(self, initial_state=0, initial_uncertainty=1, process_variance=1e-3, measurement_variance=1e-2):
        self.state = initial_state  # Initial estimate of the state (depth)
        self.uncertainty = initial_uncertainty  # Initial estimate uncertainty
        self.process_variance = process_variance  # Variance in the process (small number)
        self.measurement_variance = measurement_variance  # Variance in measurements

    def predict(self):
        # Prediction step: assumes a constant model (no state change)
        self.uncertainty += self.process_variance  # Increase uncertainty by process noise

    def update(self, measurement):
        # Kalman Gain calculation
        kalman_gain = self.uncertainty / (self.uncertainty + self.measurement_variance)
        
        # Update state with the new measurement
        self.state += kalman_gain * (measurement - self.state)
        
        # Update uncertainty
        self.uncertainty *= (1 - kalman_gain)

    def get_state(self):
        return self.state