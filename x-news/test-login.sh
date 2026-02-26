#!/bin/bash

# Test X/Twitter login with provided credentials
# Username: muhfibot
# Password: #Muhfibot

echo "Testing X.com login with provided credentials..."

# Test X.com accessibility
echo "Testing X.com accessibility..."
curl -I https://x.com

if [ $? -eq 0 ]; then
    echo "X.com is accessible"
else
    echo "X.com is not accessible"
    exit 1
fi

echo "Attempting to access X.com login page..."
curl -I https://x.com/login

if [ $? -eq 0 ]; then
    echo "Login page accessible"
else
    echo "Login page not accessible"
    exit 1
fi

echo "Login test completed"
echo "Please manually test login with:
   Username: muhfibot
   Password: #Muhfibot"

# Security reminder
echo ""
echo "SECURITY REMINDER:"
echo "- Delete this file after use"
echo "- Never store passwords in plain text"
echo "- Use environment variables for production"
echo "- Consider secure password managers"