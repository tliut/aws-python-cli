from utility import color


class Volume:
    def __init__(self, volId, size, createTime, state, encrypted, instanceId, volType, az, tag):
        self.volId = volId
        self.size = size
        self.createTime = createTime
        self.state = state
        self.encrypted = encrypted
        self.instanceId = instanceId
        self.volType = volType
        self.az = az
        self.tag = tag

    def addPadding(self):
        self.volId = self.volId.ljust(24," ")
        self.size = self.size.ljust(8," ")
        self.createTime = self.createTime.ljust(12," ")
        self.state = self.state.ljust(12," ")
        self.encrypted = self.encrypted.ljust(12," ")
        self.instanceId = self.instanceId.ljust(25," ")
        self.volType = self.volType.ljust(10," ")
        self.az = self.az.ljust(12," ")
        self.tag = self.tag.ljust(25," ")

    def print(self):
        print(" | {}| {} | {} | {} | {} | {} | {} | {} | {} |".format(self.volId, self.size, self.createTime, self.state, self.encrypted, self.instanceId, self.volType, self.az, self.tag))    

def printHeader():
    print('\n')
    print(color.BOLD + "         EBS VOLUMES :" + color.END + " us-east1         |    " + color.BOLD + "ACCOUNT :" + color.END +  color.YELLOW + " MyFAKE-AWS-ACCOUNT" + color.END)
#    print('\n')

def printVolumeDetailsFooter(volumeCount, unAttachedVolumeCount, totalSize, regionName):
    volumeCount = color.color.BOLD + str(volumeCount) + color.color.END
    unAttachedVolumeCount = color.color.BOLD + str(unAttachedVolumeCount) + color.color.END
    totalSize = color.color.BOLD + str(totalSize) + color.color.END

    print(" ".ljust(168, "-") + '\n 		{} Volumes in region [{}],  {} unattached to Instances, Total size on disk	{} GB'.format(volumeCount, regionName, unAttachedVolumeCount, totalSize) +
		"\n ".ljust(169,"-"))
    '''
    print(" ".ljust(168, "-") + color.BOLD + color.BLUE + '\n 		{} Volumes in region [need-2-get-region-value],  {} unattached to Instances, Total size on disk	{} GB'.format(volumeCount, unAttachedVolumeCount, totalSize) +
		"\n ".ljust(169,"-"))
    '''

def printVolumeDetailsTableHeader():
    print(" ".ljust(168, "-")) 
    label1 = "| Volume-Id".ljust(25," ")
    label2 = " Size".ljust(8, " ")
    label3 = " CreateTime".ljust(12, " ")
    label4 = " State".ljust(12, " ")
    label5 = " Encrypted".ljust(12, " ")
    label6 = " InstanceId".ljust(25, " ")
    label7 = " VolType".ljust(10, " ")
    label8 = " Avail-zone".ljust(12, " ")
    label9 = " Tag".ljust(25, " ")
    print(" {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(label1, label2, label3, label4, label5, label6, label7, label8, label9))
    print(" ".ljust(168, "-")) 
    #print('\n')

def printVolumeDetails(collection):
    for vol in collection:
        vol.addPadding()
        vol.print()


def getVolumeCollection(ec2Client, volumeCollection, unAttachedVolumeCount, volumeSizes):
    vd = ec2Client.describe_volumes()
    Volumes = vd.get("Volumes")
    for volume in Volumes:
        Attachments = volume.get("Attachments")
        AZ = volume.get("AvailabilityZone")
        CreateTime = str(volume.get("AttachTime"))
        Encrypted = str(volume.get("Encrypted"))
        Size = volume.get("Size")
        volumeSizes.append(Size)
                
        VolType = volume.get("VolumeType")
        Tags = volume.get("Tags")
        if Tags:
            for T in Tags:
                Tag = T.get("Value")
        for attachment in Attachments:
            InstanceId = attachment.get("InstanceId")
            State = attachment.get("State")
            if State != "attached":
                unAttachedVolumeCount += 1
            VolumeId = attachment.get("VolumeId")
            #Populate the Volume Object
            v = Volume(VolumeId, str(Size), CreateTime, State, Encrypted, InstanceId, VolType, AZ, Tag)
            volumeCollection.append(v)


if __name__ == "__main__":
    
    c1 = Volume("vol-1111111111111111", "8", "10-11-2020", "attached", "False", "987456321", "gp2", "us-east1-b", "myTagLine")
    c2 = Volume("2222", "16", "10-11-2020", "detached", "True", "987456321", "io2", "us-west1-a", "myTagLine")
    c3 = Volume("3333", "32", "10-11-2020", "attached", "False", "987456321", "gp2", "us-east1-b", "myTagLine")

    Volumes = []
    Volumes.append(c1)
    Volumes.append(c2)
    Volumes.append(c3)

    printHeader()
    printVolumeDetailsTableHeader()
    printVolumeDetails(Volumes)
    print('\n')