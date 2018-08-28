# Using the CORE GUI

* Table of Contents
{:toc}

## Overview

CORE can be used via the GUI or [Python_Scripting](scripting.md). Often the GUI is used to draw nodes and network devices on the canvas. A Python script could also be written, that imports the CORE Python module, to configure and instantiate nodes and networks. This chapter primarily covers usage of the CORE GUI.

![](static/core-workflow.jpg)

CORE can be customized to perform any action at each phase in the workflow above. See the *Hooks...* entry on the **Session Menu** for details about when these session states are reached.

## Modes of Operation

The CORE GUI has two primary modes of operation, **Edit** and **Execute** modes. Running the GUI, by typing **core-gui** with no options, starts in Edit mode.  Nodes are drawn on a blank canvas using the toolbar on the left and configured from right-click menus or by double-clicking them. The GUI does not need to be run as root.

Once editing is complete, pressing the green **Start** button (or choosing **Execute** from the **Session** menu) instantiates the topology within the Linux kernel and enters Execute mode. In execute mode, the user can interact with the running emulated machines by double-clicking or right-clicking on them. The editing toolbar disappears and is replaced by an execute toolbar, which provides tools while running the emulation. Pressing the red **Stop** button  (or choosing **Terminate** from the **Session** menu) will destroy the running emulation and return CORE to Edit mode.

CORE can be started directly in Execute mode by specifying **--start** and a topology file on the command line:

```shell
core-gui --start ~/.core/configs/myfile.imn
```

Once the emulation is running, the GUI can be closed, and a prompt will appear asking if the emulation should be terminated. The emulation may be left running and the GUI can reconnect to an existing session at a later time.

The GUI can be run as a normal user on Linux.

The GUI can be connected to a different address or TCP port using the **--address** and/or **--port** options. The defaults are shown below.

```shell
core-gui --address 127.0.0.1 --port 4038
```

## Toolbar

The toolbar is a row of buttons that runs vertically along the left side of the CORE GUI window. The toolbar changes depending on the mode of operation.

### Editing Toolbar

When CORE is in Edit mode (the default), the vertical Editing Toolbar exists on the left side of the CORE window. Below are brief descriptions for each toolbar item, starting from the top. Most of the tools are grouped into related sub-menus, which appear when you click on their group icon.

* |select| *Selection Tool* - default tool for selecting, moving, configuring nodes
* |start| *Start button* - starts Execute mode, instantiates the emulation
* |link| *Link* - the Link Tool allows network links to be drawn between two nodes by clicking and dragging the mouse
* |router| *Network-layer virtual nodes*
  * |router| *Router* - runs Quagga OSPFv2 and OSPFv3 routing to forward packets
  * |host| *Host* - emulated server machine having a default route, runs SSH server
  * |pc| *PC* - basic emulated machine having a default route, runs no processes by default
  * |mdr| *MDR* - runs Quagga OSPFv3 MDR routing for MANET-optimized routing
  * |router_green| *PRouter* - physical router represents a real testbed machine
  * |document_properties| *Edit* - edit node types button invokes the CORE Node Types dialog. New types of nodes may be created having different icons and names. The default services that are started with each node type can be changed here.
* |hub| *Link-layer nodes*
  * |hub|  *Hub* - the Ethernet hub forwards incoming packets to every connected node
  * |lanswitch| *Switch* - the Ethernet switch intelligently forwards incoming packets to attached hosts using an Ethernet address hash table
  * |wlan| *Wireless LAN* - when routers are connected to this WLAN node, they join a wireless network and an antenna is drawn instead of a connecting line; the WLAN node typically controls connectivity between attached wireless nodes based on the distance between them
  * |rj45| *RJ45* - with the RJ45 Physical Interface Tool, emulated nodes can be linked to real physical interfaces; using this tool, real networks and devices can be physically connected to the live-running emulation
  * |tunnel| *Tunnel* - the Tunnel Tool allows connecting together more than one CORE emulation using GRE tunnels
* *Annotation Tools*
  * |marker| *Marker* - for drawing marks on the canvas
  * |oval| *Oval* - for drawing circles on the canvas that appear in the background
  * |rectangle| *Rectangle* - for drawing rectangles on the canvas that appear in the background
  * |text| *Text* - for placing text captions on the canvas

### Execution Toolbar

When the Start button is pressed, CORE switches to Execute mode, and the Edit toolbar on the left of the CORE window is replaced with the Execution toolbar Below are the items on this toolbar, starting from the top.

* |select| *Selection Tool* - in Execute mode, the Selection Tool can be used for moving nodes around the canvas, and double-clicking on a node will open a shell window for that node; right-clicking on a node invokes a pop-up menu of run-time options for that node
* |stop| *Stop button* - stops Execute mode, terminates the emulation, returns CORE to edit mode.
* |observe| *Observer Widgets Tool* - clicking on this magnifying glass icon
  invokes a menu for easily selecting an Observer Widget. The icon has a darker
  gray background when an Observer Widget is active, during which time moving
  the mouse over a node will pop up an information display for that node.
* |plot| *Plot Tool* - with this tool enabled, clicking on any link will
  activate the Throughput Widget and draw a small, scrolling throughput plot
  on the canvas. The plot shows the real-time kbps traffic for that link.
  The plots may be dragged around the canvas; right-click on a
  plot to remove it.
* |marker| *Marker* - for drawing freehand lines on the canvas, useful during
  demonstrations; markings are not saved
* |twonode| *Two-node Tool* - click to choose a starting and ending node, and
  run a one-time *traceroute* between those nodes or a continuous *ping -R*
  between nodes. The output is displayed in real time in a results box, while
  the IP addresses are parsed and the complete network path is highlighted on
  the  CORE display.
