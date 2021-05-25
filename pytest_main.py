import shutil

import pytest

if __name__ == '__main__':
    pytest.main(['--alluredir', './result'])
    shutil.copy('test_config/environment.properties', 'result/environment.properties')
