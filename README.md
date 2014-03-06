vmware_snapshot_tool
====================

A pysphere script for basic snapshot management (create, delete, list, revert).

``` bash
./vmware_snapshot_tool.py  -h
usage: vmware_snapshot_tool.py [-h] -s SERVER -u USERNAME -m VMNAME [-v] [-d]
                               [-l LOGFILE] [-V]
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
  -d, --debug           Enable debug output
  -l LOGFILE, --log-file LOGFILE
                        File to log to (default = stdout)
  -V, --version         show program's version number and exit
```    

For instance, listing snapshots taken of a certain VM:

``` bash
./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra -d list
2014-02-25 12:47:33,937 DEBUG logger initialized
2014-02-25 12:47:33,937 DEBUG No command line password received, requesting password from user
Enter password for vCenter 198.100.234.200 for user vma:
2014-02-25 12:47:35,960 INFO Connecting to server 198.100.234.200 with username vma
2014-02-25 12:47:35,960 DEBUG Trying to connect with provided credentials
2014-02-25 12:47:36,515 INFO Connected to server 198.100.234.200
2014-02-25 12:47:36,515 DEBUG Server type: VMware vCenter Server
2014-02-25 12:47:36,516 DEBUG API version: 5.1
2014-02-25 12:47:39,731 DEBUG Found VM dijkstra
2014-02-25 12:47:39,731 INFO Successfully found dijkstra in [datastore1] dijkstra_1/dijkstra.vmx
2014-02-25 12:47:39,731 DEBUG Listing all snapshots as requested by user.
2014-02-25 12:47:40,223 DEBUG  Found 1 snapshot(s). Will take a few secs to list.
2014-02-25 12:47:40,223 INFO 1 snapshot(s) found.
{'snapshot-3337': {'Created': (2014, 2, 25, 12, 19, 6, 897, 0, 0),
                   'Description': 'description1',
                   'Name': 't1',
                   'Path': '/t1',
                   'State': 'poweredOn'}}
2014-02-25 12:47:40,223 DEBUG Terminating vCenter session.
``` 

Creating a snapshot:

``` bash
 ./vmware_snapshot_tool.py -s 198.100.234.200 -u vma -m dijkstra create -sn Snap2014-02-08@3 -sd "Testing new features"
2014-02-25 12:52:08,142 DEBUG logger initialized
2014-02-25 12:52:08,142 DEBUG No command line password received, requesting password from user
Enter password for vCenter 198.100.234.200 for user vma: 
2014-02-25 12:52:10,315 INFO Connecting to server 198.100.234.200 with username vma
2014-02-25 12:52:10,316 DEBUG Trying to connect with provided credentials
2014-02-25 12:52:10,841 INFO Connected to server 198.100.234.200
2014-02-25 12:52:10,842 DEBUG Server type: VMware vCenter Server
2014-02-25 12:52:10,842 DEBUG API version: 5.1
2014-02-25 12:52:14,057 DEBUG Found VM dijkstra
2014-02-25 12:52:14,057 INFO Successfully found dijkstra in [datastore1] dijkstra_1/dijkstra.vmx
2014-02-25 12:52:14,057 DEBUG Creating snapshot as requested by user.
2014-02-25 12:52:14,058 INFO Creating snapshot on dijkstra with the following attributes: Name: Snap2014-02-08@3; Description: Testing new features; Run Sync: False
2014-02-25 12:52:14,318 WARNING Task running asynchronously. This might take a few minutes.
2014-02-25 12:52:14,319 DEBUG Terminating vCenter session.

```
