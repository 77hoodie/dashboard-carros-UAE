import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "maindashboard.py"]
sys.exit(stcli.main())

# Executor