# Azure 설정 체크리스트 ✅

## 📋 Phase 1: Azure 계정 & 크레딧

### Step 1: GitHub Student Pack 신청
- [ ] https://education.github.com/pack 접속
- [ ] GitHub로 로그인
- [ ] 학생 인증 (대학 이메일 또는 재학증명서)
- [ ] "Verify" 완료

### Step 2: Azure 계정 생성
- [ ] https://azure.microsoft.com/en-us/free/students/ 접속
- [ ] "Start free" 클릭
- [ ] Microsoft 계정 생성 (또는 GitHub로 로그인)
- [ ] 결제 정보 입력 (크레딧으로 결제)
- [ ] $100 크레딧 확인

### Step 3: Azure Portal 접속
- [ ] https://portal.azure.com 접속
- [ ] 리소스 그룹 확인
- [ ] 크레딧 남은 금액 확인

---

## 🏗️ Phase 2: Azure 리소스 생성

### 리소스 그룹 생성
- [ ] 이름: `my-ai-trader-app`
- [ ] 지역: `East Asia` 또는 `Southeast Asia`

### App Service 생성 (프론트엔드)
- [ ] 이름: `my-ai-trader-frontend`
- [ ] 런타임: Node 18
- [ ] SKU: Free F1
- [ ] 배포 완료 URL 기록: `https://my-ai-trader-frontend.azurewebsites.net`

### App Service 생성 (백엔드)
- [ ] 이름: `my-ai-trader-api`
- [ ] 런타임: Python 3.9
- [ ] SKU: Free F1
- [ ] 배포 완료 URL 기록: `https://my-ai-trader-api.azurewebsites.net`

### PostgreSQL 데이터베이스 생성
- [ ] 이름: `my-ai-trader-db`
- [ ] 관리자: `dbadmin`
- [ ] 암호: `복잡한 암호 설정`
- [ ] 방화벽 규칙 추가
- [ ] 연결 문자열 복사

### Redis 캐시 생성
- [ ] 이름: `my-ai-trader-redis`
- [ ] SKU: Basic
- [ ] 액세스 키 복사

### Container Registry 생성
- [ ] 이름: `myaitraderapp`
- [ ] SKU: Basic
- [ ] 로그인 정보 복사 (사용자명, 암호)

---

## 🔐 Phase 3: GitHub Secrets 설정

### Step 1: GitHub 리포지토리 설정
- [ ] https://github.com/rngusrb03-source/MY-AI-TRADER-APP 접속
- [ ] "Settings" → "Secrets and variables" → "Actions"

### Step 2: 다음 Secrets 추가

**Azure 인증:**
```
AZURE_REGISTRY_USERNAME: 
  (Container Registry 사용자명)

AZURE_REGISTRY_PASSWORD: 
  (Container Registry 암호)

AZURE_PUBLISH_PROFILE_FRONTEND:
  (App Service "배포 센터" → "배포 프로필 다운로드")

AZURE_PUBLISH_PROFILE_BACKEND:
  (App Service "배포 센터" → "배포 프로필 다운로드")
```

**API 키:**
```
NEWSAPI_KEY:
  (https://newsapi.org에서 발급)

ALPHA_VANTAGE_KEY:
  (https://www.alphavantage.co에서 발급)
```

---

## 🐳 Phase 4: Docker 이미지 준비

### Step 1: 로컬 테스트
```bash
# Backend 테스트
cd backend
docker build -t my-ai-trader-api:latest .
docker run -p 8000:8000 my-ai-trader-api:latest

# Frontend 테스트
cd frontend
docker build -t my-ai-trader-frontend:latest .
docker run -p 3000:3000 my-ai-trader-frontend:latest
```

- [ ] Backend API: http://localhost:8000/docs 확인
- [ ] Frontend: http://localhost:3000 확인

### Step 2: Azure Container Registry에 Push
```bash
# 로그인
az acr login --name myaitraderapp

# Backend Push
docker tag my-ai-trader-api:latest myaitraderapp.azurecr.io/my-ai-trader-api:latest
docker push myaitraderapp.azurecr.io/my-ai-trader-api:latest

# Frontend Push
docker tag my-ai-trader-frontend:latest myaitraderapp.azurecr.io/my-ai-trader-frontend:latest
docker push myaitraderapp.azurecr.io/my-ai-trader-frontend:latest
```

