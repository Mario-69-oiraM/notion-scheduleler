if [ -d "/app/tempClone" ] 
then
    echo "Directory /path/to/dir exists." 
    cd /app/tempClone
    git pull https://mario-69-mario@github.com/Mario-69-Mario/notion-scheduleler
else
    echo "Error: Directory /app/tempClone does not exists."
    mkdir /app/tempClone
    cd /app/tempClone
    git clone https://mario-69-mario@github.com/Mario-69-Mario/notion-scheduleler /app/tempClone
fi


cd /app
cp /app/tempClone/*.py /app

python3 /app/notion-scheduleler.py
