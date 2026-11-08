"""Consistent, checksummed private migration package. Stop writers first."""
import argparse
import hashlib
import json
import shutil
import sqlite3
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def snapshot(project,destination):
    project=project.resolve();destination=destination.resolve()
    if destination.exists():raise ValueError('snapshot destination already exists')
    destination.mkdir(parents=True);target=destination/'snapshot';target.mkdir()
    records={};excluded=[]
    for source in sorted(project.rglob('*')):
        rel=source.relative_to(project);parts=rel.parts
        if any(x in {'.git','.venv','.uv-cache','__pycache__','.pytest_cache','node_modules','graphify-out'} for x in parts):continue
        if parts[:2]==('output','migration'):continue
        if not source.is_file():continue
        if source.name.startswith('.env') and source.name!='.env.example' or source.suffix in {'.pem','.key'} or source.name in {'id_rsa','id_ed25519'}:
            excluded.append(str(rel));continue
        if source.name.endswith(('-wal','-shm','-journal')):continue
        if source.is_symlink():raise ValueError('review symlink before packaging: '+str(rel))
        dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        with source.open('rb') as f:is_sqlite=f.read(16)==b'SQLite format 3\x00'
        if is_sqlite:
            with sqlite3.connect(source.as_uri()+'?mode=ro',uri=True) as origin,sqlite3.connect(dest) as replica:
                origin.backup(replica)
                if replica.execute('PRAGMA quick_check').fetchone()[0]!='ok':raise ValueError('sqlite integrity failed: '+str(rel))
        else:shutil.copy2(source,dest)
        records[str(rel)]={'sha256':sha(dest),'bytes':dest.stat().st_size,'sqlite_backup':is_sqlite}
    metadata={'created_at':datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),'source_root':str(project),
              'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=project,text=True).strip(),
              'git_status':subprocess.check_output(['git','status','--short'],cwd=project,text=True),
              'files':records,'excluded_credentials':excluded,'total_bytes':sum(r['bytes'] for r in records.values())}
    (target/'MIGRATION_MANIFEST.json').write_text(json.dumps(metadata,ensure_ascii=False,sort_keys=True,indent=2))
    archive=destination/'esun-private-snapshot.tar.gz'
    with tarfile.open(archive,'w:gz') as tar:tar.add(target,arcname='snapshot')
    (destination/'archive.sha256').write_text(sha(archive)+'  '+archive.name+'\n')
    print(json.dumps({'archive':str(archive),'sha256':sha(archive),'files':len(records),'data_bytes':metadata['total_bytes'],'archive_bytes':archive.stat().st_size,'sqlite_databases':sum(r['sqlite_backup'] for r in records.values()),'excluded_credentials':excluded},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--project',type=Path,required=True);parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args();snapshot(args.project,args.destination)
