
import dispy

jobs = dispy.recover_jobs('_dispy_20171205113700')
for job in jobs:
        print('Job result: %s' % job.result)

