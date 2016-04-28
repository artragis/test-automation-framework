import time


class TestCallback:
    """
    This represents actions that will be executed at the end of a test
    """
    def on_success(self, test):
        """
        called on success
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_failure(self, test):
        """
        called on failure
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_error(self, test):
        """
        called on error (i.e when an unexpected Exception is raised)
        :param test:
        :type test: unittest.TestCase
        """
        pass

    def on_skip(self, test):
        """
        called on skipping test
        :param test:
        :type test: unittest.TestCase
        """
        pass


class TakeScreenshotCallback(TestCallback):
    """
    This callback will take screenshot on failure or error
    """
    def __init__(self, filepath_format):
        self.filepath_format = filepath_format

    def __get_data(self, test, **kwargs):
        default = dict(
            name = test.id(),
            status = "fail",
            time=int(time.time())
        )
        default.update(kwargs)
        return default

    def on_failure(self, test):
        if hasattr(test, "driver"):
            test.driver.save_screenshot(self.filepath_format.format(**self.__get_data()))

    def on_error(self, test):
        if hasattr(test, "driver"):
            test.driver.save_screenshot(self.filepath_format.format(**self.__get_data(status="error")))


def with_callback(callback):
    """
    Decorator to be used for registering a callback
    :param callback:
    :type callback: TestCallback
    """
    def __(cls):
        class NewTest(cls):
            def __init__(self, *args, **kwargs):
                super(NewTest, self).__init__(*args, **kwargs)
                if not hasattr(self, "callbacks"):
                    self.callbacks = []
                self.callbacks.append(callback)
        return NewTest
    return __