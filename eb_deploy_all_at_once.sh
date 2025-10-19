#!/bin/bash
# Deploy with All-at-Once deployment policy
# Fastest deployment but causes downtime

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Load configuration
if [ -f .eb_config ]; then
    source .eb_config
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploying with All-at-Once Policy${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "${YELLOW}Policy Details:${NC}"
echo -e "  • All instances updated simultaneously"
echo -e "  • ${RED}CAUSES DOWNTIME${NC}"
echo -e "  • Fastest deployment method"
echo -e "  • Immediate rollback if issues"

# Create temporary deployment config
mkdir -p .ebextensions/saved_configs
cat > .ebextensions/deployment.config <<EOF
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: AllAtOnce
    Timeout: 600
    IgnoreHealthCheck: false

  aws:autoscaling:asg:
    MinSize: ${EB_MIN_INSTANCES:-3}
    MaxSize: ${EB_MAX_INSTANCES:-6}
    Cooldown: 360
EOF

echo -e "\n${YELLOW}Starting deployment...${NC}"
START_TIME=$(date +%s)

# Deploy
if eb deploy --timeout 20; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Deployment Successful${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}Deployment Time:${NC} ${DURATION}s"
    echo -e "${YELLOW}Policy:${NC} All-at-Once"
    
    # Get environment URL
    ENV_URL=$(eb status | grep "CNAME" | awk '{print $2}')
    if [ -n "$ENV_URL" ]; then
        echo -e "${YELLOW}URL:${NC} http://$ENV_URL"
        
        # Test endpoint
        echo -e "\n${BLUE}Testing health endpoint...${NC}"
        sleep 10  # Wait for app to be ready
        if curl -sf "http://$ENV_URL/ping" > /dev/null; then
            echo -e "${GREEN}✓ Application is responding${NC}"
        else
            echo -e "${RED}⚠ Application not responding yet${NC}"
        fi
    fi
else
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Deployment Failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo -e "${YELLOW}Duration:${NC} ${DURATION}s"

    exit 1
fi

echo -e "\n${BLUE}View logs:${NC} eb logs"
echo -e "${BLUE}Monitor:${NC} eb health"