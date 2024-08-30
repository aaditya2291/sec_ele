

def get_random_base64(count):
    """
        Generating the required number of dictionaries containing the base64 strings along with the other variables.
    """
    import random
    import string
    import datetime
    import base64
    import os

    def random_hex_string(length):
        """Generates a random hex string of a given length."""
        return ''.join(random.choices(string.hexdigits.lower(), k=length))

    def random_base64_string():
        """Generates a random base64 string similar to the one provided."""
        raw_bytes = random_hex_string(180).encode()
        base64_str = base64.b64encode(raw_bytes).decode('utf-8')
        return base64_str

    def random_id():
        """Generates a random ID similar to the '_id' field."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def random_index():
        """Generates a random '_index' string based on a date in 2024."""
        date_str = datetime.datetime(2024, random.randint(1, 12), random.randint(1, 28)).strftime('%Y.%m.%d')
        return f"syslog-{date_str}"

    def random_timestamp():
        """Generates a random timestamp in 2024 in the required format."""
        date = datetime.datetime(2024, random.randint(1, 12), random.randint(1, 28),
                                 random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"

    def generate_random_dict():
        """Generates a single random dictionary."""
        timestamp = random_timestamp()
        base64_str = random_base64_string()

        return {
            "@timestamp": [timestamp],
            "@version": ["1"],
            "@version.keyword": ["1"],
            "event.original": [f"<185>{timestamp[5:10]} NUC11TNHi5 HPC-IDS[18545]: IDS-R|{base64_str}"],
            "event.original.keyword": [f"<185>{timestamp[5:10]} NUC11TNHi5 HPC-IDS[18545]: IDS-R|{base64_str}"],
            "message": [f"<185>{timestamp[5:10]} NUC11TNHi5 HPC-IDS[18545]: IDS-R|{base64_str}"],
            "message.keyword": [f"<185>{timestamp[5:10]} NUC11TNHi5 HPC-IDS[18545]: IDS-R|{base64_str}"],
            "type": ["syslog"],
            "type.keyword": ["syslog"],
            "_id": random_id(),
            "_index": random_index(),
            "_score": None
        }

    def generate_random_dicts(count):
        """Generates a list of random dictionaries."""
        return [generate_random_dict() for _ in range(count)]

    # Generate 100 random dictionaries
    random_dicts = generate_random_dicts(count)

    return random_dicts