import unittest,sys,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build_plan import parse_todo,public_doc_sources
class PlanContract(unittest.TestCase):
 def setUp(self):self.text=(ROOT/'DAILY_TODO.md').read_text()
 def test_approval_gate(self):
  with self.assertRaisesRegex(ValueError,'acceptance not confirmed'):parse_todo(self.text.replace('- 狀態：待驗收','- 狀態：已完成',1))
  with self.assertRaisesRegex(ValueError,'list not confirmed'):parse_todo(self.text.replace('2026-10-08 使用者指示執行 U01','未確認',1))
 def test_dependency_gate(self):
  text=self.text.replace('## U02 開發與模型底座\n\n- 階段：開發\n- 狀態：待開始','## U02 開發與模型底座\n\n- 階段：開發\n- 狀態：進行中',1).replace('- 清單確認：未確認','- 清單確認：使用者已確認',1)
  with self.assertRaisesRegex(ValueError,'dependency not accepted'):parse_todo(text)
 def test_generated_parity(self):
  tasks=parse_todo(self.text);self.assertEqual(tasks,json.loads((ROOT/'plan.json').read_text())['tasks'])
  payload=(ROOT/'site/dist/data.js').read_text();self.assertEqual(tasks,json.loads(payload.split('window.PLAN=',1)[1].split(';\nwindow.DOCS=',1)[0]))
  for name,p in public_doc_sources():self.assertEqual(p.read_bytes(),(ROOT/'site/dist/documents'/name).read_bytes())
  self.assertFalse(any((ROOT/'site/dist/documents').glob('SERVER*.md')))
  self.assertEqual([t['status'] for t in tasks],['待驗收']+['待開始']*13)
 def test_reply_field_contract(self):
  with self.assertRaisesRegex(ValueError,'invalid reply field'):parse_todo(self.text.replace('team｜隊伍與報名狀態｜','BAD KEY｜隊伍與報名狀態｜',1))
  with self.assertRaisesRegex(ValueError,'duplicate reply field'):parse_todo(self.text.replace('m3｜M3 Ultra 的存取方式｜','team｜M3 Ultra 的存取方式｜',1))
 def test_required_content_and_order(self):
  for malformed in [self.text.replace('U01 資源與規則','U02 資源與規則',1),self.text.replace('### 證據','### 未知欄位',1),self.text.replace('- 前置依賴：U01','- 前置依賴：U02',1)]:
   with self.assertRaises(ValueError):parse_todo(malformed)
if __name__=='__main__':unittest.main()
