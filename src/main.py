import argparse
from frames.app import App
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galvanic Skin Sensor tracker")
    parser.add_argument('--test', '-t', default='n', help='Set it as y or Y if you want to run the program in test environment. Default: n')
    args = parser.parse_args()
    isTest = args.test.lower() == "y"

    app = App(isTest)
    app.mainloop()