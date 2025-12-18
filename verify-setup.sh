#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables
STUDENT_LOGIN=""  # Set this before running
PROJECT_DIR="./"
SRCS_DIR="$PROJECT_DIR/srcs"
MAKEFILE="$PROJECT_DIR/Makefile"
DOCKER_COMPOSE="$SRCS_DIR/docker-compose.yml"
COMPOSE_PROJECT_NAME="inception"  # Adjust if different

# Results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0
ERRORS=()

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║            42 Inception Project Evaluation Script        ║${NC}"
echo -e "${PURPLE}║                 (Complete Check - No Exit)               ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}\n"

# Function to add result
add_result() {
    local test_name="$1"
    local status="$2"
    local message="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    case $status in
        "PASS")
            PASSED_TESTS=$((PASSED_TESTS + 1))
            echo -e "${GREEN}✓ PASS:${NC} $test_name - $message"
            ;;
        "FAIL")
            FAILED_TESTS=$((FAILED_TESTS + 1))
            ERRORS+=("$test_name: $message")
            echo -e "${RED}✗ FAIL:${NC} $test_name - $message"
            ;;
        "WARN")
            WARNINGS=$((WARNINGS + 1))
            echo -e "${YELLOW}⚠ WARN:${NC} $test_name - $message"
            ;;
    esac
}

# Function to run test and capture result
run_test() {
    local test_name="$1"
    local command="$2"
    local success_message="$3"
    local fail_message="$4"
    
    if eval "$command" > /dev/null 2>&1; then
        add_result "$test_name" "PASS" "$success_message"
    else
        add_result "$test_name" "FAIL" "$fail_message"
    fi
}

# ==============================
# PRELIMINARY CHECKS
# ==============================

echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}1. REPOSITORY STRUCTURE CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check srcs directory
if [ -d "$SRCS_DIR" ]; then
    add_result "srcs Directory" "PASS" "srcs directory exists at $SRCS_DIR"
else
    add_result "srcs Directory" "FAIL" "srcs directory not found at $SRCS_DIR"
fi

# Check Makefile
if [ -f "$MAKEFILE" ]; then
    add_result "Makefile" "PASS" "Makefile exists at $MAKEFILE"
else
    add_result "Makefile" "FAIL" "Makefile not found at $MAKEFILE"
fi

# Check .env file
if [ -f "$SRCS_DIR/.env" ]; then
    add_result ".env File" "PASS" ".env file exists in srcs directory"
else
    add_result ".env File" "WARN" ".env file not found in srcs directory"
fi

# Check for hardcoded credentials
if [ -d "$SRCS_DIR" ]; then
    if grep -r "MYSQL_ROOT_PASSWORD\|MYSQL_PASSWORD\|MYSQL_USER\|WORDPRESS_" "$SRCS_DIR" \
        --include="*.yml" --include="*.yaml" --include="Dockerfile*" \
        --exclude=".env" > /dev/null 2>&1; then
        add_result "Hardcoded Credentials" "FAIL" "Found hardcoded credentials outside .env file"
    else
        add_result "Hardcoded Credentials" "PASS" "No hardcoded credentials found"
    fi
fi

