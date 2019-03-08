
def test_write_file():
    file = open("test_file.txt", "w")
    file.write("This is a test of Apache Airflow.")
    file.close()

if __name__ == '__main__':
    test_write_file()