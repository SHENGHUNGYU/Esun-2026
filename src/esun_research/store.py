"""Content-addressed files with an append-only capture index."""
import hashlib
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from .contracts import instant, now

def encoded(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def immutable(path: Path, body: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        tmp = Path(f.name)
        f.write(body)
        f.flush()
        os.fsync(f.fileno())
    try:
        try:
            os.link(tmp, path)
        except FileExistsError:
            if path.read_bytes() != body:
                raise ValueError(f'Immutable artifact conflict: {path.name}')
    finally:
        tmp.unlink(missing_ok=True)

class Store:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS captures (
                id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, fetched_at TEXT NOT NULL,
                epoch REAL NOT NULL, status TEXT NOT NULL, ref TEXT, error TEXT,
                UNIQUE(source_id, fetched_at, status, ref))''')

    def connect(self):
        return sqlite3.connect(self.root / 'index.sqlite', timeout=30)

    def put(self, body: bytes, suffix='json') -> str:
        if suffix not in {'json','bin'}:
            raise ValueError('Unsupported artifact suffix')
        ref = f'objects/{digest(body)}.{suffix}'
        immutable(self.root / ref, body)
        return ref

    def put_json(self, value) -> str:
        return self.put(encoded(value))

    def read(self, ref: str) -> bytes:
        p = self.root / ref
        if not p.resolve().is_relative_to(self.root / 'objects'):
            raise ValueError('Invalid artifact reference')
        body = p.read_bytes()
        if digest(body) != p.stem:
            raise ValueError('Artifact hash mismatch')
        return body

    def json(self, ref: str):
        return json.loads(self.read(ref))

    def capture(self, source_id, body=None, error=None, fetched_at=None):
        when = fetched_at or now()
        epoch = instant(when).timestamp()
        ref = self.put(body, 'bin') if body is not None else None
        status = 'ok' if body is not None and error is None else 'error'
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO captures(source_id,fetched_at,epoch,status,ref,error) VALUES(?,?,?,?,?,?)',
                       (source_id, when, epoch, status, ref, error))
        return {'source_id':source_id,'fetched_at':when,'status':status,'ref':ref,'error':error}

    def select(self, source_id, cutoff_at):
        with self.connect() as db:
            db.row_factory = sqlite3.Row
            r = db.execute('SELECT * FROM captures WHERE source_id=? AND epoch<=? ORDER BY epoch DESC,id DESC LIMIT 1',
                           (source_id, instant(cutoff_at).timestamp())).fetchone()
            if not r:
                return {'source_id':source_id,'status':'missing','error':'no_capture_before_cutoff','ref':None}
            result = dict(r)
            if r['ref']:
                first = db.execute('SELECT fetched_at FROM captures WHERE source_id=? AND ref=? ORDER BY epoch,id LIMIT 1',
                                   (source_id,r['ref'])).fetchone()
                result['first_seen_at'] = first[0]
            return result

    def freeze(self, request, sources, namespace='research'):
        if namespace not in {'research','candidates'}:
            raise ValueError('Unsupported run namespace')
        folder = self.root / namespace / request.run_id
        manifest = folder / 'request.json'
        body = request.model_dump(mode='json')
        if manifest.exists():
            saved = json.loads(manifest.read_bytes())
            if saved['request'] != body:
                raise ValueError('run_id already bound to different request/code/model')
            # Verify every referenced artifact on resume; never silently reselect new data.
            for c in saved['captures'].values():
                if c.get('ref'):
                    self.read(c['ref'])
            return saved
        saved = {'request':body,'captures':{s.id:self.select(s.id,request.cutoff_at) for s in sources}}
        immutable(manifest, encoded(saved))
        return saved

