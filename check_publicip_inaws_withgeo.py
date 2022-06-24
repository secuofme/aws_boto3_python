import requests
import boto3
import json

# input check profile list
profile_names = ["test-profile", "test"]
# input check regions
aws_regions = ["ap-northeast-1", "ap-northeast-2", "eu-west-1", "eu-west-2"]
# input check ip list
ips = ["1.1.1.1"]
# geolocation check url
url = "https://ipinfo.io/"

for profile_name in profile_names:
  for region_name in aws_regions:
    session = boto3.Session(profile_name=profile_name, region_name=region_name)
    # Get resources from AWS
    ec2 = session.resource('ec2')

    instances = ec2.instances.all()
    for instance in instances:
      if instance.state['Name'] != 'running':
        pass
      else:
        for tags in instance.tags:
          if tags["Key"] == "Name":
            instance_tagname = tags['Value']
          else:
            pass
        for network in instance.network_interfaces_attribute:
          publicip = network.get('Association')
          if publicip == None:
            pass
          else:
            public_ip = publicip.get('PublicIp')
            for ip in ips:
              if public_ip == ip:
                req = requests.get(url + ip)
                iplocation = json.loads(req.content.decode("utf-8"))
                print(public_ip, instance_tagname, iplocation['city'])
              else:
                pass
    print("Check is Done '%s' Region on '%s' Profile" % (region_name, profile_name))
    

  