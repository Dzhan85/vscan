class discovered_host(object):
    """
    Auxiliary class used for storing discovered hosts
    """

    def __init__(self):
        self.hostname = ''
        self.response_code = 0
        self.hash = ''
        self.keys = []
        self.content = b''

"""
Adding to output content-type, content-length
"""

        #self.content_type = ''
        #self.content_length ''