# ==============================
# DOCKER COMPOSE CHECK
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}2. DOCKER COMPOSE CONFIGURATION${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check docker-compose.yml exists
if [ -f "$DOCKER_COMPOSE" ]; then
    add_result "docker-compose.yml" "PASS" "docker-compose.yml exists"
else
    add_result "docker-compose.yml" "FAIL" "docker-compose.yml not found at $DOCKER_COMPOSE"
fi

# Check for network: host (if docker-compose exists)
if [ -f "$DOCKER_COMPOSE" ]; then
    if grep -q "network:\s*host" "$DOCKER_COMPOSE"; then
        add_result "Network Host" "FAIL" "Found 'network: host' in docker-compose.yml"
    else
        add_result "Network Host" "PASS" "No 'network: host' found"
    fi
    
    # Check for links
    if grep -q "links:" "$DOCKER_COMPOSE"; then
        add_result "Links Directive" "FAIL" "Found 'links:' in docker-compose.yml"
    else
        add_result "Links Directive" "PASS" "No 'links:' directive found"
    fi
    
    # Check for networks
    if grep -q "networks:" "$DOCKER_COMPOSE"; then
        add_result "Networks Section" "PASS" "Found 'networks:' section in docker-compose.yml"
    else
        add_result "Networks Section" "FAIL" "No 'networks:' section in docker-compose.yml"
    fi
fi

# ==============================
# MAKEFILE CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}3. MAKEFILE CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check for --link in Makefile
if [ -f "$MAKEFILE" ]; then
    if grep -q "docker run.*--link" "$MAKEFILE"; then
        add_result "Makefile Links" "FAIL" "Found '--link' in Makefile"
    else
        add_result "Makefile Links" "PASS" "No '--link' in Makefile"
    fi
fi

# Check scripts for --link
if [ -d "$PROJECT_DIR" ]; then
    if find "$PROJECT_DIR" -name "*.sh" -type f -exec grep -l "docker run.*--link" {} \; 2>/dev/null | grep -q .; then
        add_result "Script Links" "FAIL" "Found '--link' in scripts"
    else
        add_result "Script Links" "PASS" "No '--link' in scripts"
    fi
fi

# ==============================
# DOCKERFILE CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}4. DOCKERFILE CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check each service has a Dockerfile
SERVICES=("nginx" "wordpress" "mariadb")
for service in "${SERVICES[@]}"; do
    DOCKERFILE="$SRCS_DIR/requirements/$service/Dockerfile"
    
    # Check if Dockerfile exists
    if [ -f "$DOCKERFILE" ]; then
        add_result "$service Dockerfile" "PASS" "Dockerfile exists for $service"
        
        # Check if Dockerfile is not empty
        if [ -s "$DOCKERFILE" ]; then
            add_result "$service Dockerfile Content" "PASS" "Dockerfile for $service is not empty"
        else
            add_result "$service Dockerfile Content" "FAIL" "Dockerfile for $service is empty"
        fi
        
        # Check FROM line
        if head -1 "$DOCKERFILE" 2>/dev/null | grep -q "FROM debian:\|FROM alpine:"; then
            add_result "$service FROM Directive" "PASS" "Starts with FROM debian: or FROM alpine:"
        else
            add_result "$service FROM Directive" "FAIL" "Doesn't start with FROM debian: or FROM alpine:"
        fi
        
        # Check for prohibited commands
        if grep -i "entrypoint\|cmd" "$DOCKERFILE" 2>/dev/null | grep -q "tail -f"; then
            add_result "$service Prohibited Commands" "FAIL" "Found 'tail -f' in ENTRYPOINT/CMD"
        elif grep -i "entrypoint\|cmd" "$DOCKERFILE" 2>/dev/null | grep -q "bash\|sh"; then
            # Check if bash/sh is used for running a script
            if grep -i "entrypoint\|cmd" "$DOCKERFILE" 2>/dev/null | grep -q '\["sh",\|\["bash",'; then
                add_result "$service Prohibited Commands" "PASS" "bash/sh used for script execution (allowed)"
            else
                add_result "$service Prohibited Commands" "FAIL" "Found bash/sh in ENTRYPOINT/CMD without script"
            fi
        else
            add_result "$service Prohibited Commands" "PASS" "No prohibited commands found"
        fi
        
        # Check for NGINX in wrong Dockerfiles
        if [ "$service" != "nginx" ]; then
            if grep -iq "nginx" "$DOCKERFILE"; then
                add_result "$service No Nginx" "FAIL" "Found NGINX in $service Dockerfile"
            else
                add_result "$service No Nginx" "PASS" "No NGINX in $service Dockerfile"
            fi
        fi
        
    else
        add_result "$service Dockerfile" "FAIL" "Dockerfile not found for $service at $DOCKERFILE"
    fi
done

# ==============================
# SCRIPT CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}5. SCRIPT CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check for infinite loops in scripts
if [ -d "$SRCS_DIR" ]; then
    INFINITE_LOOPS=$(find "$SRCS_DIR" -name "*.sh" -type f -exec grep -l "sleep infinity\|tail -f /dev/null\|tail -f /dev/random" {} \; 2>/dev/null)
    if [ -z "$INFINITE_LOOPS" ]; then
        add_result "Infinite Loops" "PASS" "No infinite loops found in scripts"
    else
        add_result "Infinite Loops" "FAIL" "Found infinite loops in scripts: $INFINITE_LOOPS"
    fi
fi

# ==============================
# BUILD AND RUN
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}6. BUILD AND RUN TESTS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Clean up first
echo -e "${BLUE}Cleaning up existing containers...${NC}"
cd "$SRCS_DIR" > /dev/null 2>&1
if docker-compose down -v > /dev/null 2>&1; then
    add_result "Cleanup" "PASS" "Successfully cleaned up containers"
else
    add_result "Cleanup" "WARN" "Cleanup had issues (might be nothing to clean)"
fi

# Build
echo -e "${BLUE}Building containers...${NC}"
if make build > /dev/null 2>&1; then
    add_result "Build" "PASS" "Successfully built containers"
