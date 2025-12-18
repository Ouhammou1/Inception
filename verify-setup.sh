RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
 



#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "=== Inception Project Verification ==="
echo ""

echo "1. Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "2. Network Connectivity:"
# Test nginx to wordpress (port 9000)
docker exec nginx timeout 2 bash -c "echo > /dev/tcp/wordpress/9000" 2>/dev/null \
&& echo -e "${GREEN}✓ Nginx → WordPress (PHP-FPM): OK${NC}" \
|| echo -e "${RED}✗ Nginx → WordPress: FAILED${NC}"

# Test wordpress to mariadb
docker exec wordpress timeout 2 mysqladmin ping -h mariadb \
-u$(wp config get DB_USER --allow-root 2>/dev/null) \
-p$(wp config get DB_PASSWORD --allow-root 2>/dev/null) 2>/dev/null \
&& echo -e "${GREEN}✓ WordPress → MariaDB: OK${NC}" \
|| echo -e "${RED}✗ WordPress → MariaDB: FAILED${NC}"

echo ""
echo "3. Service Accessibility:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -k https://localhost 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "301" ]; then
    echo -e "${GREEN}✓ HTTPS (443): Accessible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ HTTPS (443): Not accessible (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo "4. WordPress Installation:"
docker exec wordpress wp core is-installed --allow-root 2>/dev/null \
&& echo -e "${GREEN}✓ WordPress: Installed${NC}" \
|| echo -e "${RED}✗ WordPress: Not installed${NC}"

echo ""
echo "5. Database Content:"
USERS=$(docker exec wordpress wp user list --format=count --allow-root 2>/dev/null || echo "0")
POSTS=$(docker exec wordpress wp post list --format=count --allow-root 2>/dev/null || echo "0")
echo "   Users: $USERS | Posts: $POSTS"

echo ""
echo "6. SSL Certificate:"
docker exec nginx openssl x509 -in /etc/nginx/ssl/nginx.crt -noout -subject 2>/dev/null | cut -d'=' -f2- \
|| echo -e "${RED}Certificate not found${NC}"

echo ""
echo "7. Volume Persistence Check:"
ls -ld /home/bouhammo/data/ 2>/dev/null \
&& echo -e "${GREEN}✓ Data directory exists${NC}" \
|| echo -e "${RED}✗ Data directory missing${NC}"

ls -ld /home/bouhammo/data/wp/ 2>/dev/null \
&& echo -e "${GREEN}✓ WordPress volume exists${NC}" \
|| echo -e "${RED}✗ WordPress volume missing${NC}"

ls -ld /home/bouhammo/data/maria/ 2>/dev/null \
&& echo -e "${GREEN}✓ MariaDB volume exists${NC}" \
|| echo -e "${RED}✗ MariaDB volume missing${NC}"

echo ""
echo "=== Verification Complete ==="
