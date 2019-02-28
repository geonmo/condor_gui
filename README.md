## KISTIBatch
KISTI Tier-3의 편리한 사용을 위한 HTCondor JDL(Job Description Language) 파일 생성기(GUI)입니다.

해당 시스템을 이용하기 위해서는 git clone을 통해 소스 코드 복사를 먼저 하셔야 합니다.

```bash
git clone https://github.com/geonmo/KISTIBatch.git
```

해당 git 코드들은 예제를 포함하고 있습니다.

예제를 통하여 본인이 어떻게 JDL을 생성할 수 있을지 실습해봅시다.

## 예제
### 파일 소개 : 각 파일들은 다음과 같은 기능을 수행합니다.
- getZMass.py : nanoAOD 파일을 읽어 Zmass 분포를 그립니다. 해당 코드에서 결과물 파일 이름은 zcandmass.root이며 TFile의 Open("RECREATE")로 결과파일을 생성합니다.
- run.sh : CMSSW와 ROOT 사용을 위한 환경변수 설정 및 위 분석 코드를 실행하는 코드입니다. 이 예제에서는 getZMass.py 뒤에 붙는 인자를 통해 입력 파일을 넣어줍니다. 예) ./getZMass.py a.root => a.root 파일을 읽어서 분석
- filelist.txt : 입력 파일의 경로를 넣어주는 파일입니다. 이 예제에서는 외부 사이트에 들어있는 파일을 넣기 위해 CMS AAA federation (root://cmsxrootd.fnal.gov/)를 이용합니다.
- gui.py : 위 3개 파일을 이용하여 HTCondor 작업 제출 명세 파일을 작성해주는 GUI 프로그램입니다.
### 사용 방법 소개
cmsenv를 사용하지 않고 gui.py를 실행합니다. 
```bash
./gui.py
```
