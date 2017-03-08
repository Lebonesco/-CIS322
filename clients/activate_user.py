import sys
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main(port, username, password, role):
    args = {}
    args["timestamp"] = datetime.datetime.utcnow().isoformat()
    args["username"] = username
    args["password"] = password
    args["role"] = role

    args = json.dumps(args)

    req = Request(port, data.encode("ascii"), method-'POST')
    res = urlopen(req)

    res = json.loads(res.read().decode("ascii"))

    print("Server returned: %s"%resp['result'])



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python %s <port> <username> <password> <role>"%sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
