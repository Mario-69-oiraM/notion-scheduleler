echo "# Auto build from buildContainer script"  > token.sh
echo export NOTION_TOKEN=$NOTION_TOKEN >> token.sh
echo export PYTHONPATH=/app/appRequirements >> token.sh

docker build -t my-python --build-arg NOTION_TOKEN=$NOTION_TOKEN .
