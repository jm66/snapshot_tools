vmware_snapshot_tool
====================

A pysphere script for basic snapshot management (create, delete, list, revert).

``` bash
./vmware_snapshot_tool.py -h
usage: vmware_snapshot_tool.py [-h] -s SERVER -u USERNAME -m VMNAME [-v] [-V]
                               {revert,create,list,delete} ...

Manage VM snapshots. Create, Delete, List and Revert to Snapshot.

positional arguments:
  {revert,create,list,delete}
                        commands
    list                List Snapshot(s) of a given VM
    create              Create a Snapshot of a given VM
    delete              Delete a Snapshot of a given VM
    revert              Revert to a Snapshot of a given VM

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        The vCenter or ESXi server to connect to
  -u USERNAME, --user USERNAME
                        The username with which to connect to the server
  -m VMNAME, --vm VMNAME
                        The virtual machine (VM) to manage snapshots
  -v, --verbose         Enable verbose output
  -V, --version         show program's version number and exit
```    

For instance, listing snapshots taken of a certain VM:

``` bash
./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra list
Enter password for vCenter 198.100.234.200 for user vma: 
Successfully found dijkstra in [datastore1] dijkstra/dijkstra.vmx
 
OK. Found 2 snapshot(s). Will take a few secs to list them...
 
Snapshot(s) found:
Name: Snap2014-02-08@2
Description Testing new features
Created: (2014, 2, 10, 14, 0, 14, 850, 0, 0)
State: poweredOn
Path: /Snap2014-02-08@2
 
Name: Snap2014-02-08@3
Description Testing new features
Created: (2014, 2, 10, 14, 27, 37, 78, 0, 0)
State: poweredOn
Path: /Snap2014-02-08@2/Snap2014-02-08@3

``` 

Creating a snapshot:

``` bash
 ./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra create -sn Snap2014-02-08@3 -sd "Testing new features"
Enter password for vCenter 198.100.234.200 for user vma: 
Successfully found dijkstra in [datastore1] dijkstra/dijkstra.vmx
 
Creating snapshot on dijkstra with the following attributes: 
Snapshot name: Snap2014-02-08@3
Snapshot Description: Testing new features
Run Synchronously: False
 
OK. Creating Snapshot...
Task running asynchronously. This might take a few minutes.

```

Deleting snapshot:

``` bash
 ./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra delete -sn Snap2014-02-08@3 
 Enter password for vCenter 198.100.234.200 for user vma: 
 Successfully found dijkstra in [datastore1] dijkstra/dijkstra.vmx
 
 Deleting snapshot of dijkstra: 
 Snapshot name: Snap2014-02-08@3
 Run Synchronously: False
 Delete children: False
 
 OK. Deleting Snapshot...
 Task running asynchronously. This might take a few minutes.

```

Reverting to a specific snapshot:

``` bash
./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra revert -sn Snap2014-02-08@2
Enter password for vCenter 198.100.234.200 for user vma: 
Successfully found dijkstra in [datastore1] dijkstra/dijkstra.vmx
 
Reverting snapshot on dijkstra with the following attributes: 
Snapshot name: Snap2014-02-08@2
Run Synchronously: False
 
OK. Reverting to requested Snapshot...
Task running asynchronously. This process might take a few minutes.
```
