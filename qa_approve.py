from typing import List, Tuple
import subprocess

ADDRESS_CITY_MAP = {
    "SFO": "185 Berry St, San Francisco, CA 94107",
    "SEA": "400 Broad St, Seattle, WA 98109",
    "LAS": "770 Las Vegas Blvd N, Las Vegas, NV 89101",
    "AUS": "919 E 32nd St, Austin, TX 78705",
}


def run_cmd(cmd: str, timeout: int):
    proc = subprocess.Popen([cmd], shell=True)
    try:
        proc.communicate(timeout=timeout)
        return 0
    except:
        proc.kill()
        return -1


def qa_approve(driver_phone_number: str, city: str):
    print(f"-------start approving {driver_phone_number} from {city}-------")
    qa_approve_cmd = f'''
                        (echo logout
                        sleep 4
                        echo login
                        sleep 2
                        echo "\n"
                        sleep 2
                        echo {driver_phone_number}
                        sleep 10
                        echo 'set-default-location --address \"{ADDRESS_CITY_MAP[city]}\"'
                        sleep 4
                        echo 'qa-approve'
                        sleep 6
                        ) | driver-cli
                    '''
    driver_return_code = run_cmd(qa_approve_cmd, timeout=35)
    print(f"-------finished approving {driver_phone_number} from {city}-------")
    return driver_return_code


def qa_approve_batch(phone_numbers: List[Tuple]):
    retries = 5  # each phone number will get up to 5 retries if qa-approve fails for some reason
    for phone_number, city in phone_numbers:
        counter = 1
        while counter <= retries:
            if qa_approve(phone_number, city) == 0:
                break
            else:
                counter += 1


if __name__ == "__main__":
    # add all phone numbers you need to qa approve below. The phone numbers below are for earnings team UI automation
    driver_phone_numbers = [
        ("4135553178", "SFO"),
        ("4185552882", "AUS"),
        ("4235557832", "AUS"),
        ("4105559030", "AUS"),
        ("4075556855", "SFO"),
        ("4385559316", "SFO"),
        ("4195551878", "AUS"),
        ("4435552084", "SFO")
     ]

    qa_approve_batch(driver_phone_numbers)
