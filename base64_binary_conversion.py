def base64_binary(data):
    """
        Takes the loaded json data as input. Then extracts the base64 string from it.
        After the extraction this string will be converted binary hexadecimal format.
        Finally returns the binary hexadecimal string.
    """
    
    import base64
    
    index_idsr = data['message'][0].index('IDS-R|')
    index_string = index_idsr + 6
    base64_string = data['message'][0][index_string:]
    
    binary_hex_string = base64.b64decode(base64_string).hex()
    
    return (base64_string, binary_hex_string)