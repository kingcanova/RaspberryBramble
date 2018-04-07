
import dispy
 
jobs = dispy.recover_jobs('crash')
for job in jobs:
        print('Job result: %s' % job.result)

