import numpy as np

skeleton_1 = np.load('./data/skeleton_2.npy')


class FallDetection:
    """
    Used to extract features from keypoints.
    """

    def __init__(self):
        self.torso_up = np.array(
            [[5, 6]]
        )  # The slice used for generating the midpoint of the shoulders

        self.torso_down = np.array(
            [[11, 12]]
        )  # The slice used for generating the midpoint of the hips

        self.vector_indices = np.array(
            [
                [19, 17],
                [19, 18],
                [6, 12],
                [5, 11],
                [6, 8],
                [5, 7],
                [12, 14],
                [11, 13],
                [11, 12],
                [13, 15],
                [14, 16],
                [20, 21],
            ]
        )  # Vectors to be considered for calculating angles

        self.pair_indices = np.array(
            [[4, 2], [5, 3], [6, 10], [7, 9], [8, 6], [8, 7], [0, 11], [1, 11]]
        )  # The pairs of vectors for angle computation

        self.vertical_coordinates = np.array(
            [[1, 1], [1, 100]]
        )  # A vertical vector for comparing with other vectors

        self.angle_weights = np.ones((8, 1))  # Weights for angles
        self.cache_weights = np.ones((1, 6))  # Weights for the cache
        self.fps = 18  # Number of frames to consider in every second
        self.threshold = 10  # The threshold for fall detection

    def angleCalculation(self, vectors):
        """
        Used to calculate the angles between given pairs of vectors
        Takes as input the list of vector pairs, which represent two vectors with two coordinates each
        Returns the list of angles between them
        """

        difference = np.subtract(
            vectors[:, :, 0], vectors[:, :, 1]
        )  # Subtracts the coordinates to obtain the vectors

        dot = (difference[:, 0, :] * difference[:, 1, :]).sum(
            axis=-1
        )  # Calculates the dot product between the pairs of vectors

        norm = np.prod(
            np.linalg.norm(difference[:, :, :], axis=2), axis=-1
        )  # Calculates the norm of the vectors and multiplies them, same as |a|*|b|

        cos_angle = np.divide(dot, norm)  # cos(x) = dot(a,b)/|a|*|b|

        angle = (
                np.arccos(cos_angle) * 180 / np.pi
        )  # Take arccos of the result to get the angle

        angle = angle.reshape(-1, 1)  # Correct the shape of the output

        return angle

    def collectData(self, keypoints):
        """
        Calls handleMissingValues and addExtraPoints functions
        Used for handling negative predictions and adding extra points to the keypoints
        Takes as input the list of keypoints
        Returns the list of handled keypoints and added extra points
        """
        keypoints = self.handleMissingValues(keypoints)
        keypoints = self.addExtraPoints(keypoints)
        return keypoints

    def handleMissingValues(self, keypoints):
        """
        Used for replacing negative predictions with NaNs
        Takes as input the list of the keypoints for the current frame
        Returns corrected list of keypoints with NaNs instead of negative values
        """

        if keypoints.size > 0:
            keypoints = np.where(
                keypoints < 0, np.nan, keypoints
            )  # Where the points is negative replace it with NaN

        return keypoints

    def addExtraPoints(self, keypoints):

        """
        Used for adding extra points to the keypoints list
        Takes as input the keypoints for the frame
        Returns the list of keypoints with added extra points
        """
        if keypoints.size>0:
            torso_up = keypoints[self.torso_up].mean(axis=1)

            torso_down = keypoints[self.torso_down].mean(axis=1)

            head_coordinate = np.nanmean(keypoints[:5], axis=0)

            keypoints = np.vstack(
                (
                    keypoints,
                    torso_up,
                    torso_down,
                    head_coordinate,
                    self.vertical_coordinates,
                )
            )

            return keypoints
    def differenceMean(self, vector1_angles, vector2_angles):
        """
        Used for calculating the feature using differenceMean method
        Takes as input previous frame angles and current frame angles
        Returns a scalar (the cost)
        """

        angle_difference = np.abs(
            vector1_angles - vector2_angles
        )  # Absolute difference of previous frame's angles and current frame's angles

        return (
                np.nanmean(angle_difference) * self.fps
        )  # Returns the mean of the difference multiplied by fps

    def __call__(self,skeleton):
        cache = []
        for i in range(len(skeleton)-1):
            previous_keypoints = self.collectData(skeleton[i])
            current_keypoints = self.collectData(skeleton[i+1])

            vector1_pairs = np.array(
                previous_keypoints[self.vector_indices][self.pair_indices]
            )  # Get vector pairs for previous keypoints
            #             print(previous_keypoints)

            vector2_pairs = np.array(
                current_keypoints[self.vector_indices][self.pair_indices]
            )  # Get vector pairs for current keypoints
            #             print(previous_keypoints[self.vector_indices], 'With indices')
            vector1_angles = (
                self.angleCalculation(vector1_pairs)
            )  # Calculate the angles for previous frame

            #             print(vector1_pairs)
            #             print(vector1_angles)
            vector2_angles = (
                self.angleCalculation(vector2_pairs)
            )  # Calculate the angles for current frame

            cost = self.differenceMean(vector1_angles, vector2_angles)
            cache.append(cost)
        fallScore = np.nanmean(cache)
        if fallScore > 40:
            isFall = True
        else:
            isFall = False
        return  isFall, fallScore
a = FallDetection()
print(a(skeleton_1))
