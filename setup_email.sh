#!/bin/bash
# Quick setup script for Resend API key

echo "Setting up Resend API key for Job Tracker..."
echo ""
echo "Your API key: re_fmF2hgy9_JNp85323QuxDa2SEw4koWsKG"
echo ""
echo "Setting it as a Cloudflare secret..."

wrangler secret put RESEND_API_KEY <<EOF
re_fmF2hgy9_JNp85323QuxDa2SEw4koWsKG
EOF

echo ""
echo "✅ API key set successfully!"
echo "Now deploy your worker: wrangler deploy"

