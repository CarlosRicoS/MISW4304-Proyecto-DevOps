#!/bin/bash
# Deploy with Immutable deployment policy
# Creates new instances, swaps, then terminates old ones

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
echo -e "${BLUE}Deploying with Immutable Policy${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "${YELLOW}Policy Details:${NC}"
echo -e "  • Creates entirely new instances"
echo -e "  • ${GREEN}Zero downtime${NC}"
echo -e "  • ${GREEN}Quick rollback capability${NC}"
echo -e "  • Requires double capacity temporarily"
echo -e "  • Safest deployment method"
echo -e "  • Longest deployment time"

# Create deployment config
mkdir -p .ebextensions/saved_configs
cat > .ebextensions/deployment.config <<EOF
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: Immutable
    Timeout: 1200
    IgnoreHealthCheck: false

  aws:autoscaling:asg:
    MinSize: ${EB_MIN_INSTANCES:-3}
    MaxSize: ${EB_MAX_INSTANCES:-6}
    Cooldown: 360

  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    Statistic: Average
    Unit: Percent
    UpperThreshold: 80
    UpperBreachScaleIncrement: 1
    LowerThreshold: 20
    LowerBreachScaleIncrement: -1
    BreachDuration: 5
    EvaluationPeriods: 1
    Period: 5
EOF

echo -e "\n${YELLOW}Starting deployment...${NC}"
echo -e "${YELLOW}This will take longer due to instance provisioning${NC}"
START_TIME=$(date +%s)

# Deploy
if eb deploy --timeout 40; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Deployment Successful${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}Deployment Time:${NC} ${DURATION}s"
    echo -e "${YELLOW}Policy:${NC} Immutable"
    
    # Get environment URL
    ENV_URL=$(eb status | grep "CNAME" | awk '{print $2}')
    if [ -n "$ENV_URL" ]; then
        echo -e "${YELLOW}URL:${NC} http://$ENV_URL"
        
        # Test endpoint
        echo -e "\n${BLUE}Testing health endpoint...${NC}"
        sleep 5
        if curl -sf "http://$ENV_URL/ping" > /dev/null; then
            echo -e "${GREEN}✓ Application is responding${NC}"
            
            # Detailed health check
            echo -e "\n${BLUE}Performing detailed health check...${NC}"
            RESPONSE=$(curl -s "http://$ENV_URL/health")
            echo -e "${GREEN}Health Response:${NC} $RESPONSE"
            
            # Check instance health
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
    echo -e "${YELLOW}Note:${NC} Failed instances were automatically terminated"

    
    exit 1
fi

echo -e "\n${BLUE}View logs:${NC} eb logs"
echo -e "${BLUE}Monitor:${NC} eb health --refresh"
echo -e "${BLUE}View events:${NC} eb events"