* |run| *Run Tool* - this tool allows easily running a command on all or a
  subset of all nodes. A list box allows selecting any of the nodes. A text
  entry box allows entering any command. The command should return immediately,
  otherwise the display will block awaiting response. The *ping* command, for
  example, with no parameters, is not a good idea. The result of each command
  is displayed in a results box. The first occurrence of the special text
  "NODE" will be replaced with the node name. The command will not be attempted
  to run on nodes that are not routers, PCs, or hosts, even if they are
  selected.

## Menubar

The menubar runs along the top of the CORE GUI window and provides access to a
variety of features. Some of the menus are detachable, such as the *Widgets*
menu, by clicking the dashed line at the top.

### File Menu

The File menu contains options for manipulating the **.imn** Configuration Files. Generally, these menu items should not be used in
Execute mode.

* *New* - this starts a new file with an empty canvas.
* *Open* - invokes the File Open dialog box for selecting a new **.imn**
  or XML file to open. You can change the default path used for this dialog
  in the Preferences Dialog.
* *Save* - saves the current topology. If you have not yet specified a file
  name, the Save As dialog box is invoked.
* *Save As XML* - invokes the Save As dialog box for selecting a new
  **.xml** file for saving the current configuration in the XML file.
* *Save As imn* - invokes the Save As dialog box for selecting a new
  **.imn** topology file for saving the current configuration. Files are saved in the
  *IMUNES network configuration* file
* *Export Python script* - prints Python snippets to the console, for inclusion
  in a CORE Python script.
* *Execute XML or Python script* - invokes a File Open dialog box for selecting an XML file to run or a
  Python script to run and automatically connect to. If a Python script, the script must create
  a new CORE Session and add this session to the daemon's list of sessions
  in order for this to work
* *Execute Python script with options* - invokes a File Open dialog box for selecting a
  Python script to run and automatically connect to. After a selection is made,
  a Python Script Options dialog box is invoked to allow for command-line options to be added.
  The Python script must create a new CORE Session and add this session to the daemon's list of sessions
  in order for this to work
* *Open current file in editor* - this opens the current topology file in the
  **vim** text editor. First you need to save the file. Once the file has been
  edited with a text editor, you will need to reload the file to see your
  changes. The text editor can be changed from the Preferences Dialog.
* *Print* - this uses the Tcl/Tk postscript command to print the current canvas
  to a printer. A dialog is invoked where you can specify a printing command,
  the default being **lpr**. The postscript output is piped to the print
  command.
* *Save screenshot* - saves the current canvas as a postscript graphic file.
* Recently used files - above the Quit menu command is a list of recently use
  files, if any have been opened. You can clear this list in the
  Preferences dialog box. You can specify the number of files to keep in
  this list from the Preferences dialog. Click on one of the file names
  listed to open that configuration file.
* *Quit* - the Quit command should be used to exit the CORE GUI. CORE may
  prompt for termination if you are currently in Execute mode. Preferences and
  the recently-used files list are saved.

### Edit Menu

* *Undo* - attempts to undo the last edit in edit mode.
* *Redo* - attempts to redo an edit that has been undone.
* *Cut*, *Copy*, *Paste* - used to cut, copy, and paste a selection. When nodes
  are pasted, their node numbers are automatically incremented, and existing
  links are preserved with new IP addresses assigned. Services and their
  customizations are copied to the new node, but care should be taken as
  node IP addresses have changed with possibly old addresses remaining in any
  custom service configurations. Annotations may also be copied and pasted.
* *Select All* - selects all items on the canvas. Selected items can be moved
  as a group.
* *Select Adjacent* - select all nodes that are linked to the already selected
  node(s). For wireless nodes this simply selects the WLAN node(s) that the
  wireless node belongs to. You can use this by clicking on a node and pressing
  CTRL+N to select the adjacent nodes.
* *Find...* - invokes the *Find* dialog box. The Find dialog can be used to
  search for nodes by name or number. Results are listed in a table that
  includes the node or link location and details such as IP addresses or
  link parameters. Clicking on a result will focus the canvas on that node
  or link, switching canvases if necessary.
* *Clear marker* - clears any annotations drawn with the marker tool. Also
  clears any markings used to indicate a node's status.
* *Preferences...* - invokes the Preferences dialog box.

### Canvas Menu

The canvas menu provides commands for adding, removing, changing, and switching to different editing canvases.

* *New* - creates a new empty canvas at the right of all existing canvases.
* *Manage...* - invokes the *Manage Canvases* dialog box, where canvases may be
  renamed and reordered, and you can easily switch to one of the canvases by
  selecting it.
* *Delete* - deletes the current canvas and all items that it contains.
* *Size/scale...* - invokes a Canvas Size and Scale dialog that allows
  configuring the canvas size, scale, and geographic reference point. The size
  controls allow changing the width and height of the current canvas, in pixels
  or meters. The scale allows specifying how many meters are equivalent to 100
  pixels. The reference point controls specify the latitude, longitude, and
  altitude reference point used to convert between geographic and Cartesian
  coordinate systems. By clicking the *Save as default* option, all new
  canvases will be created with these properties. The default canvas size can
  also be changed in the Preferences dialog box.
* *Wallpaper...* - used for setting the canvas background image,
* *Previous*, *Next*, *First*, *Last* - used for switching the active canvas to
  the first, last, or adjacent canvas.

### View Menu

The View menu features items for controlling what is displayed on the drawing
canvas.

* *Show* - opens a submenu of items that can be displayed or hidden, such as
  interface names, addresses, and labels. Use these options to help declutter
  the display. These options are generally saved in the topology
  files, so scenarios have a more consistent look when copied from one computer
  to another.
* *Show hidden nodes* - reveal nodes that have been hidden. Nodes are hidden by
  selecting one or more nodes, right-clicking one and choosing *hide*.
* *Locked* - toggles locked view; when the view is locked, nodes cannot be
  moved around on the canvas with the mouse. This could be useful when
  sharing the topology with someone and you do not expect them to change
  things.
* *3D GUI...* - launches a 3D GUI by running the command defined under
  Preferences, *3D GUI command*. This is typically a script that runs
  the SDT3D display. SDT is the Scripted Display Tool from NRL that is based on
  NASA's Java-based WorldWind virtual globe software.
