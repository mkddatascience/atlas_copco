# atlas_copco
# clone the repo
`git clone http://23.29.118.76:3000/kowshik/atlas_copco`
# create a virtual environment
`apt install python3.10-venv`

`python3.10 -m venv venv`
# activate the virtual environment
`source venv/bin/activate`
# install the requirements
`pip install -r requirements.txt`
# run the app using gunicorn 
`gunicorn -b 0.0.0.0:4000 atlas_copco:app --workers=1 --daemon`

