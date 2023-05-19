from ciscoaxl import axl

cucm = 'cucm1.dcloud.cisco.com'
username = 'axlapiuser'
password = 'dCloud123!'
version = '12.5'
ucm = axl(username=username,password=password,cucm=cucm,cucm_version=version)

########### Add Bruce Lee #############

for user in ucm.get_users():
    print(user.firstName)
ucm.add_user(userid='blee',lastName='Lee',firstName='Bruce')
print("\n adding Bruce\n")

for user in ucm.get_users():
    print(user.firstName)

print("\n removing Bruce\n")

ucm.delete_user(userid='blee')

for user in ucm.get_users():
    print(user.firstName)

############# Add a phone for Bruce #############


ucm.add_phone(
	name='SEPB4B4B4B4B4B4',
	description='8861 for Bruce',
	product='Cisco 8861',
	device_pool='Conferencing',
	phone_template='Standard 8861 SIP',
	protocol='SIP',
	securityProfileName='Universal Device Template - Model-independent Security Profile',
	lines=[(
		'+14085554019',
		'DN',
		'Jim Li',
		'Jim Li',
		'Jim li',
        '+14085554019'
		)]
	)

######### Print Directory Numbers with associated data #########
for dn in ucm.get_directory_numbers():
    print(dn.pattern, dn.description, dn['routePartitionName']['_value_1'])




######### Print phones with device model and locations #########

phoneslist = ucm.get_phones()

for phones in phoneslist:
    print (phones.description, phones.name, phones['locationName']['_value_1'], phones.product)

######## Reorder Route Group ##########

 
            
rg = ucm.get_route_group(name='new')
print(rg)

groupmap = { "EU" : { "index" : None, "order": None},
             "US" : { "index" : None, "order": None}}
for x in range(len(rg['members']['member'])):
    if rg['members']['member'][x]['deviceName']['_value_1'] == 'ST_UCM_EMEA':
        groupmap['EU']['order'] = rg['members']['member'][x]['deviceSelectionOrder']
        groupmap['EU']['index'] = x
    elif rg['members']['member'][x]['deviceName']['_value_1'] == 'TRUNK_TO_CUBE_US':
        groupmap['US']['order'] = rg['members']['member'][x]['deviceSelectionOrder']
        groupmap['US']['index'] = x
rg['members']['member'][groupmap['US']['index']]['deviceSelectionOrder'] = groupmap['EU']['order']
rg['members']['member'][groupmap['EU']['index']]['deviceSelectionOrder'] = groupmap['US']['order']

ucm.update_route_group(name='new',members=rg.members)

rgnew = ucm.get_route_group(name='new')
print(rgnew) 