* *Zoom In* - magnifies the display. You can also zoom in by clicking *zoom
  100%* label in the status bar, or by pressing the **+** (plus) key.
* *Zoom Out* - reduces the size of the display. You can also zoom out by
  right-clicking *zoom 100%* label in the status bar or by pressing the **-**
  (minus) key.

### Tools Menu

The tools menu lists different utility functions.

* *Autorearrange all* - automatically arranges all nodes on the canvas. Nodes
  having a greater number of links are moved to the center. This mode can
  continue to run while placing nodes. To turn off this autorearrange mode,
  click on a blank area of the canvas with the select tool, or choose this menu
  option again.
* *Autorearrange selected* - automatically arranges the selected nodes on the
  canvas.
* *Align to grid* - moves nodes into a grid formation, starting with the
  smallest-numbered node in the upper-left corner of the canvas, arranging
  nodes in vertical columns.
* *Traffic...* - invokes the CORE Traffic Flows dialog box, which allows
  configuring, starting, and stopping MGEN traffic flows for the emulation.
* *IP addresses...* - invokes the IP Addresses dialog box for configuring which
  IPv4/IPv6 prefixes are used when automatically addressing new interfaces.
* *MAC addresses...* - invokes the MAC Addresses dialog box for configuring the
  starting number used as the lowest byte when generating each interface MAC
  address. This value should be changed when tunneling between CORE emulations
  to prevent MAC address conflicts.
* *Build hosts file...* - invokes the Build hosts File dialog box for
  generating **/etc/hosts** file entries based on IP addresses used in the
  emulation.
* *Renumber nodes...* - invokes the Renumber Nodes dialog box, which allows
  swapping one node number with another in a few clicks.
* *Experimental...* - menu of experimental options, such as a tool to convert
  ns-2 scripts to IMUNES imn topologies, supporting only basic ns-2
  functionality, and a tool for automatically dividing up a topology into
  partitions.
* *Topology generator* - opens a submenu of topologies to generate. You can
  first select the type of node that the topology should consist of, or routers
  will be chosen by default. Nodes may be randomly placed, aligned in grids, or
  various other topology patterns.
  * *Random* - nodes are randomly placed about the canvas, but are not linked
    together. This can be used in conjunction with a WLAN node to quickly create a wireless network.
  * *Grid* - nodes are placed in horizontal rows starting in the upper-left
    corner, evenly spaced to the right; nodes are not linked to each other.
  * *Connected Grid* - nodes are placed in an N x M (width and height)
    rectangular grid, and each node is linked to the node above, below, left
    and right of itself.
  * *Chain* - nodes are linked together one after the other in a chain.
  * *Star* - one node is placed in the center with N nodes surrounding it in a
    circular pattern, with each node linked to the center node
  * *Cycle* - nodes are arranged in a circular pattern with every node
    connected to its neighbor to form a closed circular path.
  * *Wheel* - the wheel pattern links nodes in a combination of both Star and
    Cycle patterns.
  * *Cube* - generate a cube graph of nodes
  * *Clique* - creates a clique graph of nodes, where every node is connected
    to every other node
  * *Bipartite* - creates a bipartite graph of nodes, having two disjoint sets
    of vertices.
* *Debugger...* - opens the CORE Debugger window for executing arbitrary Tcl/Tk
  commands.

### Widgets Menu

*Widgets* are GUI elements that allow interaction with a running emulation.
Widgets typically automate the running of commands on emulated nodes to report
status information of some type and display this on screen.

#### Periodic Widgets

These Widgets are those available from the main *Widgets* menu. More than one
of these Widgets may be run concurrently. An event loop fires once every second
that the emulation is running. If one of these Widgets is enabled, its periodic
routine will be invoked at this time. Each Widget may have a configuration
dialog box which is also accessible from the *Widgets* menu.

Here are some standard widgets:

* *Adjacency* - displays router adjacency states for Quagga's OSPFv2 and OSPFv3
  routing protocols. A line is drawn from each router halfway to the router ID
  of an adjacent router. The color of the line is based on the OSPF adjacency
  state such as Two-way or Full. To learn about the different colors, see the
  *Configure Adjacency...* menu item. The **vtysh** command is used to
  dump OSPF neighbor information.
  Only half of the line is drawn because each
  router may be in a different adjacency state with respect to the other.
* *Throughput* - displays the kilobits-per-second throughput above each link,
  using statistics gathered from the ng_pipe Netgraph node that implements each
  link. If the throughput exceeds a certain threshold, the link will become
  highlighted. For wireless nodes which broadcast data to all nodes in range,
  the throughput rate is displayed next to the node and the node will become
  circled if the threshold is exceeded.

#### Observer Widgets

These Widgets are available from the *Observer Widgets* submenu of the
*Widgets* menu, and from the Widgets Tool on the toolbar. Only one Observer Widget may
be used at a time. Mouse over a node while the session is running to pop up
an informational display about that node.

Available Observer Widgets include IPv4 and IPv6 routing tables, socket
information, list of running processes, and OSPFv2/v3 neighbor information.

Observer Widgets may be edited by the user and rearranged. Choosing *Edit...*
from the Observer Widget menu will invoke the Observer Widgets dialog. A list
of Observer Widgets is displayed along with up and down arrows for rearranging
the list. Controls are available for renaming each widget, for changing the
command that is run during mouse over, and for adding and deleting items from
the list. Note that specified commands should return immediately to avoid
delays in the GUI display. Changes are saved to a **widgets.conf** file in
the CORE configuration directory.

### Session Menu

The Session Menu has entries for starting, stopping, and managing sessions,
in addition to global options such as node types, comments, hooks, servers,
and options.

* *Start* or *Stop* - this starts or stops the emulation, performing the same
  function as the green Start or red Stop button.
