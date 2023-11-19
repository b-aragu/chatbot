import unittest
from echomodel import EchoModel  

class TestEchoModel(unittest.TestCase):

    def setUp(self):
        # This method will be called before each test
        self.echo_model = EchoModel()

    def test_predict(self):
        # Test the predict method of EchoModel
        user_input = "Hello, World!"
        expected_output = f"Your custom model says: {user_input}"

        # Call the predict method and compare the result with the expected output
        actual_output = self.echo_model.predict(user_input)
        self.assertEqual(actual_output, expected_output, "EchoModel did not produce the expected output.")

if __name__ == '__main__':
    unittest.main()

