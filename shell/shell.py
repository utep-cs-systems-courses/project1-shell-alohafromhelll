import os, sys, re

while True:

    x = input()
    split_string = x.split(" ")

    if split_string[0].lower() == 'exit':
        sys.exit(1)

    if split_string[0].lower() == 'cd':
        os.chdir(split_string[1])



    pid = os.fork()



    if pid == 0:
        #print('test')


        if '>' in split_string:
            i = split_string.index('>')


            os.close(1)
            os.open(split_string[i + 1], os.O_CREAT | os.O_WRONLY);
            #sys.stdout = open(split_string[i+1].strip(), "w")
            os.set_inheritable(1, True)
            split_string = split_string[0:i]


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