* *Change sessions...* - invokes the CORE Sessions dialog box containing a list
  of active CORE sessions in the daemon. Basic session information such as
  name, node count, start time, and a thumbnail are displayed. This dialog
  allows connecting to different sessions, shutting them down, or starting
  a new session.
* *Node types...* - invokes the CORE Node Types dialog, performing the same
  function as the Edit button on the Network-Layer Nodes toolbar.
* *Comments...* - invokes the CORE Session Comments window where optional
  text comments may be specified. These comments are saved at the top of the
  configuration file, and can be useful for describing the topology or how
  to use the network.
* *Hooks...* - invokes the CORE Session Hooks window where scripts may be
  configured for a particular session state. The top of the window has a list
  of configured hooks, and buttons on the bottom left allow adding, editing,
  and removing hook scripts. The new or edit button will open a hook script
  editing window.  A hook script is a shell script invoked on the host (not
  within a virtual node).
  * *definition* - used by the GUI to tell the backend to clear any state.
  * *configuration* - when the user presses the *Start* button, node, link, and
    other configuration data is sent to the backend. This state is also
    reached when the user customizes a service.
  * *instantiation* - after configuration data has been sent, just before the nodes are created.
  * *runtime* - all nodes and networks have been
    built and are running. (This is the same state at which
    the previously-named *global experiment script* was run.)
  * *datacollect* - the user has pressed the
    *Stop* button, but before services have been stopped and nodes have been
    shut down. This is a good time to collect log files and other data from the
    nodes.
  * *shutdown* - all nodes and networks have been shut down and destroyed.
* *Reset node positions* - if you have moved nodes around
  using the mouse or by using a mobility module, choosing this item will reset
  all nodes to their original position on the canvas. The node locations are
  remembered when you first press the Start button.
* *Emulation servers...* - invokes the CORE emulation
  servers dialog for configuring.
* *Change Sessions...* - invokes the Sessions dialog for switching between different
  running sessions. This dialog is presented during startup when one or
  more sessions are already running.
* *Options...* - presents per-session options, such as the IPv4 prefix to be
  used, if any, for a control network the ability to preserve
  the session directory; and an on/off switch for SDT3D support.

### Help Menu

* *Online manual (www)*, *CORE website (www)*, *Mailing list (www)* - these
  options attempt to open a web browser with the link to the specified web
  resource.
* *About* - invokes the About dialog box for viewing version information

## Connecting with Physical Networks

CORE's emulated networks run in real time, so they can be connected to live
physical networks. The RJ45 tool and the Tunnel tool help with connecting to
the real world. These tools are available from the *Link-layer nodes* menu.

When connecting two or more CORE emulations together, MAC address collisions
should be avoided. CORE automatically assigns MAC addresses to interfaces when
the emulation is started, starting with **00:00:00:aa:00:00** and incrementing
the bottom byte. The starting byte should be changed on the second CORE machine
using the *MAC addresses...* option from the *Tools* menu.

### RJ45 Tool

The RJ45 node in CORE represents a physical interface on the real CORE machine.
Any real-world network device can be connected to the interface and communicate
with the CORE nodes in real time.

The main drawback is that one physical interface is required for each
connection. When the physical interface is assigned to CORE, it may not be used
for anything else. Another consideration is that the computer or network that
you are connecting to must be co-located with the CORE machine.

To place an RJ45 connection, click on the *Link-layer nodes* toolbar and select
the *RJ45 Tool* from the submenu. Click on the canvas near the node you want to
connect to. This could be a router, hub, switch, or WLAN, for example. Now
click on the *Link Tool* and draw a link between the RJ45 and the other node.
The RJ45 node will display "UNASSIGNED". Double-click the RJ45 node to assign a
physical interface. A list of available interfaces will be shown, and one may
be selected by double-clicking its name in the list, or an interface name may
be entered into the text box.

**NOTE:**
   When you press the Start button to instantiate your topology, the
   interface assigned to the RJ45 will be connected to the CORE topology. The
   interface can no longer be used by the system. For example, if there was an
   IP address assigned to the physical interface before execution, the address
   will be removed and control given over to CORE. No IP address is needed; the
   interface is put into promiscuous mode so it will receive all packets and
   send them into the emulated world.

Multiple RJ45 nodes can be used within CORE and assigned to the same physical
interface if 802.1x VLANs are used. This allows for more RJ45 nodes than
physical ports are available, but the (e.g. switching) hardware connected to
the physical port must support the VLAN tagging, and the available bandwidth
will be shared.

You need to create separate VLAN virtual devices on the Linux host,
and then assign these devices to RJ45 nodes inside of CORE. The VLANning is
actually performed outside of CORE, so when the CORE emulated node receives a
packet, the VLAN tag will already be removed.

Here are example commands for creating VLAN devices under Linux:

```shell
ip link add link eth0 name eth0.1 type vlan id 1
ip link add link eth0 name eth0.2 type vlan id 2
ip link add link eth0 name eth0.3 type vlan id 3
```

### Tunnel Tool

The tunnel tool builds GRE tunnels between CORE emulations or other hosts.
Tunneling can be helpful when the number of physical interfaces is limited or
when the peer is located on a different network. Also a physical interface does
not need to be dedicated to CORE as with the RJ45 tool.

The peer GRE tunnel endpoint may be another CORE machine or another
host that supports GRE tunneling. When placing a Tunnel node, initially
the node will display "UNASSIGNED". This text should be replaced with the IP
address of the tunnel peer. This is the IP address of the other CORE machine or
physical machine, not an IP address of another virtual node.

**NOTE:**
   Be aware of possible MTU issues with GRE devices. The *gretap* device
   has an interface MTU of 1,458 bytes; when joined to a Linux bridge, the
   bridge's MTU
   becomes 1,458 bytes. The Linux bridge will not perform fragmentation for
   large packets if other bridge ports have a higher MTU such as 1,500 bytes.

