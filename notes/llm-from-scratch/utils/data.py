from utils.downloaders import THE_VERDICT_FILE

def read_the_verdict():
    with open(THE_VERDICT_FILE) as f:
        return f.read()
