import sys
from routingnode import router

if __name__ == "__main__":
    # TODO: check argv
    router.run(sys.argv[1])