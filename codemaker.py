import logging
from selenium import webdriver
from time import sleep
import os

logging.basicConfig(filename='log.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)

class CodeMaker:
    url = 'https://sketch.hoylu.com/'

    def __init__(self, input_file,
                 url = 'https://sketch.hoylu.com/', driver_path='chromedriver.exe', short_sleep=1, long_sleep=3,
                 output_folder='sketchcodes'):
        """
        >>> from codemaker import CodeMaker
        >>> cm = CodeMaker('courses.tsv')
        >>> cm.run()
        """


        with open(input_file) as f:
            self.courses = f.read()

        self.url = url
        self.username = input('username:\n')
        self.password = input('password:\n')
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        self.courses = [line.split() for line in self.courses.splitlines()]
        self.sketch_codes = {item[0]: {} for item in self.courses}


        self.driver = webdriver.Chrome(driver_path)
        self.short_sleep = short_sleep
        self.long_sleep = long_sleep




    def run(self):
        self.login()
        self.make_codes()


    def make_codes(self):
        first = True
        for course_code, start_i, end_i in self.courses:
            output_fp = os.path.join(self.output_folder, course_code + '.tsv')
            print('Created', output_fp)
            for i in range(int(start_i), int(end_i) + 1):
                self.driver.find_element_by_class_name('b69').click()
                sleep(self.short_sleep)
                # clears old work space
                if not first:
                    self.driver.find_element_by_class_name('b92').click()
                    sleep(self.short_sleep)
                    self.driver.find_element_by_class_name('b1f').click()
                    sleep(self.short_sleep)
                    self.driver.find_element_by_class_name('b69').click()
                    sleep(self.short_sleep)
                else:
                    first = False

                sketch_name = '{code}-Lesson{num}'.format(code=course_code, num=str(i).zfill(2))
                self.driver.find_element_by_class_name('b23').send_keys(sketch_name)
                self.driver.find_element_by_class_name('b96').click()
                sleep(self.long_sleep)

                sketch_code = self.driver.current_url.split('/')[-1]
                output_line = "{sn}\t'{sc}\n".format(sn=sketch_name, sc=sketch_code)

                with open(output_fp, 'a+') as f:
                    f.write(output_line)
                print(output_line)










    def login(self):
        self.driver.get(self.url)
        sleep(self.long_sleep)
        email_input = self.driver.find_element_by_class_name('b23')
        email_input.send_keys(self.username)
        continue_button = self.driver.find_element_by_class_name('b19')
        continue_button.click()
        sleep(self.long_sleep)
        password_input = self.driver.find_element_by_class_name('b23')
        password_input.send_keys(self.password)
        login_button = self.driver.find_element_by_class_name('b19')
        login_button.click()
        sleep(self.long_sleep)


def tsv_fixer(fn):
    with open(fn) as f:
        text = f.read()

    output = []

    for line in text.splitlines():
        course, code = line.split()
        code = "'" + code

        output.append(course + '\t' + code)

    output = '\n'.join(output)

    with open(fn.split('.')[0] + '.tsv', 'w') as f:
        f.write(output)

