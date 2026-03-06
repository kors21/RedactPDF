import argparse
import sys
from pathlib import Path

import fitz


def load_words(words_file: str) -> list[str]:
    path = Path(words_file)
    if not path.exists():
        print(f"단어 파일을 찾을 수 없습니다: {words_file}")
        sys.exit(1)
    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.strip()
        if word:
            words.append(word)
    if not words:
        print("단어 파일이 비어 있습니다.")
        sys.exit(1)
    return words


def redact_pdf(pdf_path: str, words: list[str], output_path: str) -> dict[str, int]:
    doc = fitz.open(pdf_path)
    counts = {}

    for word in words:
        counts[word] = 0
        for page in doc:
            rects = page.search_for(word)
            for rect in rects:
                page.add_redact_annot(rect, fill=(0, 0, 0))
                counts[word] += 1

    for page in doc:
        page.apply_redactions()

    doc.save(output_path)
    doc.close()
    return counts


def main():
    parser = argparse.ArgumentParser(description="PDF 특정 단어를 검정색으로 가리기")
    parser.add_argument("pdf", help="입력 PDF 파일 경로")
    parser.add_argument("-w", "--words", required=True, help="가릴 단어 목록 텍스트 파일 경로 (한 줄에 하나)")
    parser.add_argument("-o", "--output", help="출력 PDF 파일 경로 (기본: {파일명}_redacted.pdf)")
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        print(f"PDF 파일을 찾을 수 없습니다: {args.pdf}")
        sys.exit(1)

    words = load_words(args.words)
    print(f"가릴 단어 {len(words)}개 로드: {words}")

    if args.output:
        output_path = args.output
    else:
        p = Path(args.pdf)
        output_path = str(p.with_stem(p.stem + "_redacted"))

    counts = redact_pdf(args.pdf, words, output_path)

    total = sum(counts.values())
    print(f"\n결과:")
    for word, count in counts.items():
        print(f"  '{word}' → {count}건 처리")
    print(f"  총 {total}건 가림 처리 완료")
    print(f"  저장: {output_path}")


if __name__ == "__main__":
    main()
