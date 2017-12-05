
import dispy

jobs = dispy.recover_jobs()
for job in jobs:
        print('Job result: %s' % job.result)

