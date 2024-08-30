

def decode_hex_string(strings):
    """
        Takes the hex_string as the input and based on the column details, breaks it down at
        respective intervals and decode it as needed.
    """
    
    import datetime
    # Remove spaces from the hex string
    base64_string = strings[0]
    hex_string = strings[1]
    hex_string = hex_string.replace(" ", "")
    hex_string = hex_string[40:]
    # Group sizes as specified
    group_sizes = [1, 1, 1, 2, 2, 1, 4, 4, 8, 2, 14, 64]
    groups = ['log_type', 'can_bus_number', 'violation_rule_id', 'signal_start_bit', 'signal_length', 'raw_message_length', 'message_can_id', 'detection_time', 'detection_reason', 'duplication_number', 'reserved', 'raw_message_body', 'context_idsr', 'context_binary']
    results = {}
    # Initialize variables
    start = 0
    decodings = []
    j = 1

    # Decode each group
    for size in group_sizes:
        
        end = start + size * 2  # Each group size represents pairs of hex digits
        group = hex_string[start:end]
        
        # Convert to integer
        decoded_value = int(group, 16)
        
        if j == 1:
            binary_hex_str = bin(int(group, 16))[2:].zfill(size * 8)
            decodings.append(binary_hex_str)
        # Check if it's the group that should be a timestamp
        elif j == 8:
            # Assuming Unix epoch for the timestamp conversion
            decoded_value = int(group, 16)
            timestamp = datetime.datetime.utcfromtimestamp(decoded_value)
            decodings.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            decodings.append(decoded_value)
        
        start = end
        j += 1
        
    decodings.append(base64_string)
    decodings.append(hex_string)
    for i in range(len(groups)):
        results[groups[i]] = decodings[i]
    return results