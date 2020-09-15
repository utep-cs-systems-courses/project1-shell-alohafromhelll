#Jerardo Velazquez ID:80266747
import os, sys, re

while True:
    #ps1 var
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    #default set to $
    else:
        os.write(1, ('$').encode())
    try:
        userCommand = input()
    except EOFError:
        sys.exit(1)

    
    # split input by blank space
    split_string = userCommand.split(" ")
    #check if exit
    if split_string[0].lower() == 'exit':
        sys.exit(1)
    #check if change directory
    if split_string[0].lower() == 'cd':
        os.chdir(split_string[1])
    #fork
    pid = os.fork()

    #child
    if pid == 0:
        #redirect
        #ls > out.txt
        if '>' in split_string:
            i = split_string.index('>')
            os.close(1)
            os.open(split_string[i + 1], os.O_CREAT | os.O_WRONLY);
            #sys.stdout = open(split_string[i+1].strip(), "w")
            os.set_inheritable(1, True)
            split_string = split_string[0:i]

        #grep py < t.txt
        elif '<' in split_string:
            print('hello')
            i = split_string.index('<')
            os.close(0)
            os.open(split_string[i + 1], os.O_RDONLY);
            #sys.stdin = open(split_string[i+1].strip(), "r")
            os.set_inheritable(0, True)
            split_string = split_string[0:i]

        #pipes
        #ls | grep py
        if '|' in split_string:
            #grab the index of the pipe to split later
            i = split_string.index('|')
            #both pipe commands
            pipe1 = split_string[0:i]
            pipe2 = split_string[i+1:len(split_string)]

            #pipe
            pr,pw = os.pipe()

            #file descriptors
            for fdes in (pr, pw):
                os.set_inheritable(fdes, True)
            pipeChild = os.fork()

            if pipeChild < 0:
                sys.exit(1)

            #pipe child
            if pipeChild == 0:
                os.close(1)
                os.dup(pw)
                os.set_inheritable(1, True)
                #file descriptors
                for fdes in (pr, pw):
                    os.close(fdes)
                #pipe1 for arguments
                split_string = pipe1
            else:
                os.close(0)
                os.dup(pr)
                os.set_inheritable(0, True)
                #file descriptors
                for fd in (pr,pw):
                    os.close(fd)
                #pipe2 for arguments
                split_string = pipe2

        #attaching arguments to new list
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
