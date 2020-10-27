import boto3
from utility import color

#instantiate the color class
color = color.color()

class Snapshot:
    def __init__(self, SnapId, Size, CreateTime, State, Prog, Encrypted, VolumeId, Tag, Description):
        self.SnapId = SnapId
        self.Size = Size
        self.CreateTime = CreateTime
        self.State = State
        self.Prog = Prog
        self.Encrypted = Encrypted
        self.VolumeId = VolumeId
        self.Tag = Tag
        self.Description = Description

    def addPadding(self):
        self.SnapId = self.SnapId.ljust(24," ")
        self.Size = self.Size.ljust(6," ")
        self.CreateTime = self.CreateTime.ljust(29," ")
        self.State = self.State.ljust(12," ")
        self.Prog = self.Prog.ljust(8," ")
        self.Encrypted = self.Encrypted.ljust(12," ")
        self.VolumeId = self.VolumeId.ljust(25," ")
        self.Tag = self.Tag.ljust(25," ")
        self.Description = self.Description.ljust(25," ")

    def print(self):
        print(" | {}|  {} |  {}|  {}|  {}|  {}|  {}|  {}|  {}|".format(self.SnapId, self.Size, self.CreateTime, self.State, self.Prog, self.Encrypted, self.VolumeId, self.Tag, self.Description))    

'''
def printSnapshotDetailsHeader():
    print('\n')
    print(color.BOLD + color.BLUE + "            SNAPSHOTS :" + color.END + " we-need-2-get-this-value         |    " + color.BOLD + color.DARKCYAN + "ACCOUNT :" + color.END +  color.YELLOW + " we-need-2-get-this-value" + color.END)

'''
def printSnapshotDetailsTableHeader():
    print(" ".ljust(195, "-")) 
    label1 = "| Snap-Id".ljust(25," ")
    label2 = " Size".ljust(6, " ")
    label3 = " CreateTime " + color.BOLD + color.CYAN + "*".ljust(17, " ") + color.END
    label4 = " State".ljust(12, " ")
    label5 = " Prog".ljust(8, " ")
    label6 = " Encrypted".ljust(12, " ")
    label7 = " VolumeId".ljust(25, " ")
    label8 = " Tag".ljust(25, " ")
    label9 = " Description".ljust(25, " ")
    print(" {} | {}  | {} | {} | {} | {} | {} | {} | {} |".format(label1, label2, label3, label4, label5, label6, label7, label8, label9))
    print(" ".ljust(195, "-")) 
    

def printSnapshotDetailsFooter(totalSnaps, totalSnapSize, regionName):
    totalSnaps = color.BOLD + color.BLUE + str(totalSnaps) + color.END
    totalSnapSize = color.BOLD + color.BLUE + str(totalSnapSize) + color.END
    print(" ".ljust(195, "-") + '\n 		{} snapshots in region [need-2-get-region-value],  total {} GB '.format(totalSnaps, totalSnapSize) + color.CYAN + '(*sorted)' + color.END +
		"\n ".ljust(196,"-") +"\n")


def printSnapshotDetails(Snapshots):
    for snapshot in Snapshots:
        snapshot.addPadding()
        snapshot.print()




def getSnapshotCollection(ec2Client, Snapshots, SnapshotSizes, AccountId):

    AccountIds = []
    AccountIds.append(AccountId)
    SnapshotsList = ec2Client.describe_snapshots(MaxResults=10).get("Snapshots")
    '''
    response = ec2Client.describe_snapshots(OwnerIds = AccountIds)
    SnapshotsList = response.get("Snapshots")
    '''
    # Sort the Snapshot List by "CreateTime" Before Printing the table
    Snapshots.sort(key=sortByCreateTime)
    for snapshot in SnapshotsList:
        SnapId = snapshot.get("SnapshotId")
        Size = snapshot.get("VolumeSize")
        CreateTime = snapshot.get("StartTime")
        State = snapshot.get("State")
        Prog = snapshot.get("Progress")
        Encrypted = snapshot.get("Encrypted")
        VolumeId = snapshot.get("VolumeId")
        Description = snapshot.get("Description")
        Description = Description[:20]
        TagsList = snapshot.get("Tags")
        if TagsList:
            for tag in TagsList:
                Tag = tag.get("Value")
        else:
            Tag = ""
        s = Snapshot(SnapId, str(Size), str(CreateTime), State, Prog, str(Encrypted), VolumeId, Tag, Description)
        Snapshots.append(s)
        SnapshotSizes.append(Size)
        exit

# Define a function for the Sort Criteria to be 'CreateTime' for the Snapshot List
def sortByCreateTime(Snapshots):
    return sorted(Snapshots, key=lambda Snapshot: Snapshot.CreateTime)

'''    
def Main():
    ec2Client = boto3.client('ec2')
    Snapshots = []
    SnapshotSizes = []

    printSnapshotDetailsHeader()
    getSnapshotDetails(ec2Client, Snapshots, SnapshotSizes, AccountId)
    printSnapshotDetailsTableHeader()

    Snapshots = sortByCreateTime(Snapshots)

    printSnapshotDetails(Snapshots)
    totalSnaps = len(Snapshots)
    totalSnapSize = sum(SnapshotSizes)
    printSnapshotDetailsFooter(totalSnaps, totalSnapSize)

if __name__== "__main__":
    Main()
'''