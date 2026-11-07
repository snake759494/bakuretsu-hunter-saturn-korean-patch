# 폭렬헌터 세가 새턴 한글패치

세가 새턴 일본판 **爆れつハンター (T-22402G)**용 비공식 한국어 패치입니다. **1~6장 44장면의 대사·나레이션·선택지 1,621개 전체**를 한국어로 바꿨습니다. **대화창 이름표, 타이틀·옵션·파일 메뉴 버튼, 세이브 파일 판, 세이브/로드 화면, 슬롯 배틀 승패 글자** 같은 그림 글자도 한글로 다시 그렸습니다. 현재 배포판은 **v1.3 (2026-11-08)**입니다.

[패치 다운로드](https://github.com/snake759494/bakuretsu-hunter-saturn-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 한글패치 **BakuretsuHunter_SS_KO_v1.3.xdelta**뿐입니다. 저장소에는 제작 소스와 한국어 번역만 공개합니다. 원본·완성 디스크 이미지, 추출한 게임 파일, 일본어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『폭렬헌터』는 아카호리 사토루 원작 만화·애니메이션을 바탕으로 한 1996년 세가 새턴 어드벤처 게임입니다. 소서러 헌터 캐롯 일행이 빅 맘의 의뢰를 받아 횡포를 부리는 소서러를 처리하러 다니며, 보기·조사·말하기 커맨드와 선택지, 슬롯 배틀로 이야기를 진행합니다.

이 패치는 **세가 새턴 일본판 T-22402G V1.002의 BIN/CUE 이미지(트랙 2개: 데이터 MODE1/2352 + 음악)**의 **트랙 1**에만 적용합니다. 트랙 2(음악)는 바뀌지 않으므로 원본을 그대로 씁니다. 파일 이름보다 아래 표의 크기와 해시가 일치하는지가 중요합니다.

## 적용할 원본

| 항목 | 값 |
| --- | --- |
| 게임 ID | T-22402G V1.002 |
| 원본 형식 | 수정되지 않은 일본판 BIN/CUE (트랙 2개) |
| 원본 트랙 1 BIN 크기 | 386,640,576 바이트 |
| **원본 트랙 1 BIN MD5** | `2ae2063dc74a2c4451d555820f940c60` |
| 원본 트랙 1 BIN SHA-1 | `770e7981bd541ce76b785552bcf3e001fe8bc8b0` |
| 원본 트랙 1 BIN SHA-256 | `5e5e130cd7b126d82615d2242cb07ea38a10a344f20e7ccff6ec9adc3d34be07` |
| 원본 트랙 2 BIN MD5 (변경 없음) | `e9b72983c72cbeb7aa0d58bfacc10e1d` |
| xdelta 파일 크기 | 710,270 바이트 |
| xdelta SHA-256 | `8243820a1668dbd6396aeeb6ad1c44f55f3fcc70167190835b151d5cd42dd7b6` |
| 적용 결과 트랙 1 BIN 크기 | 386,640,576 바이트 (원본과 같음) |
| 적용 결과 트랙 1 BIN SHA-1 | `6320713d305823c2fb7b65a19e74265a4402d9c2` |
| 적용 결과 트랙 1 BIN SHA-256 | `077e695d0ae9d895e35d38058aa912a7b275362679026af86f5d25b1f38967e7` |

원본 게임 파일은 사용자가 직접 준비해야 합니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin'
```

위 표와 다르면 적용을 중단하세요. CHD, ECM, 압축 이미지에는 적용할 수 없습니다.

### xdelta UI 사용

1. 릴리즈에서 `BakuretsuHunter_SS_KO_v1.3.xdelta`를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 **트랙 1** `.bin`을 선택합니다.
4. **Output File**에는 새 파일 이름을 지정합니다(예: `Bakuretsu Hunter (Korean) (Track 1).bin`).
5. 원본 트랙 2 `.bin`을 복사해 `Bakuretsu Hunter (Korean) (Track 2).bin`으로 이름을 바꾸고, 아래처럼 `.cue`를 만듭니다.

```
FILE "Bakuretsu Hunter (Korean) (Track 1).bin" BINARY
  TRACK 01 MODE1/2352
    INDEX 01 00:00:00
FILE "Bakuretsu Hunter (Korean) (Track 2).bin" BINARY
  TRACK 02 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00
```

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다. xdelta 자체는 [공식 프로젝트](https://github.com/jmacd/xdelta)를 참고하세요.

### 명령줄 사용

```powershell
.\xdelta3.exe -d -s '.\Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin' '.\BakuretsuHunter_SS_KO_v1.3.xdelta' '.\Bakuretsu Hunter (Korean) (Track 1).bin'
```

해시를 자동으로 검사하고 CUE까지 만들어 주는 도구도 있습니다(CUE는 원본 트랙 2를 그대로 가리킵니다). Python 3과 xdelta3가 필요하며, 같은 이름의 출력 파일이 이미 있으면 덮어쓰지 않습니다.

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source '.\Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin' --patch '.\BakuretsuHunter_SS_KO_v1.3.xdelta' --output '.\Bakuretsu Hunter (Korean) (Track 1).bin'
```

### 실행

에뮬레이터에서 결과 `.cue`를 여세요. 원본판의 세이브 스테이트는 불러오지 마세요(대사 파일 내용이 다릅니다). 내장 메모리·카트리지 세이브는 원본판과 같은 형식입니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 대사 | 1~6장 44장면의 대사·나레이션·선택지·커맨드 1,621개 |
| 대화 글꼴 | 장면마다 쓰인 한글만 나눔스퀘어 네오로 그려 장면 글꼴 칸에 넣음 |
| 이름표 | 대화창 캐릭터 이름표(갈무리9·갈무리7) |
| 메뉴 그림 글자 | 타이틀 시작·옵션, 옵션 화면 스테레오·모노·음성·텍스트·사운드·메시지, 파일 화면 로드·복사·삭제·처음부터 |
| 세이브 | 파일 판 「스테이지 ○장」, 세이브 화면 「세이브 중」 |
| 로고 | 타이틀 로고와 세이브/로드 화면 로고는 그림을 살리고 작은 「폭렬헌터」 자막을 덧붙임(갈무리7) |
| 슬롯 배틀 | 「승리」·「패배」 큰 글자, 튜토리얼 글꼴, 능력치 표시 힘·방·기·필, 「플레이어」 판 |
| 장 제목 | 1~5장 시작의 빨간 제목 화면(후리가나는 뺐습니다) |

### 번역 원칙

- 기계 번역 없이 문맥을 보고 직접 번역했습니다(`docs/TRANSLATION_GUIDE.md`).
- 대화창은 한 줄 15칸·3줄이라 원문 길이를 넘지 않게 다듬었습니다.
- 캐릭터 이름은 일본어 발음을 따라 캐롯·쇼콜라·티라·가토·마론·도터·빅 맘 등으로 적었습니다.

### 번역하지 않은 것

- 오프닝 동영상(`OPEN.CPK`)의 크레디트 글씨
- 시스템 화면의 영어(EXIT, FILE, PRESS START 등), 제작사 로고·저작권 표기

## 알려진 한계

- 타이틀·옵션·파일 메뉴, 세이브/로드 화면과 여러 장면의 대사는 에뮬레이터로 확인했지만, 슬롯 배틀 튜토리얼·능력치 판과 1장 제목 화면은 에뮬레이터로 확인했습니다. 2~5장 제목 화면과 미니게임 화면은 이미지 변환 결과만 확인했습니다.
- 모든 선택지 분기를 끝까지 플레이해 보지는 않았습니다. 빌드는 모든 대사가 칸에 들어가는지 검사합니다.
- 실기에서의 동작은 확인하지 못했습니다. 칸을 넘치거나 어긋난 문구가 있으면 이슈로 알려 주세요.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `tools/build.py` | 전체 빌드(장면 대사·글꼴, 이름표, `extras.py`로 그림 글자 교체) |
| `tools/` | 빌드·검증 도구(Python). `cdimg.py` 디스크 이미지 직접 수정, `wrap.py` 번역 줄바꿈, `kfont.py` 대화 글꼴, `kname.py` 이름표, `kmenu.py`·`kload.py`·`kslot.py`·`ksub.py` 그림 글자, `extract.py`·`dump.py`·`scan2.py`·`names.py` 분석 데이터 생성, `apply_release.py` 해시 검사 후 적용, 그 밖에 에뮬레이터 테스트 조작 도구 |
| `tr/*.txt` | 장면별 번역. `번호<TAB>한국어` |
| `ko/*.json` | `wrap.py`가 `tr/`에서 만든 줄바꿈 완료 번역(빌드 입력) |
| `scan2.json`·`scenes.json`·`names.json`·`name_uniq.json`·`loadmap.json` | 대사 위치·포인터·글꼴 칸·이름표·세이브 화면 타일 배치 등 오프셋 정보(원문 없음) |
| `fonts/` | (저장소에 없음) 갈무리 BDF를 두는 곳 |
| `docs/` | 기술 설명, 재빌드 방법, 글꼴 출처, 번역 지침 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
