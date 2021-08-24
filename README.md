# 538_Riddlers
Location for 538 riddler problems

## Virtual Environment (For Mac)

- Ensure you have virtualenv installed for Python 3:
`pip3 install --user virtualenv`

- Create a new environment, this will just create an environment in current location
`python3 -m venv fte`

- Activate & check where python is (it should be in the directory)
`source fte/bin/activate`
`which python`

- Able to install a requirements.txt file or just install individual libraries
`pip install -m pandas`

### Adding Julyter Notebook

```
pip install -m ipykernel
pip install -m jupyter
python -m ipykernel install --user --name=fte
jupyter notebook
```

## Poetry - This Is Cooler
<in progress>
