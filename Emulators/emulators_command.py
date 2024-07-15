class CommandEmulators:

    def __init__(self, socket):
        self.socket = socket
        self.validSrcList = ["front", "web", "seq", "eth", "slot1", "slot2", "slot3", "slot4", "loc", "rem"]

    def send_command(self, msg):

        try:
            print(f"Calling command: {msg}")
            msg = msg + "\n"
            self.socket.sendall(msg.encode("UTF-8"))
        except Exception as e:
            print(e)

    def set_prog_source_v(self, src):
        retval = 0
        if src in self.validSrcList:
            self.send_command("SYST:REM:CV {0}".format(src))

        else:
            retval = -1
        return retval

    def set_prog_source_i(self, src):
        retval = 0
        if src.lower() in self.validSrcList:
            self.send_command("SYST:REM:CC {0}".format(src))
        else:
            retval = -1
        return retval
