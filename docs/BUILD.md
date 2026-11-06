# 재빌드

## 준비물

빌드 스크립트는 저장소 폴더를 작업 폴더로 쓰고, **그 상위 폴더**에서 원본 디스크와 나눔스퀘어 네오 글꼴을 찾습니다.

```
<상위 폴더>/
  Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin   ← README의 해시와 일치해야 함
  NanumSquareNeo-bRg.ttf  NanumSquareNeo-dEb.ttf  NanumSquareNeo-eHv.ttf
  <이 저장소>/
    fonts/Galmuri7-2.40.4.bdf  fonts/Galmuri9-2.40.4.bdf
```

- Python 3.13, `numpy`, `Pillow`
- 글꼴 출처는 `docs/FONT_CREDITS.md`
- xdelta3 (배포 파일을 만들 때만)

## 빌드

저장소 폴더에서 실행합니다.

```powershell
python tools/extract.py "../Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin" disc PRG DAT   # 디스크 파일 → disc/
python tools/dump.py        # 원본 장면 글꼴 → glyphs.bin (scenes.json도 다시 씀)
python tools/build.py "../Bakuretsu Hunter (Korean) (Track 1).bin"
```

`glyphs.bin`은 원본 글리프라 저장소에 없습니다. 번역문의 `⟨번호⟩`(하트 등 원본 기호)를 그릴 때 씁니다. `build.py`는 원본 BIN을 읽어 바뀐 파일만 같은 자리에 다시 쓰고, 마지막에 `errors 0`이 나와야 합니다. 결과 BIN의 SHA-256이 `release_manifest.json`의 `output_bin_sha256`과 같아야 합니다. 트랙 2는 원본을 그대로 씁니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s "Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin" "Bakuretsu Hunter (Korean) (Track 1).bin" BakuretsuHunter_SS_KO_v1.0.xdelta
```

## 번역 수정

1. `tr/<장면>.txt`의 `번호<TAB>한국어`를 고칩니다(`docs/TRANSLATION_GUIDE.md`).
2. `python tools/wrap.py 2_04`처럼 장면 이름을 주어 `ko/<장면>.json`을 다시 만듭니다. 한 줄 15칸을 넘으면 `LONG`을 출력합니다.
3. `python tools/build.py ...`를 다시 실행합니다.
