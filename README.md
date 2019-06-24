# Quick Overview Video:
https://www.youtube.com/watch?v=jz-FSPdoL-w

https://www.youtube.com/watch?v=ehYXVCzd1Gs

# RTFM
Tool used for enumeration, reporting, and automating low hanging fruit during a penetration test.

# Overview:
1. Framework dir is the main tool, that will help automate common pen testing tasks.  It must have at least libnmap, and the Setup.py script ran alone will install it, but it will install a lot of other things as well, and could take about an hour.  main.py will run the entire script.
2. ToolUpdater is a C# tool used to add new command lines, mostly just a copy of the Kali tools page.

- Attack.py: Keeps a collection of possible attack vectors with the exploits.  Automatically populated by searchsploit, probably 95% of attacks are not applicable.
- Checklist.py: Used to keep a record of what has been checked or tried.  Keeps notes, and outputs to a report.
- CustomTools.py: More complex use of tools that would be difficult to make data driven.
- Enumeration.py: Facilitates nmap, tshark, nikto, tcpdump, few other tools, and can be used for local enumeration.
- Exploit.py: Specifically runs tools for exploiting.  More intelligent then the tool list.
- main.py: Starts the program.  Use `Python3 main.py -s debug12345` to load an existing session.
- Maintain.py: Used to help maintain access on a compromised machine, but not working on because I don't think it's needed for OSCP.
- MenuBase.py: Base class for menus.
- NmapScripts.py: Custom tools that are all utilizing Nmap.
- Parsers.py: Custom parsing logic used to better integrate output from various tools and create a collaborative process.
- Screen.py: Main menu screen.
- Session.py: Keep the session data, saves and loads the session/s, and generates the reports.
- Setup.py: Can be used alone, or part of the program.  Installed required software, and ensures rapid deployment on new Kali machines.
- Shells.py: Collection of reverse shells that are outputted with the host IP and port, plain text, base64, and simple encryption.
- TargetHost.py: Keeps information on the target, and will output a report whenever the session is saved.
- Templates.py: Contains steps for standard attacks based on the enumerated information previously gathered.
- Tool.py: Tool class used to categorize and contain a meaning of a tool in Kali or Windows.
- ToolManager.py: Used to execute tools on the system.
- tools.json/tools_win.json: Json collection of tools that can be ran by the ToolManager.  Can be created in the ToolUpdate project.
