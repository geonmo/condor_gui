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
- run.sh : CMSSW와 ROOT 사용을 위한 환경변수 설정 및 위 분석 코드를 실행하는 코드입니다. 이 예제에서는 getZMass.py 뒤에 붙는 인자를 통해 입력 파일을 넣어줍니다. 이 예제는 10000개의 이벤트만 분석합니다. 
   - 예) ./getZMass.py a.root => a.root 파일을 읽어서 분석
- filelist.txt : 입력 파일의 경로를 넣어주는 파일입니다. 이 예제에서는 외부 사이트에 들어있는 파일을 넣기 위해 CMS AAA federation (root://cmsxrootd.fnal.gov/)를 이용합니다.
- gui.py : 위 3개 파일을 이용하여 HTCondor 작업 제출 명세 파일을 작성해주는 GUI 프로그램입니다.
### 사용 방법 소개
1. cmsenv를 사용하지 않고 gui.py를 실행합니다. 
```bash
./gui.py
```
![image](https://user-images.githubusercontent.com/4969463/53553725-a4032400-3b81-11e9-90d4-5e1943c29fce.png)

2. App Name에는 아무 이름이나 넣으면 됩니다. 해당 이름으로 JDL 파일이 생성됩니다.

3. Running Script는 환경변수 설정을 담당하는 run.sh 를 넣어줍니다. Open File 버튼을 통해 오타 없이 파일을 입력할 수 있습니다.

4. Analysis Code File Name 부분에는 분석 코드를 입력합니다. 이 예제에서는 getZMass.py 입니다. 마찬가지로 Open File 버튼을 통해 입력합니다.

5. FileList는 예제에서 주어진 filelist.txt파일을 넣어줍니다. 마찬가지로 Open File 버튼을 통해 입력합니다.

6. output File Name은 LineEditor에 직접 출력 파일을 입력하거나 Analysis code에 "RECREATE" 로 결과파일을 하나만 출력한 경우 Search 버튼을 활용할 수 있습니다.

7. 모든 항목을 입력한 후 Done 버튼을 누르면 $AppName.sub 파일이 생성됩니다.

![image](https://user-images.githubusercontent.com/4969463/53554548-5edff180-3b83-11e9-8e7b-a4d9e8c64873.png)

8. 파일이 잘 생성되었는지 확인합니다.
```bash
(base) [geonmo@ui10 KISTIBatch]$ cat ana01.sub 

batch_name = ana01
executable = /share/geonmo/CMSSW_10_2_9/src/KISTIBatch/run.sh
universe   = vanilla
arguments  = $(DATAFile)
getenv     = True

transfer_input_files = /share/geonmo/CMSSW_10_2_9/src/KISTIBatch/getZMass.py, /tmp/x509up_u556800422
should_transfer_files = YES
when_to_transfer_output = ON_EXIT

transfer_output_files = zcandmass.root
transfer_output_remaps = "zcandmass.root = zcandmass_$(Process).root"


output = job_$(Process).out
error  = job_$(Process).err
log = condor.log

x509userproxy=/tmp/x509up_u556800422
accounting_group=group_cms

+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest"
+SingularityBind = "/cvmfs, /cms, /share, /tmp"

queue DATAFile from /share/geonmo/CMSSW_10_2_9/src/KISTIBatch/filelist.txt
```

9. 외부 사이트의 데이터를 사용하는 경우에는 x509 인증서를 만들어야 합니다.
(현재 업데이트된 프로그램에서는 파일 존재를 검색하여 테스트가 진행됩니다. T3에 파일이 있는 경우 local 경로를 사용합니다.)

```bash
voms-proxy-init --voms cms
```

10. 작업을 제출하고 결과가 잘 돌아오는지 확인합니다.
```bash
condor_submit Ana02.sub
```
