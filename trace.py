counter = 1000

def generate_trace_id():
    global counter
    counter += 1
    return f"TRACE_{counter}"