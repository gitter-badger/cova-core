import sys
from computenode import computer

if __name__ == "__main__":
    # TODO: check argv
    # look for ../config/usercred.json
    # from there get all the credentials, url, port
    computer.run(sys.argv[1], sys.argv[2])