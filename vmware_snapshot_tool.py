#!/usr/bin/python
import sys, re, getpass, argparse, subprocess,urllib, urllib2
from time import sleep
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
from pysphere.vi_virtual_machine import VIVirtualMachine

# - Revert To Snapshot
# |- Revert by Name

def print_verbose(message):
	if verbose:
		print message
		
def find_vm(name, con):
	try:
		vm = con.get_vm_by_name(name)
		return vm
	except VIException:
		return None

def list_snapshot(vm):
	try:
		snapshot_list = vm.get_snapshots()
		snapshot_list_len = len(snapshot_list)
		print " " 
		print("OK. Found %d snapshot(s). Will take a few secs to list them..." % snapshot_list_len)
		print " "
		if len(snapshot_list) > 0:
		        print "Snapshot(s) found:"
			for snapshot in snapshot_list:
			  print "Name:", snapshot.get_name()
			  print "Description", snapshot.get_description()
			  print "Created:", snapshot.get_create_time()
			  print "State:", snapshot.get_state()
			  print "Path:", snapshot.get_path()
		  	print " "
		else:
			print("Nothing here to see. Goodbye!")
	except VIException as inst:
		print "Ooops! Something went wrong."
		print inst

def create_snapshot(vm, snapname, snapdesc, snaprun):
	try:
		print " "
		print "Creating snapshot on %s with the following attributes: " % vm.get_property('name') 
		print "Snapshot name: %s"  %snapname
		print "Snapshot Description: %s" % snapdesc
		print "Run Synchronously: %s" % snaprun
		print " "
		print "OK. Creating Snapshot..."
		vm.create_snapshot(snapname, description=snapdesc, sync_run=snaprun)
		if snaprun:
			print "Snapshot taken successfully."
		else:	
			print "Task running asynchronously. This might take a few minutes."
	except VIException as inst:
		print "Ooops! Something went wrong."
		print inst

def delete_snapshot(vm, snapname, snaprun, children):
	try:
                print " "
                print "Deleting snapshot of %s: " % vm.get_property('name')
	        print "Snapshot name: %s"  % snapname
		print "Run Synchronously: %s" % snaprun
		print "Delete children: %s" % children
                print " "
                print "OK. Deleting Snapshot..."
		vm.delete_named_snapshot(snapname, remove_children=children, sync_run=snaprun)
		if snaprun:
			print "Snapshot successfully deleted"
		else:
			print "Task running asynchronously. This might take a few minutes."
	except VIException as inst:
		print "Ooops! Something went wrong."
		print inst

def revert_snapshot(vm, snapname, snaprun):
	try:
                print " "
                print "Reverting snapshot on %s with the following attributes: " % vm.get_property('name')
                print "Snapshot name: %s"  %snapname
                print "Run Synchronously: %s" % snaprun
                print " "
                print "OK. Reverting to requested Snapshot..."
                vm.revert_to_named_snapshot(snapname, sync_run=snaprun)
		if snaprun:
			print "Successfully reverterd to requested snapshot."
		else:
			print "Task running asynchronously. This process might take a few minutes."

	except VIException as inst:
		print "Oops. Something went wrong"
		print inst

# Creating the argument parser
parser = argparse.ArgumentParser(description="Manage VM snapshots. Create, Delete, List and Revert to Snapshot.")
parser.add_argument('-s', '--server', nargs=1, required=True, help='The vCenter or ESXi server to connect to', dest='server', type=str)
parser.add_argument('-u', '--user', nargs=1, required=True, help='The username with which to connect to the server', dest='username', type=str)
parser.add_argument('-m', '--vm', nargs=1, required=True, help='The virtual machine (VM) to manage snapshots', dest='vmname', type=str)
parser.add_argument('-v', '--verbose', required=False, help='Enable verbose output', dest='verbose', action='store_true')
parser.add_argument('-V', '--version', action='version', version="%(prog)s (version 0.1)")

subparsers = parser.add_subparsers(help='commands')

# A list command
list_parser = subparsers.add_parser('list', help='List Snapshot(s) of a given VM')
list_parser.add_argument('-a','--all', action='store_true', help='List all snapshots', default=False, dest='lall')

# A create command
create_parser = subparsers.add_parser('create', help='Create a Snapshot of a given VM')
create_parser.add_argument('-sn', '--sname', required=True, action='store', help='New snapshot name', dest='sname', type=str)
create_parser.add_argument('-sd', '--sdescription', required=True, help='New snapshot description.', action='store', dest='sdesc', type=str)
create_parser.add_argument('-sr', '--syncrun', default=False, help='Take snapshot synchronously, default is False', dest='ssync', action='store_true')

# A delete command
delete_parser = subparsers.add_parser('delete', help='Delete a Snapshot of a given VM')
delete_parser.add_argument('-sn', '--sname', action='store', required=True, help='Name of the snapshot to delete', dest='snamed', type=str)
delete_parser.add_argument('-sr', '--syncrun', default=False, help='Delete snapshot synchronously, default is False', dest='ssync', action='store_true')
delete_parser.add_argument('-ch', '--children', default=False, help='Will delete not only the specified snapshot but also all of its descendants, default is False', dest='children', action='store_true')

# A revert command
revert_parser = subparsers.add_parser('revert', help='Revert to a Snapshot of a given VM')
revert_parser.add_argument('-sn', '--sname', action='store', required=True, help='Name of the snapshot to revert', dest='snamer', type=str)
revert_parser.add_argument('-sr', '--syncrun', default=False, help='Revert to snapshot synchronously, default is False', dest='ssync', action='store_true')

args = parser.parse_args()
argsdict = vars(args)
server 		= args.server[0]
username 	= args.username[0]
vmname	 	= args.vmname[0]
verbose		= args.verbose

# Asking Users password for server
password=getpass.getpass(prompt='Enter password for vCenter %s for user %s: ' % (server,username))

# Connecting to server
print_verbose('Connecting to server %s with username %s' % (server,username))

con = VIServer()
con.connect(server,username,password)
print_verbose('-' * 50)
print_verbose('Connected to server %s' % server)
print_verbose('Server type: %s' % con.get_server_type())
print_verbose('API version: %s' % con.get_api_version())
print_verbose('-' * 50)

# Getting VM object
vm = find_vm(vmname, con)

if vm:
	print('Successfully found %s in %s' % (vm.get_property('name'), vm.get_property('path')))
else:
	print("Could not find %s, please verify VM's name and try again." % vm)
	sys.exit()

# Parse List opt
if hasattr(args, 'lall'):
        list            = args.lall
	list_snapshot(vm)
	con.disconnect()
	sys.exit()
elif hasattr(args, 'sname'):
	# Parse create opt
	snapname        = args.sname
	snapdesc        = args.sdesc
	snaprun         = args.ssync
	create_snapshot(vm, snapname, snapdesc, snaprun)
	con.disconnect()
	sys.exit()
elif hasattr(args, 'snamed'):
	snapnamed 	= args.snamed
	snaprun 	= args.ssync
	children	= args.children
	delete_snapshot(vm, snapnamed, snaprun, children)
	con.disconnect()
	sys.exit()
elif hasattr(args, 'snamer'):
	snapnamer	= args.snamer
	snaprun		= args.ssync
	revert_snapshot(vm, snapnamer, snaprun)
	con.disconnect()
	sys.exit()

con.disconnect()