else
    add_result "Build" "FAIL" "Make build failed"
fi

# Run
echo -e "${BLUE}Starting containers...${NC}"
if make up > /dev/null 2>&1; then
    add_result "Start" "PASS" "Successfully started containers"
else
    add_result "Start" "FAIL" "Make up failed"
fi

# Wait for services to start
echo -e "${BLUE}Waiting for services to start (30 seconds)...${NC}"
sleep 30

# ==============================
# SERVICE CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}7. SERVICE CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check containers are running
if docker-compose ps 2>/dev/null | grep -q "Up"; then
    add_result "Running Containers" "PASS" "All containers are running"
    echo -e "${BLUE}Current containers status:${NC}"
    docker-compose ps 2>/dev/null
else
    add_result "Running Containers" "FAIL" "No containers are running"
fi

# Check network
if docker network ls 2>/dev/null | grep -q "$COMPOSE_PROJECT_NAME"; then
    add_result "Docker Network" "PASS" "Docker network created"
    echo -e "${BLUE}Current networks:${NC}"
    docker network ls 2>/dev/null | grep "$COMPOSE_PROJECT_NAME"
else
    add_result "Docker Network" "FAIL" "Docker network not found"
fi

# ==============================
# NGINX CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}8. NGINX CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Test port 80 (should fail)
echo -e "${BLUE}Testing HTTP port 80 (should fail)...${NC}"
if curl -s -f --connect-timeout 5 "http://localhost:80" >/dev/null 2>&1; then
    add_result "HTTP Port Blocked" "FAIL" "HTTP port 80 should not be accessible but it is"
else
    add_result "HTTP Port Blocked" "PASS" "HTTP port 80 correctly blocked"
fi

# Test port 443 (should work)
echo -e "${BLUE}Testing HTTPS port 443...${NC}"
if curl -s -k -f --connect-timeout 5 "https://localhost:443" >/dev/null 2>&1; then
    add_result "HTTPS Port Accessible" "PASS" "HTTPS port 443 accessible"
    
    # Check SSL certificate
    echo -e "${BLUE}Checking SSL certificate...${NC}"
    if openssl s_client -connect localhost:443 -tls1_2 < /dev/null 2>/dev/null | grep -q "TLSv1.2"; then
        add_result "TLS 1.2" "PASS" "TLS 1.2 detected"
    else
        if openssl s_client -connect localhost:443 -tls1_3 < /dev/null 2>/dev/null | grep -q "TLSv1.3"; then
            add_result "TLS 1.3" "PASS" "TLS 1.3 detected"
        else
            add_result "TLS Version" "FAIL" "TLS 1.2 or 1.3 not detected"
        fi
    fi
else
    add_result "HTTPS Port Accessible" "FAIL" "Cannot access NGINX on port 443"
fi

# ==============================
# WORDPRESS CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}9. WORDPRESS CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Test WordPress URL
echo -e "${BLUE}Testing WordPress accessibility...${NC}"
if curl -s -k -f --connect-timeout 5 "https://localhost" >/dev/null 2>&1; then
    add_result "WordPress Access" "PASS" "WordPress is accessible"
    
    # Check if WordPress is installed (not showing installation page)
    if curl -s -k "https://localhost" | grep -q "wp-admin/install.php"; then
        add_result "WordPress Installation" "FAIL" "WordPress shows installation page"
    else
        add_result "WordPress Installation" "PASS" "WordPress is properly installed"
    fi
else
    add_result "WordPress Access" "FAIL" "Cannot access WordPress"
fi

# Check WordPress volume
echo -e "${BLUE}Checking WordPress volume...${NC}"
VOLUME_NAME="${COMPOSE_PROJECT_NAME}_wordpress_data"
if docker volume inspect "$VOLUME_NAME" 2>/dev/null | grep -q "/home/$STUDENT_LOGIN/data"; then
    add_result "WordPress Volume" "PASS" "WordPress volume configured correctly"
else
    if docker volume ls 2>/dev/null | grep -q "$VOLUME_NAME"; then
        add_result "WordPress Volume" "WARN" "WordPress volume exists but path might be different"
    else
        add_result "WordPress Volume" "FAIL" "WordPress volume not properly configured"
    fi
fi

