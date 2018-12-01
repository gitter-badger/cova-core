import json
import sys
from nodehelpers.protocol_const import DEFAULT_CRED_PATH


def get_credentials(cred_path):
    with open(cred_path) as f:
        return json.load(f)


if __name__ == "__main__":
    cred = None
    try:
        if len(sys.argv) == 2:
            cred = get_credentials(sys.argv[1])
        else:
            cred = get_credentials(DEFAULT_CRED_PATH)
    except Exception as e:
        print "FAILED TO GET CREDENTIALS"
        raise e
        sys.exit()

    if cred["router"]:
        from routingnode import router
        router.run(cred["id"], cred)
    else:
        from computenode import computer
        computer.run(cred["eth_cred"]["address"], cred["public_ip"])

    
    