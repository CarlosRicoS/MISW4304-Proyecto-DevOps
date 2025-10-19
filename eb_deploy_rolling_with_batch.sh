#!/bin/bash
# Deploy with Rolling with Additional Batch policy
# Creates extra instances first, then updates in batches

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
echo -e "${BLUE}Deploying with Rolling + Additional Batch${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "${YELLOW}Policy Details:${NC}"
echo -e "  • Creates additional instances first"
echo -e "  • ${GREEN}Maintains full capacity${NC}"
echo -e "  • Updates existing instances in batches"
echo -e "  • No downtime, no reduced capacity"
echo -e "  • Moderate deployment time"
echo -e "  • Good balance of safety and speed"
echo -e "  • Batch Size: $BATCH_SIZE ($BATCH_TYPE)"

# Create deployment config
mkdir -p .ebextensions/saved_configs
cat > .ebextensions/deployment.config <<EOF
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: RollingWithAdditionalBatch
    Timeout: 1000
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

  aws:elasticbeanstalk:healthreporting:system:
    SystemType: enhanced
    EnhancedHealthAuthEnabled: true
EOF

echo -e "\n${YELLOW}Starting deployment...${NC}"
START_TIME=$(date +%s)

# Deploy
if eb deploy --timeout 35; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Deployment Successful${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}Deployment Time:${NC} ${DURATION}s"
    echo -e "${YELLOW}Policy:${NC} Rolling with Additional Batch (Batch: $BATCH_SIZE)"

    # Get environment URL
    ENV_URL=$(eb status | grep "CNAME" | awk '{print $2}')
    if [ -n "$ENV_URL" ]; then
        echo -e "${YELLOW}URL:${NC} http://$ENV_URL"

        # Test endpoints
        echo -e "\n${BLUE}Testing application endpoints...${NC}"
        sleep 5

        # Test ping
        if curl -sf "http://$ENV_URL/ping" > /dev/null; then
            echo -e "${GREEN}✓ Ping endpoint responding${NC}"
        fi

        # Test health
        if curl -sf "http://$ENV_URL/health" > /dev/null; then
            echo -e "${GREEN}✓ Health endpoint responding${NC}"
        fi

        # Check instance health
        echo -e "\n${BLUE}Instance Health Summary:${NC}"
        eb health --refresh

        # Get instance count
        INSTANCE_COUNT=$(eb health | grep -c "Ok" || echo "0")
        echo -e "${YELLOW}Healthy Instances:${NC} $INSTANCE_COUNT"
    fi

    # Save deployment stats
    echo "$(date),RollingWithBatch,${DURATION},success,$BATCH_SIZE" >> deployment_stats.csv
else
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Deployment Failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo -e "${YELLOW}Duration:${NC} ${DURATION}s"

    # Save deployment stats
    echo "$(date),RollingWithBatch,${DURATION},failed,$BATCH_SIZE" >> deployment_stats.csv

    echo -e "\n${YELLOW}Checking logs for errors...${NC}"
    eb logs --stream

    exit 1
fi

echo -e "\n${BLUE}Monitoring Commands:${NC}"
echo -e "  eb logs           - View application logs"
echo -e "  eb health         - Check instance health"
echo -e "  eb events         - View recent events"
echo -e "  eb status         - Environment status"