import os, sys, re

while True:
    #what to print
    command = '$'
    x = input(command)
    #string stuff
    split_string = x.split(" ")

    pid = os.fork()

    if split_string[0].lower() == 'exit':
        sys.exit(1)

    homedirectory = '/Users/jerardovelazquez'

    if split_string[0].lower() == 'cd':
        os.chdir(split_string[1])

    if pid == 0:
        args = split_string

        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            #error handling
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
        print("Command Not Found!")
        sys.exit(1)

    else:
        finish = os.waitpid(0, 0)
