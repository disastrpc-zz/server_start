import time, sys, threading
from datetime import datetime
from pexpect.popen_spawn import PopenSpawn


class ServerHandler:

    def __init__(self, start_script):

        # self.timer = ServerTimer()
        self.jvm_args = (open(start_script, 'r')).read()

        if self.jvm_args is not None:
            sys.stdout.write(f"Detected Java arguments from {start_script}: \n{self.jvm_args}\n")
        else:
            sys.stdout.write("Start script not found, quitting...\n")
            exit()

        self.start_triggers = ['[Server thread/INFO]: Done (',
                            '[Server thread/INFO] [minecraft/DedicatedServer]: Done (',
                            'For help, type "help"']
        self.status = False

    # Start JVM instance with provided arguments
    def instantiate(self):
        try:
            self.server = PopenSpawn(self.jvm_args)
        except Exception as e:
            sys.stderr.write(str(e))

    # Listen on the JVM for triggers
    def listen(self):

        while self.server.proc.poll() is None:
                line = self.server.proc.stdout.read()
                print(line)
                # if 'For help, type "help"' in i.decode('utf-8'):
                #         sys.stdout.write('{} [Python Wrapper] [INFO]: Server detected online\n'.format(timestamp()))
                #         self.status = True
                #         self.execute('say test!')


                # for trigger in self.start_triggers:
                #     if trigger.encode('utf-8') in self.server.proc.stdout.readline():
                #         sys.stdout.write('{} [Python Wrapper] [INFO]: Server detected online\n'.format(timestamp()))
                #         self.status = True
                #         self.execute('say test!')
                #         break


                if line == '' and self.server.proc.poll() != None:
                    break

                if line != '':
                    sys.stdout.write(line.decode('utf-8'))
                    sys.stdout.flush()

            # if self.status:
            #         self.timer_start()
            #         self.run_timer()

            # if self.status:
            #     self.timer.start_timestamp = self.timer.get_timestamp()

    def timer_start(self):
        self.start_timestamp = int(time.time())

    def spawn_timer_daemon(self):
        self.timer_daemon = threading.Thread(target=self.run_timer, name='timer', daemon=True)
        self.timer_daemon.start()

    def run_timer(self):
        self.server.sendline('list')
        
    def update_pipe(self):
        return (self.server.proc.stdout.readline()).decode('utf-8')

    def execute(self, cmd):
        self.server.sendline(cmd)

# class ServerTimer(ServerHandler):

#     def __init__(self):

#         self.interval = 5
#         self.start_timestamp = None

#     def get_timestamp(self):
#         return int(time.time())

#     def spawn(self):
#         self.daemon = threading.Thread(target=self.update(), name='timer')
#         self.daemon.run()

#     def update(self):
#         while True:
#             print('update')

def timestamp():
    ts = time.gmtime()
    return '[{}]'.format(time.strftime("%H:%M:%S", ts))

def main():

    if (len(sys.argv) < 1):
        sys.stdout("Incorrect args. \nUsage: python server_start.py <path to script>")
        exit()
                                                                                                                                                                                                                                                                                                                                                                                           
    handler = ServerHandler(sys.argv[1])                                                                                                                                                                                                                                                                                                                                                   
    handler.instantiate()                                                                                                                                                                                                                                                                                                                                                                  
    handler.listen()                                                                                                                                                                                                                                                                                                                                                                       
    #handler.instantiate_and_listen()                                                                                                                                                                                                                                                                                                                                                      
main()   
