from pathlib import Path
import jsonlines

def process_starrocks_docs(root_dir: Path, output_path: Path):
    with jsonlines.open(output_path, 'w') as writer:
        for md_file in root_dir.glob('**/*.md'):
            content = md_file.read_text(encoding='utf-8')
            qa_pairs = parse_starrocks_md(content)
            
            for qa in qa_pairs:
                # 数据增强
                if qa["code_examples"]:
                    qa = enhance_sql_examples(qa)
                
                # 转换为标准格式
                writer.write({
                    "messages": [
                        {"role": "user", "content": f"[{qa['context']}] {qa['instruction']}"},
                        {"role": "assistant", "content": qa["output"]},
                        {"role": "system", "content": f"代码示例：{' || '.join(qa['code_examples'])}"}
                    ],
                    "source": md_file.name,
                    "type": "starrocks_doc"
                })

# 执行处理
process_starrocks_docs(
    root_dir=Path("starrocks-docs/zh-CN"), 
    output_path=Path("dataset.jsonl")
)
