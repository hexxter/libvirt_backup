#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
  virt-backup.py VMNAME DEST

Options:
  -h --help     Show this screen.
  VMNAME	Name of the host
  DEST		Destination dir or url for rsync
"""
import libvirt
import time, os
from docopt import docopt

states = {
	libvirt.VIR_DOMAIN_NOSTATE: 'no state',
	libvirt.VIR_DOMAIN_RUNNING: 'running',
	libvirt.VIR_DOMAIN_BLOCKED: 'blocked on resource',
	libvirt.VIR_DOMAIN_PAUSED: 'paused by user',
	libvirt.VIR_DOMAIN_SHUTDOWN: 'being shut down',
	libvirt.VIR_DOMAIN_SHUTOFF: 'shut off',
	libvirt.VIR_DOMAIN_CRASHED: 'crashed',
}

def main():
	arguments = docopt(__doc__)

	if arguments['VMNAME'] is None:
		print( "pls give me a VM Name" )
		sys.exit(0)
	if arguments['DEST'] is None:
		print( "pls give me a DEST" )
		sys.exit(0)

	DEST = arguments['DEST']

	conn = libvirt.open( "qemu:///system" )  # $LIBVIRT_DEFAULT_URI, or give a URI here
	assert conn, 'Failed to open connection'
	#VMNAME = "SAGE_vm"
	VMNAME = arguments['VMNAME']
	vm = conn.lookupByName( VMNAME )
	state, maxmem, mem, ncpu, cputime = vm.info()
	print( "VM State:", states.get(state, state) )
	vm_vol_path = conn.storagePoolLookupByName( 'default' ).storageVolLookupByName( VMNAME ).path()
	vm_vol = "%s/*" % ( vm_vol_path )

	#print( dir(vm) )
	#print( dir(conn) )
	#print( vm.name() )

	if "running" in states.get(state, state): 

		print( "send %s to suspend" % VMNAME )
		vm.suspend()

		while "paused by user" not in states.get(state, state):
			state, maxmem, mem, ncpu, cputime = vm.info()

		print( "%s is in state: %s" % (VMNAME, states.get(state, state)) )
		print( "sync %s to %s" % ( vm_vol, DEST ) )
		#print( "rsync -avrP %s %s" % ( vm_vol, DEST ) ) 
		os.system( "rsync -avrP %s %s" % ( vm_vol, DEST ) ) 
		print( "start %s again" % VMNAME )
		vm.resume()


if __name__ == "__main__":
	main()

'''
	snap_xml = <domainsnapshot>
		<name>snap1</name>
		<description>snap1</description>
		</domainsnapshot>
	vm.snapshotCreateXML( snap_xml, libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY|libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC )
	snap_path = "%s/%s.%s" % (vm_vol_path, VMNAME, vm.snapshotCurrent().getName())
	print( snap_path )
	#vm.blockPull( snap_path )

	print( vm.snapshotListNames() )

	print( vm.blockJobInfo( snap_path ) )	
'''
