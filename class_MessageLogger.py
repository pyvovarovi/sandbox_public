import atexit

class MessageLogger:
    def __init__(self, filename):
        self.filename = filename
        self.messages = []
        atexit.register(self.dump_to_file)

    def append_message(self, message):
        self.messages.append(message)
    
    def dump_to_file(self):
        with open(self.filename, 'a') as file:
            file.write('\n'.join(self.messages) + '\n')

# Usage
logger = MessageLogger('output.txt')
logger.append_message("Hello, World!")
logger.append_message("Goodbye, World!")
