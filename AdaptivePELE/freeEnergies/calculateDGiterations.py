import os
import sys
import shutil
from AdaptivePELE.freeEnergies import estimateDG, prepareMSMFolders

# list of tuples with format (lagtime, #clusters)
iterations = [(25, 100), (50, 100), (100, 100), (200, 100), (400, 100),
              (25, 200), (50, 200), (100, 200), (200, 200), (400, 200),
              (25, 400), (50, 400), (100, 400), (200, 400), (400, 400)]
runFolder = os.getcwd()
print "Running from " + runFolder
for tau, k in iterations:
    destFolder = "%d/%dcl" % (tau, k)
    prepareMSMFolders.main()
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)
    print "***************"
    print "Estimating dG value in folder" + os.getcwd()
    parameters = estimateDG.Parameters(ntrajs=None, length=None, lagtime=tau,
                                       nclusters=k, nruns=10, skipFirstSteps=0,
                                       useAllTrajInFirstRun=True,
                                       computeDetailedBalance=True,
                                       trajWildcard="traj_*",
                                       folderWithTraj="rawData",
                                       lagtimes=[1, 10, 25, 50, 100, 250, 500, 1000],
                                       clusterCountsThreshold=0)
    try:
        estimateDG.estimateDG(parameters, cleanupClusterCentersAtStart=True)
    except Exception as err:
        if "distribution contains entries smaller" in err.message:
            print "Caught exception in step with lag %d and k %d, moving to next iteration" % (tau, k)
            with open("error.txt", "w") as fe:
                fe.write("Caught exception in step with lag %d and k %d, moving to next iteration\n" % (tau, k))
        else:
            raise type(err), type(err)(str(err)), sys.exc_info()[2]
    shutil.move("MSM_0", destFolder)