The GRE key is used to identify flows with GRE tunneling. This allows multiple
GRE tunnels to exist between that same pair of tunnel peers. A unique number
should be used when multiple tunnels are used with the same peer. When
configuring the peer side of the tunnel, ensure that the matching keys are
used.

Here are example commands for building the other end of a tunnel on a Linux
machine. In this example, a router in CORE has the virtual address
**10.0.0.1/24** and the CORE host machine has the (real) address
**198.51.100.34/24**.  The Linux box
that will connect with the CORE machine is reachable over the (real) network
at **198.51.100.76/24**.
The emulated router is linked with the Tunnel Node. In the
Tunnel Node configuration dialog, the address **198.51.100.76** is entered, with
the key set to **1**. The gretap interface on the Linux box will be assigned
an address from the subnet of the virtual router node,
**10.0.0.2/24**.
```shell
# these commands are run on the tunnel peer
sudo ip link add gt0 type gretap remote 198.51.100.34 local 198.51.100.76 key 1
sudo ip addr add 10.0.0.2/24 dev gt0
sudo ip link set dev gt0 up
```


Now the virtual router should be able to ping the Linux machine:

```shell
# from the CORE router node
ping 10.0.0.2
```

And the Linux machine should be able to ping inside the CORE emulation:

```shell
# from the tunnel peer
ping 10.0.0.1
```

To debug this configuration, **tcpdump** can be run on the gretap devices, or
on the physical interfaces on the CORE or Linux machines. Make sure that a
firewall is not blocking the GRE traffic.

### Communicating with the Host Machine

The host machine that runs the CORE GUI and/or daemon is not necessarily
accessible from a node. Running an X11 application on a node, for example,
requires some channel of communication for the application to connect with
the X server for graphical display. There are several different ways to
connect from the node to the host and vice versa.


#### Control Network

The quickest way to connect with the host machine through the primary control network.

With a control network, the host can launch an X11 application on a node.
To run an X11 application on the node, the **SSH** service can be enabled on
the node, and SSH with X11 forwarding can be used from the host to the node:

```shell
# SSH from host to node n5 to run an X11 app
ssh -X 172.16.0.5 xclock
```

Note that the **coresendmsg** utility can be used for a node to send
messages to the CORE daemon running on the host (if the **listenaddr = 0.0.0.0**
is set in the **/etc/core/core.conf** file) to interact with the running
emulation. For example, a node may move itself or other nodes, or change
its icon based on some node state.

#### Other Methods

There are still other ways to connect a host with a node. The RJ45 Tool
can be used in conjunction with a dummy interface to access a node:

```shell
sudo modprobe dummy numdummies=1
```

A **dummy0** interface should appear on the host. Use the RJ45 tool assigned
to **dummy0**, and link this to a node in your scenario. After starting the
session, configure an address on the host.

```shell
sudo brctl show
# determine bridge name from the above command
# assign an IP address on the same network as the linked node
sudo ip addr add 10.0.1.2/24 dev b.48304.34658
```

In the example shown above, the host will have the address **10.0.1.2** and
the node linked to the RJ45 may have the address **10.0.1.1**.

## Building Sample Networks

### Wired Networks

Wired networks are created using the *Link Tool* to draw a link between two
nodes. This automatically draws a red line representing an Ethernet link and
creates new interfaces on network-layer nodes.

Double-click on the link to invoke the *link configuration* dialog box. Here
you can change the Bandwidth, Delay, Loss, and Duplicate
rate parameters for that link. You can also modify the color and width of the
link, affecting its display.

Link-layer nodes are provided for modeling wired networks. These do not create
a separate network stack when instantiated, but are implemented using Linux bridging.
These are the hub, switch, and wireless LAN nodes. The hub copies each packet from
the incoming link to every connected link, while the switch behaves more like an
Ethernet switch and keeps track of the Ethernet address of the connected peer,
forwarding unicast traffic only to the appropriate ports.

The wireless LAN (WLAN) is covered in the next section.

### Wireless Networks

The wireless LAN node allows you to build wireless networks where moving nodes
around affects the connectivity between them. The wireless LAN, or WLAN, node
appears as a small cloud. The WLAN offers several levels of wireless emulation
fidelity, depending on your modeling needs.

The WLAN tool can be extended with plug-ins for different levels of wireless
fidelity. The basic on/off range is the default setting available on all
platforms. Other plug-ins offer higher fidelity at the expense of greater
complexity and CPU usage. The availability of certain plug-ins varies depending
on platform. See the table below for a brief overview of wireless model types.


Model|Type|Supported Platform(s)|Fidelity|Description
-----|----|---------------------|--------|-----------
|Basic|on/off|Linux|Low|Ethernet bridging with ebtables
|EMANE|Plug-in|Linux|High|TAP device connected to EMANE emulator with pluggable MAC and PHY radio types

To quickly build a wireless network, you can first place several router nodes
onto the canvas. If you have the
Quagga MDR software installed, it is
recommended that you use the *mdr* node type for reduced routing overhead. Next
choose the *wireless LAN* from the *Link-layer nodes* submenu. First set the
desired WLAN parameters by double-clicking the cloud icon. Then you can link
all of the routers by right-clicking on the WLAN and choosing *Link to all
routers*.

Linking a router to the WLAN causes a small antenna to appear, but no red link
line is drawn. Routers can have multiple wireless links and both wireless and
wired links (however, you will need to manually configure route
redistribution.) The mdr node type will generate a routing configuration that
enables OSPFv3 with MANET extensions. This is a Boeing-developed extension to
Quagga's OSPFv3 that reduces flooding overhead and optimizes the flooding
procedure for mobile ad-hoc (MANET) networks.

The default configuration of the WLAN is set to use the basic range model,
using the *Basic* tab in the WLAN configuration dialog.  Having this model
selected causes **core-daemon** to calculate the distance between nodes based
on screen pixels. A numeric range in screen pixels is set for the wireless
network using the *Range* slider. When two wireless nodes are within range of
each other, a green line is drawn between them and they are linked.  Two
wireless nodes that are farther than the range pixels apart are not linked.
During Execute mode, users may move wireless nodes around by clicking and
dragging them, and wireless links will be dynamically made or broken.

