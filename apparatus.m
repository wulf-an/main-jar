# BloodHound 
BloodHound is a cybersecurity tool that maps a company's network as a visual graph to reveal hidden pathways a hacker could take to gain administrative control. It works by converting complex network permissions into nodes and edges, then executing graph traversal algorithms—like Breadth-First Search (BFS) and Dijkstra's Algorithm to calculate the shortest attack route, Depth-First Search (DFS) to resolve nested group permissions, and Community Detection to identify critical choke points—allowing security teams to locate and close those secret vulnerabilities before attackers can exploit them.


# webhook
webhook.site

# mermaid.live
create diagram

# Online-Hosted Vulnerable Environments
https://ginandjuice.shop/
https://duck-store.escape.tech/
https://dvaib.com/
https://pentest-ground.com/
http://testasp.vulnweb.com/Login.asp




#httpx 
httpx -l unique_subs.txt -o live_hosts.txt

# nc (netcat):

nc example.com 80

GET / HTTP/1.1
Host: example.com
Connection: close


# curl 
-X : Specifies the HTTP request method to use (e.g., POST, GET, DELETE).
-H : Adds a custom header to the HTTP request (used for content types, user-agents, etc.).
-b : Passes cookie data to the server (tells curl to behave like a browser with active cookies).
-d : Sends the specified data in a POST request to the server (the request body).
-v : Enables verbose mode, printing the full request and response headers for debugging.

curl https://facebook.com
curl -i -L http://facebook.com   

(i- show headers), (L - follow redirection) (I- only for response headers).

# canyouseeme
https://canyouseeme.org/

# Pinggy
ssh -p 443 -R0:127.0.0.1:8080 qr@a.pinggy.io



# vuln web
https://pentest-ground.com/



# Reonnaissance 

## Passive Recon Tools:
1. whois & RDAP
- https://whois.icann.org/ (legacy WHOIS)
- https://lookup.icann.org/ (modern RDAP-focused lookup)
- https://www.whoxy.com/ (historical WHOIS snapshots, free limited use)
2. nslookup
3. dig
4. Censys.io
5. subfinder
6. amass


## Active recon :

nmap
rustscan
mass scan



rustscan -a 3.79.202.74 --range 1-65535





brutespray/noble 1.8.1-2 all
  Python bruteforce tool

ncrack/noble 0.7+debian-5ubuntu1 amd64
  High-speed network authentication cracking tool
