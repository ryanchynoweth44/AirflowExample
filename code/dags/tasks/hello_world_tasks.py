

def print_world():
    print('world')



def test_write_file():
    file = open("test_file.txt", "w")
    file.write("This is a test of Apache Airflow.")
    file.close()