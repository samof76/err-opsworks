from errbot import BotPlugin, botcmd, arg_botcmd
import boto
from boto import opsworks


class OpsWorks(BotPlugin):
    """
    This is plugin for AWS OpsWorks Operations. The Plugin is still work in progress
    and will add more functionality as days go by. Right now of it is read functionality.
    """

    def get_stack_id(self, name, region):
        opw = opsworks.connect_to_region(region)
        stacks = opw.describe_stacks()['Stacks']
        for stack in stacks:
            if stack['Name'] == name:
                return stack['StackId']        
        return None
        
    def get_ec2_instance_id(self, name, stack_id, region):
        opw = opsworks.connect_to_region(region)
        instances = opw.describe_instances(stack_id=stack_id)['Instances']
        for instance in instances:
            if instance['Hostname'] == name:
                return instance['Ec2InstanceId']
        return None

    def get_instance_id(self, name, stack_id, region):
        opw = opsworks.connect_to_region(region)
        instances = opw.describe_instances(stack_id=stack_id)['Instances']
        for instance in instances:
            if instance['Hostname'] == name:
                return instance['InstanceId']
        return None

    @botcmd  # flags a command
    def opsworks_hello(self, msg, args):  # a command callable with !tryme
        """
        Execute to check if Errbot responds to command.
        Feel free to tweak me to experiment with Errbot.
        You can find me in your init directory in the subdirectory plugins.
        """
        return 'Hello from *OpsWorks* !'  # This string format is markdown.

    @arg_botcmd('name', type=str)  # flags a command
    @arg_botcmd('--region', dest='region', type=str)
    def opsworks_get_StackId(self, msg, name=None, region=None):  # a command callable with !tryme
        """
        Given a Stack's Name and Region, I will return the StackId
        """
        stack_id = self.get_stack_id(name, region)
        if stack_id:
            return "StackId of {0} stack in {1} region: {2}".format(name, region, stack_id)
        else:
            return "No stack by the name, {0}, in {1} region".format(name, region)

       

    @arg_botcmd('name', type=str)
    @arg_botcmd('--stack', dest='stack', type=str)
    @arg_botcmd('--region', dest='region', type=str)
    def opsworks_get_ec2_InstanceId(self, msg, name=None, stack=None, region=None):
        """
        Give an Instance's Name, Stack Name and Region, I return EC2 Instance Id
        """
        stack_id = self.get_stack_id(stack, region)
        if stack_id:
            ec2_instance_id = self.get_ec2_instance_id(name, stack_id, region)
        else:
            return "No stack by the name, {stack}, in {region} region".format(stack=stack, region=region)
        
        if ec2_instance_id:
            return "EC2 InstanceId of {name} in Stack {stack}: {ec2_instance_id}".format(name=name,stack=stack,ec2_instance_id=ec2_instance_id)
        else:
            return "No instance by the name, {name}, in stack, {stack}, in region, {region}".format(name=name, stack=stack,region=region)


    @arg_botcmd('name', type=str)
    @arg_botcmd('--stack', dest='stack', type=str)
    @arg_botcmd('--region', dest='region', type=str)
    def opsworks_get_InstanceId(self, msg, name=None, stack=None, region=None):
        """
        Give an Instance's Name, Stack Name and Region, I return EC2 Instance Id
        """
        stack_id = self.get_stack_id(stack, region)
        if stack_id:
            instance_id = self.get_instance_id(name, stack_id, region)
        else:
            return "No stack by the name, {stack}, in {region} region".format(stack=stack, region=region)
        
        if instance_id:
            return "InstanceId of {name} in Stack {stack}: **{instance_id}**".format(name=name,stack=stack,instance_id=instance_id)
        else:
            return "No instance by the name, {name}, in stack, {stack}, in region, {region}".format(name=name, stack=stack,region=region)