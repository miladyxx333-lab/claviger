#!/bin/bash
# Claviger Forge Deployment Script

echo "🚀 Preparing Claviger Forge for Cloudflare..."

# 1. Zip the skill
echo "📦 Bundling Claviger Skill..."
cd ..
zip -r claviger_skill.zip ../deer-flow/skills/custom/claviger/* -x "*/venv/*" "*/__pycache__/*" "*.log"
cp claviger_skill.zip worker/public/

# 2. Check for wrangler
if ! command -v npx &> /dev/null
then
    echo "❌ Error: npx not found. Please install Node.js."
    exit
fi

echo "✨ Ready to deploy!"
echo "Run the following command to go live:"
echo "npx wrangler deploy"
