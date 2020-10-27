from utility import color


class Instance:
    def __init__(self, instanceId, type, state, securityGroup, rootVolume, tag):
        self.instanceId = instanceId
        self.type = type
        self.state = state
        self.securityGroup = securityGroup
        self.rootVolume = rootVolume
        self.tag = tag
        
    def addPadding(self):
        self.instanceId = self.instanceId.ljust(24," ")
        self.type = self.type.ljust(12," ")
        self.state = self.state.ljust(12," ")
        self.securityGroup = self.securityGroup.ljust(25," ")
        self.rootVolume = self.rootVolume.ljust(25," ")
        self.tag = self.tag.ljust(25," ")

    def print(self):
        print(" | {}|  {} |  {}|  {}|  {}|  {}  |".format(self.instanceId, self.type, self.state, self.securityGroup, self.rootVolume, self.tag))    


def printInstanceDetailHeader():
    print('\n')
    print(color.BOLD + color.BLUE + "            EC2 INSTANCES :" + color.END + " we-need-2-get-this-value         |    " + color.BOLD + color.DARKCYAN + "ACCOUNT :" + color.END +  color.YELLOW + " we-need-2-get-this-value" + color.END)
#    print('\n')

def printInstanceDetailTableHeader():
    print(" ".ljust(145, "-")) 
    label1 = "| Instance-Id".ljust(25," ")
    label2 = " Type".ljust(12, " ")
    label3 = " State".ljust(12, " ")
    label4 = " SecurityGroup".ljust(25, " ")
    label5 = " Root-Volume".ljust(25, " ")
    label6 = " Tag".ljust(25, " ")
    print(" {} | {}  | {} | {} | {} | {}   |".format(label1, label2, label3, label4, label5, label6))
    print(" ".ljust(145, "-")) 
    #print('\n')

def printInstanceDetails(collection):
    for instance in collection:
        instance.addPadding()
        instance.print()

def printInstanceDetailsFooter(instanceCount, runningInstanceCount, regionName):
    message = " "
    if runningInstanceCount == 0:
	    message = color.color.BOLD + color.color.BLUE + '* ' + color.color.END + 'No Running Instances'
    instanceCount = color.color.BOLD + str(instanceCount) + color.color.END
    print(" ".ljust(145, "-") + '\n 		Total Instances [{}]: {}	{}'.format(regionName, instanceCount, message) +
		"\n ".ljust(146,"-"))
    print('\n')
    #print(" ".ljust(143, "-") + color.BOLD + color.BLUE + '\n 		Total Instances [need-2-get-region-value]: {}	{}'.format(instanceCount, message) +
	#	"\n ".ljust(143,"-"))

def getInstanceCollection(ec2Client, instanceCollection, runningInstanceCount):
	response = ec2Client.describe_instances()
	Reservations = response.get("Reservations")
	for reservation in Reservations:
		#OwnerId = reservation.get("OwnerId")
		Instances = reservation.get("Instances")
		for instance in Instances:
			instanceId = instance.get("InstanceId")
			instanceType = instance.get("InstanceType")
			state = instance.get("State")
			stateName = state.get("Name")
			if stateName == "running":
				runningInstanceCount += 1
		#	placement = instance.get("Placement")
		#	az = placement.get("AvailabilityZone")
			Tags = instance.get("Tags")
			if Tags:
				for tag in Tags:
					Tag = tag.get("Value")
	#		sg = NetworkInteraces.get("SecurityGroup
	#		for n in NetworkInterfaces:	
	#			SecurityGroup = n.get("SecurityGroups")
	#			for sg in SecurityGroup:
	#				securityGroupName = sg.get("GroupName")
	#		sgs = instance.get("SecurityGroups")
	#		for sg in sgs:
	#			securityGroup = sgs.get("GroupName")
			sg = "Need-2-code-this"
			rootVolume = "Need-2-code-this"
			i = Instance(instanceId, instanceType, stateName, sg, rootVolume, Tag)
			instanceCollection.append(i)
            
if __name__ == "__main__":
    
    i1 = Instance("i-1111111111111111", "t2-micro", "Running", "jenkins-server-us-cas", "vol-1111-6321-7412-9856", "myTagLine-Flying in the Sky")
    i2 = Instance("i-2222222222222222", "t2-micro", "Stopped", "jenkins-server-us-cas", "vol-2222-2222-7412-9856", "myTagLine-Flying in the Sky")
    i3 = Instance("i-3333333333333333", "t2-micro", "Running", "jenkins-server-us-cas", "vol-3333-6321-7412-9856", "myTagLine-Flying in the Sky")

    Instances = []
    Instances.append(i1)
    Instances.append(i2)
    Instances.append(i3)

    printInstanceDetailHeader()
    printInstanceDetailTableHeader()
    printInstanceDetails(Instances)
    print('\n')