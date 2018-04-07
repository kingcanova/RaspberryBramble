# executed on each node before any jobs are scheduled!
def setup(data_file):
    # read data in file to global variable
    global words, bounds
    words = []
    bounds = []

    f = open(data_file, 'r').read()  # read file in to memory; data_file can now be deleted
    i = 0
    nextUpper = 'A'
    nextLower = 'a'
    with open(data_file) as fp:
        for line in fp:
           line = str(line)
           lines = line.split('\n')
           line = lines[0]
           #print("got here")
           # ord()#turns char to ascii value
           # chr()#turns number to ascii character
           words.append(line)
           if (words[i][0] == nextUpper or words[i][0] == nextLower):

              nextUpper = chr(ord(nextUpper)+ 1)
              nextLower = chr(ord(nextLower)+ 1)
              bounds.append(i)
           i += 1
    #print("got here2")
    bounds.append(i)
    return 0


def cleanup():
    global words, bounds
    del words, bounds


# function 'compute' is distributed and executed with arguments
# supplied with 'cluster.submit' below
def compute(bIndex):
    import time, socket
    global words, bounds
    pals = 0
    print("its in here")
    hostname = socket.gethostname()
    for x in range(bounds[bIndex], bounds[bIndex+1]):
        word = words[x]
        reverse = word[::-1]
        rChar = reverse[0]
        if (ord(rChar) < ord('a')):
            rChar = chr(ord(rChar)+32)
        firstLetterId = ord(rChar) - 97
        if (firstLetterId >= 0 and firstLetterId < 26):
            # for each word in the first letter group
            found = 0
            for j in range(bounds[firstLetterId], bounds[firstLetterId+1]):

                if (words[j] == reverse):

                    found = 1
                    break
            if (found == 1):
                pals += 1

    return(pals, hostname)


if __name__ == '__main__':
    # executed on client only; variables created below, including modules imported,
    # are not available in job computations
    import dispy, sys, functools, random, dispy.httpd

    # if no data file name is given, use this file as data file
    data_file = sys.argv[1] if len(sys.argv) > 1 else sys.exit()
    print(sys.argv[1] + "\n\n\n")
    cluster = dispy.JobCluster(compute,nodes=['10.20.1.17','10.20.1.72','10.20.1.32','10.20.1.75','10.20.0.73'], depends=[data_file], recover_file='crashData', loglevel=dispy.logger.INFO,
                               setup=functools.partial(setup, data_file), cleanup=cleanup)
    # run 'compute' with 20 random numbers on available CPUs
    jobs = []
    http_server = dispy.httpd.DispyHTTPServer(cluster)

    # cluster can now be monitored / managed in web browser at
    # http://<host>:8181 where <host> is name or IP address of
    # computer running this program
    #print("PRooooblem here \n\n\n")
    for i in range(26):
        job = cluster.submit(i)
        job.id = i  # associate an ID to identify jobs (if needed later)
        jobs.append(job)
    # cluster.wait() # waits until all jobs finish
    totalPals = 0
    for job in jobs:
        #print("Is the problem in returning the job? \n\n\n")
        words = job()
        #print(words)
        pals, hostname = job()  # waits for job to finish and returns results
        totalPals += pals
        print('%s executed job %s at %s with %s palindromes counted' % (hostname, job.id, job.start_time,pals))
        # other fields of 'job' that may be useful:
        # job.stdout, job.stderr, job.exception, job.ip_addr, job.end_time
    print("\n\n")
    print("The total number of palindromes found is: %s" % (totalPals))
    cluster.print_status()  # shows which nodes executed how many jobs etc.
    http_server.shutdown()
    cluster.close()
