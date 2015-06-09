import unittest


class AttribLoader(unittest.TestLoader):
    def __init__(self, attrib):
        self.attrib = attrib

    def loadTestsFromModule(self, module, use_load_tests=False):
        return super().loadTestsFromModule(module, use_load_tests=False)

    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        filtered_test_names = [test
                               for test in test_names
                               if hasattr(getattr(testCaseClass, test),
                                          self.attrib)]
        return filtered_test_names


if __name__ == "__main__":
    loader = AttribLoader("slow")
    test_suite = loader.discover(".")
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
