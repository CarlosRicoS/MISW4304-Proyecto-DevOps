#!/bin/bash
# Deploy with Rolling deployment policy
# Updates instances in batches, no extra capacity

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

BATCH_SIZE="${EB_BATCH_SIZE:-1}"
BATCH_TYPE="${EB_BATCH_TYPE:-Fixed}"  # Fixed or Percentage

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploying with Rolling Policy${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "${YELLOW}Policy Details:${NC}"
echo -e "  • Updates instances in batches"
echo -e "  • ${YELLOW}Reduced capacity during deployment${NC}"
echo -e "  • No downtime (if health checks pass)"
echo -e "  • Slower than All-at-Once"
echo -e "  • Batch Size: $BATCH_SIZE ($BATCH_TYPE)"

# Create deployment config
mkdir -p .ebextensions/saved_configs
cat > .ebextensions/deployment.config <<EOF
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: Rolling
    Timeout: 900
    IgnoreHealthCheck: false
    BatchSize: $BATCH_SIZE
    BatchSizeType: $BATCH_TYPE

  aws:autoscaling:asg:
    MinSize: ${EB_MIN_INSTANCES:-3}
    MaxSize: ${EB_MAX_INSTANCES:-6}
    Cooldown: 360

  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    Statistic: Average
    Unit: Percent
    UpperThreshold: 80
    LowerThreshold: 20
EOF

echo -e "\n${YELLOW}Starting deployment...${NC}"
START_TIME=$(date +%s)

# Deploy
if eb deploy --timeout 30; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Deployment Successful${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}Deployment Time:${NC} ${DURATION}s"
    echo -e "${YELLOW}Policy:${NC} Rolling (Batch: $BATCH_SIZE)"
    
    # Get environment URL
    ENV_URL=$(eb status | grep "CNAME" | awk '{print $2}')
    if [ -n "$ENV_URL" ]; then
        echo -e "${YELLOW}URL:${NC} http://$ENV_URL"
        
        # Test endpoint
        echo -e "\n${BLUE}Testing health endpoint...${NC}"
        sleep 5
        if curl -sf "http://$ENV_URL/ping" > /dev/null; then
            echo -e "${GREEN}✓ Application is responding${NC}"
            
            # Check all instances
            echo -e "\n${BLUE}Instance Health:${NC}"
            eb health --refresh
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
echo -e "${BLUE}Monitor:${NC} eb health --refresh"