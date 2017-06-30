import hashlib
from selenium import webdriver

class Helper:

    @staticmethod
    def takeScreenshot(url,file):
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024,768)
        driver.get(url)
        driver.save_screenshot(file)
        
    @staticmethod
    def sha1FromFile(file):
        hash = hashlib.sha1()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()

