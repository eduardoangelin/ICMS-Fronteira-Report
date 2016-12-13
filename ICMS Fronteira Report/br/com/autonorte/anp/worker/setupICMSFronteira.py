from distutils.core import setup
import py2exe
import numpy
import matplotlib

setup(console=['br/com/autonorte/anp/worker/ICMS_Fronteira.py'],
	data_files=matplotlib.get_py2exe_datafiles(),
	options = { "py2exe": { 
        "dll_excludes": ['libzmq.dll', 'libzmq.pyd'],
        'excludes': ['zmq.libzmq', '_gtkagg', '_tkagg'],
        "includes": ["decimal", "datetime"] } }
	)