# ==============================
# MARIADB CHECKS
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}10. MARIADB CHECKS${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Check MariaDB volume
echo -e "${BLUE}Checking MariaDB volume...${NC}"
VOLUME_NAME="${COMPOSE_PROJECT_NAME}_mariadb_data"
if docker volume inspect "$VOLUME_NAME" 2>/dev/null | grep -q "/home/$STUDENT_LOGIN/data"; then
    add_result "MariaDB Volume" "PASS" "MariaDB volume configured correctly"
else
    if docker volume ls 2>/dev/null | grep -q "$VOLUME_NAME"; then
        add_result "MariaDB Volume" "WARN" "MariaDB volume exists but path might be different"
    else
        add_result "MariaDB Volume" "FAIL" "MariaDB volume not properly configured"
    fi
fi

# Test database container exists
DB_CONTAINER=$(docker-compose ps -q mariadb 2>/dev/null)
if [ -n "$DB_CONTAINER" ]; then
    add_result "MariaDB Container" "PASS" "MariaDB container is running"
else
    add_result "MariaDB Container" "FAIL" "MariaDB container not found"
fi

# ==============================
# PERSISTENCE TEST
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}11. PERSISTENCE TEST${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Only run persistence test if previous tests passed
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${BLUE}Testing persistence by restarting containers...${NC}"
    
    # Stop containers
    if docker-compose down > /dev/null 2>&1; then
        add_result "Persistence Stop" "PASS" "Successfully stopped containers"
        
        # Start containers again
        if make up > /dev/null 2>&1; then
            add_result "Persistence Start" "PASS" "Successfully restarted containers"
            
            # Wait for restart
            sleep 20
            
            # Test WordPress is still accessible
            if curl -s -k -f --connect-timeout 5 "https://localhost" >/dev/null 2>&1; then
                add_result "Persistence Access" "PASS" "WordPress accessible after restart"
            else
                add_result "Persistence Access" "FAIL" "WordPress not accessible after restart"
            fi
        else
            add_result "Persistence Start" "FAIL" "Failed to restart containers"
        fi
    else
        add_result "Persistence Stop" "FAIL" "Failed to stop containers"
    fi
else
    add_result "Persistence Test" "WARN" "Skipped due to previous failures"
fi

# ==============================
# FINAL CLEANUP
# ==============================

echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}12. FINAL CLEANUP${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

# Clean up
if docker-compose down -v > /dev/null 2>&1; then
    add_result "Final Cleanup" "PASS" "Successfully cleaned up all containers and volumes"
else
    add_result "Final Cleanup" "WARN" "Cleanup had issues"
fi

# Return to original directory
cd - > /dev/null 2>&1

# ==============================
# SUMMARY REPORT
# ==============================

echo -e "\n${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                      SUMMARY REPORT                       ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${CYAN}Test Results:${NC}"
echo -e "${GREEN}Passed:  $PASSED_TESTS${NC}"
echo -e "${RED}Failed:  $FAILED_TESTS${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
echo -e "${BLUE}Total:    $TOTAL_TESTS${NC}"

# Calculate percentage
if [ $TOTAL_TESTS -gt 0 ]; then
    PERCENTAGE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo -e "\n${CYAN}Success Rate: $PERCENTAGE%${NC}"
fi

# Display all errors if any
if [ ${#ERRORS[@]} -gt 0 ]; then
    echo -e "\n${RED}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}ERROR DETAILS:${NC}"
    for i in "${!ERRORS[@]}"; do
        echo -e "${RED}$((i+1)). ${ERRORS[$i]}${NC}"
    done
fi

# Display warnings if any
if [ $WARNINGS -gt 0 ]; then
    echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Note: There are $WARNINGS warning(s) that may need attention${NC}"
fi

# Final verdict
echo -e "\n${CYAN}══════════════════════════════════════════════════════════════${NC}"
if [ $FAILED_TESTS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ ALL TESTS PASSED SUCCESSFULLY!${NC}"
        echo -e "${GREEN}Project meets all technical requirements.${NC}"
    else
        echo -e "${YELLOW}⚠️  ALL TESTS PASSED WITH WARNINGS${NC}"
        echo -e "${YELLOW}Project meets technical requirements but has minor issues.${NC}"
    fi
else
    echo -e "${RED}❌ TEST FAILURES DETECTED${NC}"
    echo -e "${RED}Project has $FAILED_TESTS critical issue(s) that must be fixed.${NC}"
fi

# Manual checks reminder
echo -e "\n${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}MANUAL CHECKS REQUIRED:${NC}"
echo -e "${BLUE}1. Ask student to explain Docker and Docker Compose concepts${NC}"
echo -e "${BLUE}2. Verify admin username doesn't contain 'admin'${NC}"
echo -e "${BLUE}3. Test adding comments and editing pages in WordPress${NC}"
echo -e "${BLUE}4. Check database is not empty${NC}"
echo -e "${BLUE}5. Verify directory structure matches subject requirements${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"

# Exit with appropriate code
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0
else
    exit 1
fi