- [ ] Container Registry에 이미지 등록 확인

---

## ⚙️ Phase 5: App Service 설정

### Backend App Service 설정
1. [ ] "설정" → "응용 프로그램 설정"
2. [ ] 다음 환경 변수 추가:
   ```
   NEWSAPI_KEY=your_key
   ALPHA_VANTAGE_KEY=your_key
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   ENVIRONMENT=production
   ```
3. [ ] "배포 센터" → 배포 프로필 다운로드 & GitHub Secrets에 저장
4. [ ] "컨테이너 설정" → 이미지 선택: `myaitraderapp.azurecr.io/my-ai-trader-api:latest`

### Frontend App Service 설정
1. [ ] "설정" → "응용 프로그램 설정"
2. [ ] 다음 환경 변수 추가:
   ```
   VITE_API_URL=https://my-ai-trader-api.azurewebsites.net
   NODE_ENV=production
   ```
3. [ ] "배포 센터" → 배포 프로필 다운로드 & GitHub Secrets에 저장
4. [ ] "컨테이너 설정" → 이미지 선택: `myaitraderapp.azurecr.io/my-ai-trader-frontend:latest`

---

## 🚀 Phase 6: 자동 배포 테스트

### Step 1: 테스트 배포
```bash
# 로컬에서 수정 후 Push
git add .
git commit -m "Test Azure deployment"
git push origin main
```

- [ ] GitHub Actions 실행 확인
- [ ] 테스트 통과 확인
- [ ] Docker 이미지 빌드 & Push 확인
- [ ] App Service 배포 완료 확인

### Step 2: 배포된 앱 확인
- [ ] Frontend: https://my-ai-trader-frontend.azurewebsites.net
- [ ] Backend: https://my-ai-trader-api.azurewebsites.net
- [ ] API 문서: https://my-ai-trader-api.azurewebsites.net/docs

---

## 📊 Phase 7: 모니터링 & 최적화

### 비용 확인
- [ ] Azure Portal → "비용 관리" → 현재 비용 확인
- [ ] 월 $15 정도 사용 중인지 확인

### 성능 모니터링
- [ ] App Service → "메트릭" 확인
  - [ ] CPU 사용률
  - [ ] 메모리 사용률
  - [ ] HTTP 요청 수
  - [ ] 응답 시간

### 로그 확인
- [ ] App Service → "Log stream" 확인
- [ ] 에러 있는지 확인

### 보안
- [ ] PostgreSQL 방화벽 규칙 확인
- [ ] GitHub Secrets 안전 확인 (암호 노출 안 함)
- [ ] API 키 노출 확인

---

## 🎯 최종 확인

- [ ] 모든 Azure 리소스 생성 완료
- [ ] GitHub Secrets 설정 완료
- [ ] Docker 이미지 빌드 및 Push 완료
- [ ] GitHub Actions 워크플로우 실행 완료
- [ ] Frontend 배포 완료: https://my-ai-trader-frontend.azurewebsites.net
- [ ] Backend 배포 완료: https://my-ai-trader-api.azurewebsites.net
- [ ] 모니터링 설정 완료
- [ ] 비용 확인 완료 (월 ~$15)

---

## 📞 문제 해결

### App Service 배포 실패
```
→ Log stream에서 에러 확인
→ App Service → 고급 도구 → Kudu 접속
→ 배포 로그 확인
```

### 이미지 풀 실패
```
→ Container Registry 인증 정보 확인
→ GitHub Secrets 확인
→ App Service → 배포 센터 → 다시 배포
```

### 성능 느림
```
→ 현재는 Free Tier (느릴 수 있음)
→ 필요시 Standard F1 업그레이드
```

---

**모든 단계를 완료했으신가요? 🎉**
축하합니다! 이제 24시간 운영되는 웹사이트가 완성되었습니다! 🚀
