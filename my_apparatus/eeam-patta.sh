#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Banner function
show_banner() {
    clear
    echo ""
    echo -e "${BOLD}${RED}         ███████╗███████╗ █████╗ ███╗   ███╗${NC}"
    echo -e "${BOLD}${YELLOW}         ██╔════╝██╔════╝██╔══██╗████╗ ████║${NC}"
    echo -e "${BOLD}${GREEN}         █████╗  █████╗  ███████║██╔████╔██║${NC}"
    echo -e "${BOLD}${BLUE}         ██╔══╝  ██╔══╝  ██╔══██║██║╚██╔╝██║${NC}"
    echo -e "${BOLD}${PURPLE}         ███████╗███████╗██║  ██║██║ ╚═╝ ██║${NC}"
    echo -e "${BOLD}${CYAN}         ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝${NC}"
    echo ""
    echo -e "${BOLD}${RED}         ██████╗  █████╗ ████████╗████████╗ █████╗${NC}"
    echo -e "${BOLD}${YELLOW}         ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗${NC}"
    echo -e "${BOLD}${GREEN}         ██████╔╝███████║   ██║      ██║   ███████║${NC}"
    echo -e "${BOLD}${BLUE}         ██╔═══╝ ██╔══██║   ██║      ██║   ██╔══██║${NC}"
    echo -e "${BOLD}${PURPLE}         ██║     ██║  ██║   ██║      ██║   ██║  ██║${NC}"
    echo -e "${BOLD}${CYAN}         ╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝${NC}"
    echo ""
    echo -e "${WHITE}    ════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}          Passive Subdomain Enumeration Suite v1.0 ${NC}"
    echo -e "${YELLOW}          Tools: Subfinder | Amass | crt.sh ${NC}"
    echo -e "${WHITE}    ════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Function to validate domain
validate_domain() {
    if [[ $1 =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Main script starts here
show_banner

# Domain input with example
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│${NC}  ${WHITE}Enter the target domain to enumerate${NC}                     ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${CYAN}Example: google.com${NC}                                      ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${GREEN}[+] Domain:${NC} \c"
read DOMAIN

# Check if domain is empty
if [[ -z "$DOMAIN" ]]; then
    echo -e "\n${RED}[!] No domain entered. Exiting...${NC}"
    exit 1
fi

# Validate domain format
if ! validate_domain "$DOMAIN"; then
    echo -e "\n${RED}[!] Invalid domain format!${NC}"
    echo -e "${YELLOW}[+] Please enter a valid domain (e.g., example.com)${NC}"
    exit 1
fi


echo -e "${YELLOW}[+] Starting enumeration...${NC}\n"

# Create output directory
OUTPUT_DIR="eeampatta_results"
mkdir -p "$OUTPUT_DIR"

# Timestamp for output file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="${OUTPUT_DIR}/${DOMAIN}_subdomains_${TIMESTAMP}.txt"

# Run tools with progress indicators
echo -e "${BLUE}[1/3]${NC} Running ${GREEN}Subfinder${NC}..."
subfinder -d $DOMAIN -silent > "${OUTPUT_DIR}/subs1.txt" &
PID1=$!

echo -e "${BLUE}[2/3]${NC} Running ${GREEN}Amass${NC} (passive mode)..."
amass enum -passive -d $DOMAIN -o "${OUTPUT_DIR}/subs2.txt" -silent &
PID2=$!

# Wait for both to complete
wait $PID1 $PID2

echo -e "${BLUE}[3/3]${NC} Fetching from ${GREEN}crt.sh${NC}..."
curl -s "https://crt.sh/?q=$DOMAIN&output=json" | jq -r '.[].name_value' 2>/dev/null | sed 's/\*\.//g' | sort -u > "${OUTPUT_DIR}/subs3.txt"

# Combine all sources and remove duplicates

cat "${OUTPUT_DIR}/subs1.txt" "${OUTPUT_DIR}/subs2.txt" "${OUTPUT_DIR}/subs3.txt" | sort -u > "$OUTPUT_FILE"

# Clean up temporary files
rm "${OUTPUT_DIR}/subs1.txt" "${OUTPUT_DIR}/subs2.txt" "${OUTPUT_DIR}/subs3.txt"

# Display results
TOTAL_COUNT=$(wc -l < "$OUTPUT_FILE")
echo -e "\n${GREEN}[✓] Enumeration complete!${NC}"
echo -e "${CYAN}[+] Total unique subdomains found:${NC} ${GREEN}$TOTAL_COUNT${NC}"
echo -e "${CYAN}[+] Results saved to:${NC} ${YELLOW}$OUTPUT_FILE${NC}"

# Option to display results
echo -e "\n${YELLOW}[?] Do you want to display the results? (y/n)${NC}"
read -p "➜ " DISPLAY_RESULTS

if [[ "$DISPLAY_RESULTS" =~ ^[Yy]$ ]]; then
    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Subdomains found for ${CYAN}$DOMAIN${GREEN}:${NC}"
    cat "$OUTPUT_FILE"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
fi

echo -e "\n${GREEN}[+] Eeampatta out. Happy hunting! 🦋${NC}"
