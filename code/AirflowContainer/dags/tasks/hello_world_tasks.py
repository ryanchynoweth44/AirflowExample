import datetime
import os

def print_world():
    print('world')



def test_write_file():
    with open("test_file.txt", "w") as text_file:
        text_file.write("This is a test of Apache Airflow. - " + str(datetime.datetime.utcnow()) + " " + str(os.getcwd()) )
    