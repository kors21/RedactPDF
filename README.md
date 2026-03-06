# PDF Redact

PDF에서 특정 단어를 검정색으로 가려 개인정보를 제거하는 CLI 도구입니다.

`apply_redactions()`를 사용하여 검정 사각형 아래의 원본 텍스트까지 완전히 삭제합니다. 처리된 PDF는 바이너리 수준에서도 해당 텍스트가 남지 않습니다.

## Requirements

- Python 3.9+
- PyMuPDF

```bash
pip install -r requirements.txt
```

## Usage

### 1. 가릴 단어 목록 작성

`words.txt` 파일에 가릴 단어를 한 줄에 하나씩 작성합니다.

```text
John Doe
123-45-6789
456 Oak Avenue
Springfield
```

### 2. 실행

```bash
python redact.py input.pdf -w words.txt
```

출력 파일은 `input_redacted.pdf`로 자동 저장됩니다.

`-o` 옵션으로 출력 경로를 직접 지정할 수도 있습니다.

```bash
python redact.py input.pdf -w words.txt -o output.pdf
```

### 3. 실행 결과 예시

```
가릴 단어 4개 로드: ['John Doe', '123-45-6789', '456 Oak Avenue', 'Springfield']

결과:
  'John Doe' → 12건 처리
  '123-45-6789' → 8건 처리
  '456 Oak Avenue' → 3건 처리
  'Springfield' → 5건 처리
  총 28건 가림 처리 완료
  저장: output.pdf
```

## Notes

- 이미지 기반(스캔) PDF는 텍스트 검색이 불가능하므로 OCR 전처리가 필요합니다.
- 긴 문자열(예: `John Doe`)을 먼저, 짧은 파편(예: `Doe`)을 나중에 등록하면 누락 없이 처리됩니다.
- 처리 후 텍스트 추출 및 바이너리 검사로 개인정보가 완전히 제거되었는지 검증하는 것을 권장합니다.
