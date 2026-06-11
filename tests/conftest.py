from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path


TEST_DB = Path(tempfile.gettempdir()) / f'radar_financeiro_backend_test_{uuid.uuid4().hex}.db'
os.environ.setdefault('RADAR_ENV', 'test')
os.environ['RADAR_DATABASE_URL'] = f"sqlite:///{str(TEST_DB).replace('\\', '/')}"
os.environ.setdefault('RADAR_ALLOW_TEST_AUTH', 'true')

import app.database as database

database.init_db()