The *EMANE* tab lists available EMANE models to use for wireless networking.
See the [EMANE](emane.md) chapter for details on using EMANE.

### Mobility Scripting

CORE has a few ways to script mobility.

* ns-2 script - the script specifies either absolute positions
  or waypoints with a velocity. Locations are given with Cartesian coordinates.
* CORE API - an external entity can move nodes by sending CORE API Node
  messages with updated X,Y coordinates; the **coresendmsg** utility
  allows a shell script to generate these messages.
* EMANE events - see [EMANE](emane.md) for details on using EMANE scripts to move
  nodes around. Location information is typically given as latitude, longitude,
  and altitude.

For the first method, you can create a mobility script using a text
editor, or using a tool such as [BonnMotion](http://net.cs.uni-bonn.de/wg/cs/applications/bonnmotion/),  and associate the script with one of the wireless
using the WLAN configuration dialog box. Click the *ns-2 mobility script...*
button, and set the *mobility script file* field in the resulting *ns2script*
configuration dialog.

Here is an example for creating a BonnMotion script for 10 nodes:

```shell
bm -f sample RandomWaypoint -n 10 -d 60 -x 1000 -y 750
bm NSFile -f sample
# use the resulting 'sample.ns_movements' file in CORE
```

When the Execute mode is started and one of the WLAN nodes has a mobility
script, a mobility script window will appear. This window contains controls for
starting, stopping, and resetting the running time for the mobility script. The
*loop* checkbox causes the script to play continuously. The *resolution* text
box contains the number of milliseconds between each timer event; lower values
cause the mobility to appear smoother but consumes greater CPU time.

The format of an ns-2 mobility script looks like:

```shell
# nodes: 3, max time: 35.000000, max x: 600.00, max y: 600.00
$node_(2) set X_ 144.0
$node_(2) set Y_ 240.0
$node_(2) set Z_ 0.00
$ns_ at 1.00 "$node_(2) setdest 130.0 280.0 15.0"
```

The first three lines set an initial position for node 2. The last line in the
above example causes node 2 to move towards the destination **(130, 280)** at
speed **15**. All units are screen coordinates, with speed in units per second.
The total script time is learned after all nodes have reached their waypoints.
Initially, the time slider in the mobility script dialog will not be
accurate.

Examples mobility scripts (and their associated topology files) can be found in the **configs/** directory.

## Multiple Canvases

CORE supports multiple canvases for organizing emulated nodes. Nodes running on
different canvases may be linked together.

To create a new canvas, choose *New* from the *Canvas* menu. A new canvas tab
appears in the bottom left corner. Clicking on a canvas tab switches to that
canvas. Double-click on one of the tabs to invoke the *Manage Canvases* dialog
box. Here, canvases may be renamed and reordered, and you can easily switch to
one of the canvases by selecting it.

Each canvas maintains its own set of nodes and annotations. To link between
canvases, select a node and right-click on it, choose *Create link to*, choose
the target canvas from the list, and from that submenu the desired node. A
pseudo-link will be drawn, representing the link between the two nodes on
different canvases. Double-clicking on the label at the end of the arrow will
jump to the canvas that it links.

Distributed Emulation
---------------------

A large emulation scenario can be deployed on multiple emulation servers and
controlled by a single GUI. The GUI, representing the entire topology, can be
run on one of the emulation servers or on a separate machine. Emulations can be
distributed on Linux.

Each machine that will act as an emulation server needs to have CORE installed.
It is not important to have the GUI component but the CORE Python daemon
**core-daemon** needs to be installed.  Set the **listenaddr** line in the
**/etc/core/core.conf** configuration file so that the CORE Python
daemon will respond to commands from other servers:

```shell
### core-daemon configuration options ###
[core-daemon]
pidfile = /var/run/core-daemon.pid
logfile = /var/log/core-daemon.log
listenaddr = 0.0.0.0
```


The **listenaddr** should be set to the address of the interface that should
receive CORE API control commands from the other servers; setting **listenaddr
= 0.0.0.0** causes the Python daemon to listen on all interfaces. CORE uses TCP
port 4038 by default to communicate from the controlling machine (with GUI) to
the emulation servers. Make sure that firewall rules are configured as
necessary to allow this traffic.

In order to easily open shells on the emulation servers, the servers should be
running an SSH server, and public key login should be enabled. This is
accomplished by generating an SSH key for your user if you do not already have
one (use **ssh-keygen -t rsa**), and then copying your public key to the
authorized_keys file on the server (for example, **ssh-copy-id user@server** or
**scp ~/.ssh/id_rsa.pub server:.ssh/authorized_keys**.) When double-clicking on
a node during runtime, instead of opening a local shell, the GUI will attempt
to SSH to the emulation server to run an interactive shell. The user name used
for these remote shells is the same user that is running the CORE GUI.

**HINT: Here is a quick distributed emulation checklist.**

1. Install the CORE daemon on all servers.
2. Configure public-key SSH access to all servers (if you want to use
double-click shells or Widgets.)
3. Set **listenaddr=0.0.0.0** in all of the server's core.conf files,
then start (or restart) the daemon.
4. Select nodes, right-click them, and choose *Assign to* to assign
the servers (add servers through *Session*, *Emulation Servers...*)
5. Press the *Start* button to launch the distributed emulation.

Servers are configured by choosing *Emulation servers...* from the *Session*
menu. Servers parameters are configured in the list below and stored in a
*servers.conf* file for use in different scenarios. The IP address and port of
the server must be specified. The name of each server will be saved in the
topology file as each node's location.

**NOTE:**
   The server that the GUI connects with
   is referred to as the master server.

The user needs to assign nodes to emulation servers in the scenario. Making no
assignment means the node will be emulated on the master  server
In the configuration window of every node, a drop-down box located between
the *Node name* and the *Image* button will select the name of the emulation
server. By default, this menu shows *(none)*, indicating that the node will
be emulated locally on the master. When entering Execute mode, the CORE GUI
will deploy the node on its assigned emulation server.

Another way to assign emulation servers is to select one or more nodes using
the select tool (shift-click to select multiple), and right-click one of the
nodes and choose *Assign to...*.

The *CORE emulation servers* dialog box may also be used to assign nodes to
servers. The assigned server name appears in parenthesis next to the node name.
To assign all nodes to one of the servers, click on the server name and then
the *all nodes* button. Servers that have assigned nodes are shown in blue in
the server list. Another option is to first select a subset of nodes, then open
the *CORE emulation servers* box and use the *selected nodes* button.

**IMPORTANT:**
   Leave the nodes unassigned if they are to be run on the master server.
   Do not explicitly assign the nodes to the master server.

The emulation server machines should be reachable on the specified port and via
SSH. SSH is used when double-clicking a node to open a shell, the GUI will open
an SSH prompt to that node's emulation server. Public-key authentication should
be configured so that SSH passwords are not needed.

If there is a link between two nodes residing on different servers, the GUI
will draw the link with a dashed line, and automatically create necessary
tunnels between the nodes when executed. Care should be taken to arrange the
topology such that the number of tunnels is minimized. The tunnels carry data
between servers to connect nodes as specified in the topology.
These tunnels are created using GRE tunneling, similar to the Tunnel Tool.

Wireless nodes, i.e. those connected to a WLAN node, can be assigned to
different emulation servers and participate in the same wireless network
only if an
EMANE model is used for the WLAN. The basic range model does not work across multiple servers due
to the Linux bridging and ebtables rules that are used.

**NOTE:**
   The basic range wireless model does not support distributed emulation,
   but EMANE does.

## Services

CORE uses the concept of services to specify what processes or scripts run on a
node when it is started. Layer-3 nodes such as routers and PCs are defined by
the services that they run.

Services may be customized for each node, or new custom services can be
created. New node types can be created each having a different name, icon, and
set of default services. Each service defines the per-node directories,
configuration files, startup index, starting commands, validation commands,
shutdown commands, and meta-data associated with a node.

**NOTE:**
   Network namespace nodes do not undergo the normal Linux boot process
   using the **init**, **upstart**, or **systemd** frameworks. These
   lightweight nodes use configured CORE *services*.

### Default Services and Node Types

Here are the default node types and their services:

* *router* - zebra, OSFPv2, OSPFv3, and IPForward services for IGP
  link-state routing.
* *host* - DefaultRoute and SSH services, representing an SSH server having a
  default route when connected directly to a router.
* *PC* - DefaultRoute service for having a default route when connected
  directly to a router.
* *mdr* - zebra, OSPFv3MDR, and IPForward services for
  wireless-optimized MANET Designated Router routing.
* *prouter* - a physical router, having the same default services as the
  *router* node type; for incorporating Linux testbed machines into an
  emulation.

Configuration files can be automatically generated by each service. For
example, CORE automatically generates routing protocol configuration for the
router nodes in order to simplify the creation of virtual networks.

To change the services associated with a node, double-click on the node to
invoke its configuration dialog and click on the *Services...* button,
or right-click a node a choose *Services...* from the menu.
Services are enabled or disabled by clicking on their names. The button next to
each service name allows you to customize all aspects of this service for this
node. For example, special route redistribution commands could be inserted in
to the Quagga routing configuration associated with the zebra service.

To change the default services associated with a node type, use the Node Types
dialog available from the *Edit* button at the end of the Layer-3 nodes
toolbar, or choose *Node types...* from the  *Session* menu. Note that
any new services selected are not applied to existing nodes if the nodes have
been customized.

The node types are saved in a **~/.core/nodes.conf** file, not with the
**.imn** file. Keep this in mind when changing the default services for
existing node types; it may be better to simply create a new node type. It is
recommended that you do not change the default built-in node types. The
**nodes.conf** file can be copied between CORE machines to save your custom
types.

### Customizing a Service

A service can be fully customized for a particular node. From the node's
configuration dialog, click on the button next to the service name to invoke
the service customization dialog for that service.
The dialog has three tabs for configuring the different aspects of the service:
files, directories, and startup/shutdown.

**NOTE:**
   A **yellow** customize icon next to a service indicates that service
   requires customization (e.g. the *Firewall* service).
   A **green** customize icon indicates that a custom configuration exists.
   Click the *Defaults* button when customizing a service to remove any
   customizations.

The Files tab is used to display or edit the configuration files or scripts that
are used for this service. Files can be selected from a drop-down list, and
their contents are displayed in a text entry below. The file contents are
generated by the CORE daemon based on the network topology that exists at
the time the customization dialog is invoked.

The Directories tab shows the per-node directories for this service. For the
default types, CORE nodes share the same filesystem tree, except for these
per-node directories that are defined by the services. For example, the
**/var/run/quagga** directory needs to be unique for each node running
the Zebra service, because Quagga running on each node needs to write separate
PID files to that directory.

**NOTE:**
   The **/var/log** and **/var/run** directories are
   mounted uniquely per-node by default.
   Per-node mount targets can be found in **/tmp/pycore.nnnnn/nN.conf/**
   (where *nnnnn* is the session number and *N* is the node number.)

The Startup/shutdown tab lists commands that are used to start and stop this
service. The startup index allows configuring when this service starts relative
to the other services enabled for this node; a service with a lower startup
index value is started before those with higher values. Because shell scripts
generated by the Files tab will not have execute permissions set, the startup
commands should include the shell name, with
something like ```sh script.sh```.

Shutdown commands optionally terminate the process(es) associated with this
service. Generally they send a kill signal to the running process using the
*kill* or *killall* commands. If the service does not terminate
the running processes using a shutdown command, the processes will be killed
when the *vnoded* daemon is terminated (with *kill -9*) and
the namespace destroyed. It is a good practice to
specify shutdown commands, which will allow for proper process termination, and
for run-time control of stopping and restarting services.

Validate commands are executed following the startup commands. A validate
command can execute a process or script that should return zero if the service
has started successfully, and have a non-zero return value for services that
have had a problem starting. For example, the *pidof* command will check
if a process is running and return zero when found. When a validate command
produces a non-zero return value, an exception is generated, which will cause
an error to be displayed in the Check Emulation Light.

**TIP:**
   To start, stop, and restart services during run-time, right-click a
   node and use the *Services...* menu.

### Creating new Services

Services can save time required to configure nodes, especially if a number
of nodes require similar configuration procedures. New services can be
introduced to automate tasks.

The easiest way to capture the configuration of a new process into a service
is by using the **UserDefined** service. This is a blank service where any
aspect may be customized. The UserDefined service is convenient for testing
ideas for a service before adding a new service type.

To introduce new service types, a **myservices/** directory exists in the
user's CORE configuration directory, at **~/.core/myservices/**. A detailed
**README.txt** file exists in that directory to outline the steps necessary
for adding a new service. First, you need to create a small Python file that
defines the service; then the **custom_services_dir** entry must be set
in the **/etc/core/core.conf** configuration file. A sample is provided in
the **myservices/** directory.

**NOTE:**
   The directory name used in **custom_services_dir** should be unique and
   should not correspond to
   any existing Python module name. For example, don't use the name **subprocess**
   or **services**.

If you have created a new service type that may be useful to others, please
consider contributing it to the CORE project.

## Check Emulation Light

The |cel| Check Emulation Light, or CEL, is located in the bottom right-hand corner
of the status bar in the CORE GUI. This is a yellow icon that indicates one or
more problems with the running emulation. Clicking on the CEL will invoke the
CEL dialog.

The Check Emulation Light dialog contains a list of exceptions received from
the CORE daemon. An exception has a time, severity level, optional node number,
and source. When the CEL is blinking, this indicates one or more fatal
exceptions. An exception with a fatal severity level indicates that one or more
of the basic pieces of emulation could not be created, such as failure to
create a bridge or namespace, or the failure to launch EMANE processes for an
EMANE-based network.

Clicking on an exception displays details for that
exception. If a node number is specified, that node is highlighted on the
canvas when the exception is selected. The exception source is a text string
to help trace where the exception occurred; "service:UserDefined" for example,
would appear for a failed validation command with the UserDefined service.

Buttons are available at the bottom of the dialog for clearing the exception
list and for viewing the CORE daemon and node log files.

**NOTE:**
   In batch mode, exceptions received from the CORE daemon are displayed on
   the console.

## Configuration Files

Configurations are saved to **xml** or **.imn** topology files using
the *File* menu. You
can easily edit these files with a text editor.
Any time you edit the topology
file, you will need to stop the emulation if it were running and reload the
file.

The **.xml** [file schema is specified by NRL](http://www.nrl.navy.mil/itd/ncs/products/mnmtools) and there are two versions to date:
version 0.0  and version 1.0,
with 1.0 as the current default. CORE can open either XML version. However, the
xmlfilever line in **/etc/core/core.conf** controls the version of the XML file
that CORE will create.

In version 1.0, the XML file is also referred to as the Scenario Plan. The Scenario Plan will be logically
made up of the following:

* **Network Plan** - describes nodes, hosts, interfaces, and the networks to
  which they belong.
* **Motion Plan** - describes position and motion patterns for nodes in an
  emulation.
* **Services Plan** - describes services (protocols, applications) and traffic
  flows that are associated with certain nodes.
* **Visualization Plan** - meta-data that is not part of the NRL XML schema but
  used only by CORE. For example, GUI options, canvas and annotation info, etc.
  are contained here.
* **Test Bed Mappings** - describes mappings of nodes, interfaces and EMANE modules in the scenario to
  test bed hardware.
  CORE includes Test Bed Mappings in XML files that are saved while the scenario is running.


The **.imn** file format comes from IMUNES, and is
basically Tcl lists of nodes, links, etc.
Tabs and spacing in the topology files are important. The file starts by
listing every node, then links, annotations, canvases, and options. Each entity
has a block contained in braces. The first block is indented by four spaces.
Within the **network-config** block (and any *custom-*-config* block), the
indentation is one tab character.

**TIP:**
   There are several topology examples included with CORE in
   the **configs/** directory.
   This directory can be found in **~/.core/configs**, or
   installed to the filesystem
   under **/usr[/local]/share/examples/configs**.

**TIP:**
   When using the **.imn** file format, file paths for things like custom
   icons may contain the special variables **$CORE_DATA_DIR** or **$CONFDIR** which
   will be substituted with **/usr/share/core** or **~/.core/configs**.

**TIP:**
   Feel free to edit the files directly using your favorite text editor.

## Customizing your Topology's Look

Several annotation tools are provided for changing the way your topology is
presented. Captions may be added with the Text tool. Ovals and rectangles may
be drawn in the background, helpful for visually grouping nodes together.

During live demonstrations the marker tool may be helpful for drawing temporary
annotations on the canvas that may be quickly erased. A size and color palette
appears at the bottom of the toolbar when the marker tool is selected. Markings
are only temporary and are not saved in the topology file.

The basic node icons can be replaced with a custom image of your choice. Icons
appear best when they use the GIF or PNG format with a transparent background.
To change a node's icon, double-click the node to invoke its configuration
dialog and click on the button to the right of the node name that shows the
node's current icon.

A background image for the canvas may be set using the *Wallpaper...* option
from the *Canvas* menu. The image may be centered, tiled, or scaled to fit the
canvas size. An existing terrain, map, or network diagram could be used as a
background, for example, with CORE nodes drawn on top.

## Preferences

The *Preferences* Dialog can be accessed from the **Edit_Menu**. There are
numerous defaults that can be set with this dialog, which are stored in the
**~/.core/prefs.conf** preferences file.



