#!/bin/bash
# Elastic Beanstalk Initialization Script
# This script initializes an EB application and creates an environment

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
APP_NAME="${EB_APP_NAME:-blacklist-api}"
ENV_NAME="${EB_ENV_NAME:-blacklist-api-env}"
REGION="${AWS_REGION:-us-east-1}"
PLATFORM="${EB_PLATFORM:-python-3.12}"
INSTANCE_TYPE="${EB_INSTANCE_TYPE:-t3.small}"
MIN_INSTANCES="${EB_MIN_INSTANCES:-3}"
MAX_INSTANCES="${EB_MAX_INSTANCES:-6}"

# Database configuration (from Terraform outputs or manual input)
DB_HOST="${DB_HOST:-team-11-rds-db-postgres.c906624kg3ro.us-east-1.rds.amazonaws.com}"
DB_NAME="${DB_NAME:-postgres}"
DB_USER="${DB_USER:-db_user}"
DB_PASSWORD="${DB_PASSWORD:-db_password}"
DB_PORT="${DB_PORT:-5432}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Elastic Beanstalk Initialization${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verify EB CLI is installed
if ! command_exists eb; then
    echo -e "${RED}Error: EB CLI is not installed${NC}"
    echo "Install it with: pip install awsebcli"
    exit 1
fi

# Verify AWS CLI is installed
if ! command_exists aws; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    echo "Install it with: pip install awscli"
    exit 1
fi

# Check AWS credentials
echo -e "${YELLOW}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo -e "${RED}Error: AWS credentials not configured${NC}"
    echo "Configure with: aws configure"
    exit 1
fi
echo -e "${GREEN}✓ AWS credentials found${NC}"

# Construct DATABASE_URL
if [ -n "$DB_HOST" ]; then
    DATABASE_URL="postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
    echo -e "${GREEN}✓ Database URL configured${NC}"
else
    DATABASE_URL="sqlite:///app.db"
    echo -e "${YELLOW}⚠ Using SQLite (not recommended for production)${NC}"
fi

# Initialize Elastic Beanstalk application
echo -e "\n${BLUE}Step 1: Initializing EB application...${NC}"
if ! eb init "$APP_NAME" --region "$REGION" --platform "$PLATFORM"; then
    echo -e "${RED}Error: Failed to initialize EB application${NC}"
    exit 1
fi
echo -e "${GREEN}✓ EB application initialized${NC}"

# Create environment
echo -e "\n${BLUE}Step 2: Creating EB environment...${NC}"
echo -e "${YELLOW}This may take 5-10 minutes...${NC}"

eb create "$ENV_NAME" \
    --instance-type "$INSTANCE_TYPE" \
    --min-instances "$MIN_INSTANCES" \
    --max-instances "$MAX_INSTANCES" \
    --envvars \
        DATABASE_URL="$DATABASE_URL"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ EB environment created successfully${NC}"
else
    echo -e "${RED}Error: Failed to create EB environment${NC}"
    exit 1
fi

# Get environment info
echo -e "\n${BLUE}Step 3: Getting environment information...${NC}"
eb status

# Save configuration
echo -e "\n${BLUE}Step 4: Saving configuration...${NC}"
cat > .eb_config <<EOF
# Elastic Beanstalk Configuration
export EB_APP_NAME="$APP_NAME"
export EB_ENV_NAME="$ENV_NAME"
export AWS_REGION="$REGION"
export EB_PLATFORM="$PLATFORM"
export EB_INSTANCE_TYPE="$INSTANCE_TYPE"
export EB_MIN_INSTANCES="$MIN_INSTANCES"
export EB_MAX_INSTANCES="$MAX_INSTANCES"
EOF

echo -e "${GREEN}✓ Configuration saved to .eb_config${NC}"

# Print summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Initialization Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Application Name:${NC} $APP_NAME"
echo -e "${YELLOW}Environment Name:${NC} $ENV_NAME"
echo -e "${YELLOW}Region:${NC} $REGION"
echo -e "${YELLOW}Instance Type:${NC} $INSTANCE_TYPE"
echo -e "${YELLOW}Min Instances:${NC} $MIN_INSTANCES"
echo -e "${YELLOW}Max Instances:${NC} $MAX_INSTANCES"

# Get environment URL
ENV_URL=$(eb status | grep "CNAME" | awk '{print $2}')
if [ -n "$ENV_URL" ]; then
    echo -e "${YELLOW}Environment URL:${NC} http://$ENV_URL"
    echo -e "\n${BLUE}Test the application:${NC}"
    echo -e "  curl http://$ENV_URL/ping"
    echo -e "  curl http://$ENV_URL/health"
fi

echo -e "\n${BLUE}Next steps:${NC}"
echo -e "  1. Load config: ${YELLOW}source .eb_config${NC}"
echo -e "  2. Deploy: ${YELLOW}./eb_deploy_<policy>.sh${NC}"
echo -e "  3. Test different policies: ${YELLOW}./eb_test_deployments.sh${NC}"
echo -e "  4. Monitor: ${YELLOW}eb logs${NC}"