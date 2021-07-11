from os import name

from cv2 import data
from traffic import *
import unittest

# Uses the small directory in the hints section of specification for testing. Can be changed to the big version.
DIRECTORY = "gtsrb-small"


class LoadingDataTestClass(unittest.TestCase):
    def setUp(self):
        self.data = load_data(DIRECTORY)

    def test_shape_of_image(self):
        self.assertEqual(
            # Get an image to check the shape
            self.data[0][0].shape,
            (30, 30, 3)
        )

    def test_len_of_data(self):
        self.assertEqual(len(self.data[0]), len(self.data[1]))
        if DIRECTORY == "gtsrb-small":
            self.assertEqual(len(self.data[0]), 840)

    def test_num_categories(self):
        # Get all the unique numbers in a list
        # For every number add it to unique numbers list if not already in it
        unique_labels = []
        for label in self.data[1]:
            if label not in unique_labels:
                unique_labels.append(label)

        self.assertEqual(
            len(unique_labels),
            NUM_CATEGORIES
        )


if __name__ == '__main__':
    unittest.main()
