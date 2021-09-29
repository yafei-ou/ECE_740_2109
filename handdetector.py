import mediapipe as mp
import cv2
import numpy as np

class Stabilizer:
    """Using Kalman filter as a point stabilizer."""

    def __init__(self,
                 state_num=4,
                 measure_num=2,
                 cov_process=0.0001,
                 cov_measure=0.1):
        """Initialization"""
        # Currently we only support scalar and point, so check user input first.
        assert state_num == 4 or state_num == 2, "Only scalar and point supported, Check state_num please."

        # Store the parameters.
        self.state_num = state_num
        self.measure_num = measure_num

        # The filter itself.
        self.filter = cv2.KalmanFilter(state_num, measure_num, 0)

        # Store the state.
        self.state = np.zeros((state_num, 1), dtype=np.float32)


        # Store the measurement result.
        self.measurement = np.array((measure_num, 1), np.float32)

        # Store the prediction.
        self.prediction = np.zeros((state_num, 1), np.float32)

        # Kalman parameters setup for scalar.
        if self.measure_num == 1:
            self.filter.transitionMatrix = np.array([[1, 1],
                                                     [0, 1]], np.float32)

            self.filter.measurementMatrix = np.array([[1, 1]], np.float32)

            self.filter.processNoiseCov = np.array([[1, 0],
                                                    [0, 1]], np.float32) * cov_process

            self.filter.measurementNoiseCov = np.array(
                [[1]], np.float32) * cov_measure

        # Kalman parameters setup for point.
        if self.measure_num == 2:
            self.filter.transitionMatrix = np.array([[1, 0, 1, 0],
                                                     [0, 1, 0, 1],
                                                     [0, 0, 1, 0],
                                                     [0, 0, 0, 1]], np.float32)

            self.filter.measurementMatrix = np.array([[1, 0, 0, 0],
                                                      [0, 1, 0, 0]], np.float32)

            self.filter.processNoiseCov = np.array([[1, 0, 0, 0],
                                                    [0, 1, 0, 0],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]], np.float32) * cov_process

            self.filter.measurementNoiseCov = np.array([[1, 0],
                                                        [0, 1]], np.float32) * cov_measure

    def update(self, measurement):
        """Update the filter"""
        # Make kalman prediction
        self.prediction = self.filter.predict()

        # Get new measurement
        if self.measure_num == 1:
            self.measurement = np.array([[np.float32(measurement[0])]])
        else:
            self.measurement = np.array([[np.float32(measurement[0])],
                                         [np.float32(measurement[1])]])

        # Correct according to mesurement
        self.filter.correct(self.measurement)

        # Update state value.
        self.state = self.filter.statePost

    def set_q_r(self, cov_process=0.1, cov_measure=0.001):
        """Set new value for processNoiseCov and measurementNoiseCov."""
        if self.measure_num == 1:
            self.filter.processNoiseCov = np.array([[1, 0],
                                                    [0, 1]], np.float32) * cov_process
            self.filter.measurementNoiseCov = np.array(
                [[1]], np.float32) * cov_measure
        else:
            self.filter.processNoiseCov = np.array([[1, 0, 0, 0],
                                                    [0, 1, 0, 0],
                                                    [0, 0, 1, 0],
                                                    [0, 0, 0, 1]], np.float32) * cov_process
            self.filter.measurementNoiseCov = np.array([[1, 0],
                                                        [0, 1]], np.float32) * cov_measure



class SingleHandDetector:

    def __init__(self, useStabilizer=True):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False,
                            max_num_hands=1,
                            min_detection_confidence=0.8,
                            min_tracking_confidence=0.5)
        self.useStabilizer = useStabilizer
        self.steadyPoints = None
        if useStabilizer:
            self.pointStabilizers = [Stabilizer(
                state_num=4,
                measure_num=2,
                cov_process=0.005,
                cov_measure=0.1) for _ in range(21)]

    def runDetection(self, img):
        results = self.hands.process(img)
        h, w, _ = img.shape
        multiHandLms = results.multi_hand_landmarks
        # print(multiHandLms)
        if multiHandLms:
            self.points = []
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    self.points.append([lm.x *w, lm.y *h])
        else:
            self.points = None
        return self.points

    def stabilize(self):
        if self.points:
            if self.useStabilizer:
                steadyPoints = []
                for pt, stb in zip(self.points, self.pointStabilizers):
                    p = np.array([[np.float32(pt[0])], [np.float32(pt[1])]])
                    stb.update(p)
                    steadyPoint = np.array([stb.state[0][0], stb.state[1][0]])
                    # print(p, steadyPoint)
                    steadyPoints.append(steadyPoint)
                self.steadyPoints = np.array(steadyPoints)
            return steadyPoints
        else:
            return None
    
    def getSteadyPoints(self):
        return self.steadyPoints