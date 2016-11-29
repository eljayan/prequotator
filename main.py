from sys import argv
from Prequotation import Prequotation
from traceback import print_exc

def main(filename):
    p = Prequotation(filename)
    if  p.selfCheckTotalTax():
        print "Front math check succeded"
    else:
        print "Front math check failed"

    p.setItems()
    p.createSummary()
    print "process finished."

if __name__ == '__main__':
    try:
        f = argv[1]
        main(f)
    except:
        print_exc()
    finally:
        raw_input("")