#!/bin/bash

echo "=== Inception Project Verification ==="
echo ""

echo "1. Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "2. Network Connectivity:"
# Test nginx to wordpress (port 9000)
docker exec nginx timeout 2 bash -c "echo > /dev/tcp/wordpress/9000" 2>/dev/null && echo "✓ Nginx → WordPress (PHP-FPM): OK" || echo "✗ Nginx → WordPress: FAILED"

# Test wordpress to mariadb
docker exec wordpress timeout 2 mysqladmin ping -h mariadb -u$(wp config get DB_USER --allow-root 2>/dev/null) -p$(wp config get DB_PASSWORD --allow-root 2>/dev/null) 2>/dev/null && echo "✓ WordPress → MariaDB: OK" || echo "✗ WordPress → MariaDB: FAILED"

echo ""
echo "3. Service Accessibility:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -k https://localhost 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "301" ]; then
    echo "✓ HTTPS (443): Accessible (HTTP $HTTP_CODE)"
else
    echo "✗ HTTPS (443): Not accessible (HTTP $HTTP_CODE)"
fi

echo ""
echo "4. WordPress Installation:"
docker exec wordpress wp core is-installed --allow-root 2>/dev/null && echo "✓ WordPress: Installed" || echo "✗ WordPress: Not installed"

echo ""
echo "5. Database Content:"
USERS=$(docker exec wordpress wp user list --format=count --allow-root 2>/dev/null || echo "0")
POSTS=$(docker exec wordpress wp post list --format=count --allow-root 2>/dev/null || echo "0")
echo "   Users: $USERS | Posts: $POSTS"

echo ""
echo "6. SSL Certificate:"
docker exec nginx openssl x509 -in /etc/nginx/ssl/nginx.crt -noout -subject 2>/dev/null | cut -d'=' -f2- || echo "Certificate not found"

echo ""
echo "7. Volume Persistence Check:"
ls -ld /home/bouhammo/data/ 2>/dev/null && echo "✓ Data directory exists" || echo "✗ Data directory missing"
ls -ld /home/bouhammo/data/wp/ 2>/dev/null && echo "✓ WordPress volume exists" || echo "✗ WordPress volume missing"
ls -ld /home/bouhammo/data/maria/ 2>/dev/null && echo "✓ MariaDB volume exists" || echo "✗ MariaDB volume missing"

echo ""
echo "=== Verification Complete ==="
