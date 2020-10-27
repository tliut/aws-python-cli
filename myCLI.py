
#!/usr/bin/env python3
#!/home/tony/aws-cli-test-proj/venv/bin python3
import argparse
import boto3

from resources import Instance
from resources import Volume
from resources import Snapshot
from utility import color

resourceChoices = ["Instances", "Volumes", "Snapshots"]

def handleCommandArguments():

    myParser = argparse.ArgumentParser(description='Display a list of resources defined by the Service Command')

    myParser.add_argument("-s", type=str, choices=["Instances", "Volumes", "Snapshots"], help="the aws resource type for the command", required=True)
    myParser.add_argument("-c", type=str, choices=["list"], help="list is the only supported command", required=True)

    return myParser.parse_args()

def getAccountName(AccountId):
    org = boto3.client("organizations")
    resp = org.describe_account(AccountId= AccountId)
    AccountName = resp.get("Account").get("Name")
    #print(resp)
    print(AccountName)
    return AccountName

def getAccountId():
    sts = boto3.client("sts")
    response = sts.get_caller_identity()
    AccountId = response.get("Account")
    #ARN = response.get("Arn")
    print(AccountId)
    #print(ARN)
    return AccountId

def getRegion():
    currentSession = boto3.session.Session()
    regionName = currentSession.region_name
    #print(regionName)
    return regionName

def printTitle(resourceChoice, AccountName):
    print('\n')
    title1 = ""
    title2 = color.color.BOLD + "ACCOUNT: " + color.color.END
    region = color.color.BLUE + getRegion() + color.color.END
    #print("region = " + region)
    AccountName = color.color.YELLOW + AccountName + color.color.END
    #print("AccountName = " + AccountName)

    if resourceChoice == resourceChoices[0]:
        title1 = color.color.BOLD + "            EC2 INSTANCES : " + color.color.END
        
    elif resourceChoice == resourceChoices[1]:
        title1 = color.color.BOLD + "            EBS VOLUMES : " + color.color.END
    
    elif resourceChoice == resourceChoices[2]:
        title1 = color.color.BOLD + "            SNAPSHOTS : " + color.color.END

    title = title1 + " {}         |    " + title2 + " {}" 
    print(title.format(region, AccountName))

def handleInstancesOption(ec2Client, regionName):
    
    instanceCollection = []
    runningInstanceCount = 0
    instanceCount = 0

    Instance.printInstanceDetailTableHeader()
    Instance.getInstanceCollection(ec2Client, instanceCollection, runningInstanceCount)

    Instance.printInstanceDetails(instanceCollection)
    instanceCount = len(instanceCollection)

    Instance.printInstanceDetailsFooter(instanceCount, runningInstanceCount, regionName)

def handleVolumesOption(ec2Client, regionName):
    volumeCollection = []
    volumeSizes = []
    unAttachedVolumeCount = 0
    totalSize = 0

    Volume.printVolumeDetailsTableHeader()
    Volume.getVolumeCollection(ec2Client, volumeCollection, unAttachedVolumeCount, volumeSizes)

    Volume.printVolumeDetails(volumeCollection)
    totalSize = sum(volumeSizes)
    volumeCount = len(volumeCollection)
    Volume.printVolumeDetailsFooter(volumeCount, unAttachedVolumeCount, totalSize, regionName)

def handleSnapshotsOption(ec2Client, AccountId, regionName):
    Snapshots = []
    SnapshotSizes = []

    #Print the SnapshotDetails Table Header
    Snapshot.printSnapshotDetailsTableHeader()

    #Call the ec2 describe_snapshots
    Snapshot.getSnapshotCollection(ec2Client, Snapshots, SnapshotSizes, AccountId)
    
    #Sort the Snapshots List by CreateTime
    Snapshots = Snapshot.sortByCreateTime(Snapshots)
    
    Snapshot.printSnapshotDetails(Snapshots)
    
    #Calculate the Total Number of Snapshots and the Total size of all Snapshots in GB 
    totalSnaps = len(Snapshots)
    totalSnapSize = sum(SnapshotSizes)

    #Print the Footer for the SnapshotsDetail Report.
    Snapshot.printSnapshotDetailsFooter(totalSnaps, totalSnapSize, regionName)

def Main():
    ec2Client = boto3.client('ec2')
    AccountId = getAccountId()
    AccountName = getAccountName(AccountId)
    regionName = getRegion()

    args = handleCommandArguments()
    if args.s in resourceChoices:
        printTitle(args.s, AccountName)
               
        if args.s == resourceChoices[0]:
            handleInstancesOption(ec2Client, regionName)
            
        elif args.s == resourceChoices[1]:
            print("Getting the Volume Details")
            handleVolumesOption(ec2Client, regionName)    
        elif args.s == resourceChoices[2]:
            
            handleSnapshotsOption(ec2Client, AccountId, regionName)

        #printFooter(result)
        
    else:
        print("Service selected is not currently supported")


if __name__ == "__main__":
    Main()


