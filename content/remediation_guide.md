# 이메일 전달성 문제 조치 가이드

> 진단 도구로 문제를 발견하셨나요? 항목별 조치 방법을 안내합니다.
> 각 항목은 독립적으로 조치 가능합니다. 우선순위는 DKIM → DMARC → PTR 순서를 권장합니다.

---

## 1. DKIM 미설정 ❌

### 이게 왜 문제인가요?
DKIM은 이메일 본문에 디지털 서명을 추가합니다. 수신 서버는 이 서명을 보고 "이 이메일이 실제로 해당 도메인에서 발송됐는가"를 검증합니다. DKIM이 없으면:
- 수신 서버 신뢰도 점수가 낮아집니다
- DMARC 정책이 있어도 인증 체인이 완성되지 않습니다
- 이메일 내용이 전송 중 변조됐는지 확인할 방법이 없습니다

### 조치 방법

**어떤 메일 서비스를 쓰는지에 따라 방법이 다릅니다.**

#### Google Workspace 사용 중인 경우
1. Google Admin 콘솔 (`admin.google.com`) 로그인
2. 앱 → Google Workspace → Gmail → 이메일 인증
3. "DKIM 키 생성" 클릭 → 키 길이 **2048비트** 선택
4. 생성된 TXT 레코드 값을 DNS에 추가
   ```
   레코드 유형: TXT
   호스트명:    google._domainkey.yourdomain.co.kr
   값:          v=DKIM1; k=rsa; p=MIIBIjAN...
   ```
5. DNS 반영 후 (최대 48시간) Admin 콘솔에서 "DKIM 인증 시작" 클릭

#### Microsoft 365 사용 중인 경우
1. Microsoft 365 Defender 포털 (`security.microsoft.com`) 로그인
2. 이메일 및 협업 → 정책 및 규칙 → 위협 정책 → DKIM
3. 도메인 선택 → "사용" 토글 켜기
4. 자동 생성된 CNAME 레코드 2개를 DNS에 추가
   ```
   selector1._domainkey.yourdomain.co.kr  →  CNAME  →  selector1-yourdomain-co-kr._domainkey.onmicrosoft.com
   selector2._domainkey.yourdomain.co.kr  →  CNAME  →  selector2-yourdomain-co-kr._domainkey.onmicrosoft.com
   ```

#### AWS SES 사용 중인 경우
1. AWS 콘솔 → SES → 자격 증명 → 도메인 선택
2. "DKIM 구성" 탭 → Easy DKIM 활성화 → **RSA_2048_BIT** 선택
3. 자동 생성된 CNAME 레코드 3개를 DNS에 추가 (AWS가 서명 키를 자동 교체해줍니다)

#### 자체 메일 서버 운영 중인 경우 (Postfix, Exim 등)
1. DKIM 키 생성 (서버에서 실행):
   ```bash
   openssl genrsa -out dkim_private.key 2048
   openssl rsa -in dkim_private.key -pubout -out dkim_public.key
   ```
2. DNS에 공개 키 추가:
   ```
   레코드 유형: TXT
   호스트명:    mail._domainkey.yourdomain.co.kr
   값:          v=DKIM1; k=rsa; p=[공개키 한 줄로 붙여넣기]
   ```
3. 메일 서버에 opendkim 설치 및 개인 키 경로 설정

### 설정 확인 방법
```bash
# DNS 조회로 즉시 확인
nslookup -type=TXT google._domainkey.yourdomain.co.kr

# 또는 온라인 도구
# https://mxtoolbox.com/dkim.aspx
```

---

## 2. DMARC 미설정 또는 p=none ❌ / ⚠️

### 이게 왜 문제인가요?
DMARC는 SPF와 DKIM 검증 결과를 바탕으로 "인증 실패한 이메일을 어떻게 처리할지"를 수신 서버에 알려주는 정책입니다.

- **미설정**: 도메인 사칭 이메일이 수신자에게 그대로 전달됩니다. 스팸 필터도 추가 감점합니다.
- **p=none**: 정책은 있지만 아무것도 차단하지 않습니다. 모니터링 전용 상태입니다.

### 조치 방법 — 3단계 점진적 강화

**1단계 — 지금 당장 (리스크 없음):**
```dns
레코드 유형: TXT
호스트명:    _dmarc.yourdomain.co.kr
값:          v=DMARC1; p=none; rua=mailto:dmarc-reports@yourdomain.co.kr
```
`p=none`으로 시작하면 아무것도 차단하지 않고 리포트만 받습니다.
리포트를 2–4주 수신하면서 어떤 서버가 도메인을 대신 발송하는지 파악합니다.

**2단계 — 4주 후 (리포트 확인 후):**
```dns
값: v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc-reports@yourdomain.co.kr
```
`p=quarantine`은 인증 실패 이메일을 스팸함으로 보냅니다.
`pct=10`은 전체의 10%만 정책 적용 — 문제 없으면 점진적으로 100%로 올립니다.

**3단계 — 최종 목표:**
```dns
값: v=DMARC1; p=reject; rua=mailto:dmarc-reports@yourdomain.co.kr
```
`p=reject`는 인증 실패 이메일을 완전 차단합니다. 가장 강력한 보호 수준입니다.

### DNS에 추가하는 방법
도메인 관리 패널(가비아, 후이즈, Cloudflare 등)에서:
- 레코드 유형: `TXT`
- 호스트명: `_dmarc` (앞에 도메인 붙이지 않음 — 패널이 자동 처리)
- 값: 위의 문자열

### DMARC 리포트 분석 도구 (무료)
DMARC 리포트는 XML 형식으로 옵니다. 사람이 읽기 어렵습니다. 아래 무료 도구를 사용하세요:
- **dmarcian** — dmarc.org 운영, 소규모 무료 티어 있음
- **Google Postmaster Tools** — Gmail 수신 도메인 기준 평판 확인 (무료)
- **MXToolbox DMARC Analyzer** — 빠른 점검용

---

## 3. PTR (역방향 DNS) 미설정 또는 불일치 ⚠️

### 이게 왜 문제인가요?
PTR 레코드는 "이 IP 주소의 주인이 누구인가"를 역방향으로 알려줍니다.
네이버 메일은 발신 IP의 PTR이 발신 도메인과 일치하는지를 신뢰도 신호로 사용합니다.
PTR이 없거나 `ec2-xx-xx-xx-xx.compute.amazonaws.com` 같은 기본값이면 스팸 감점을 받습니다.

### 조치 방법 — 인프라 환경별

#### AWS EC2 (Elastic IP) 사용 중인 경우
AWS는 Elastic IP에 한해 PTR 설정을 직접 지원합니다:
```bash
# AWS CLI로 Elastic IP의 PTR 설정
aws ec2 modify-address-attribute \
  --allocation-id eipalloc-XXXXXXXX \
  --domain-name mail.yourdomain.co.kr
```
또는 AWS 콘솔 → EC2 → Elastic IPs → IP 선택 → "Edit reverse DNS" 클릭.

> ⚠️ Elastic IP가 아닌 일반 퍼블릭 IP는 AWS가 PTR 설정을 허용하지 않습니다. Elastic IP 할당이 선행되어야 합니다.

#### 국내 IDC / 호스팅 서버 (KT, SKT, LG U+, 가비아 등) 사용 중인 경우
ISP에 직접 PTR 설정을 요청해야 합니다. 이메일 또는 고객센터로 다음 내용을 전달하세요:
```
요청 내용: 역방향 DNS (PTR) 레코드 설정 요청
대상 IP: xxx.xxx.xxx.xxx
설정할 PTR 값: mail.yourdomain.co.kr
```
대부분의 ISP는 무료로 처리해줍니다. 처리 기간: 1–3 영업일.

#### KT 코넷 사용 중인 경우
`http://dns.kornet.net` → 역방향 DNS 관리 메뉴에서 직접 설정 가능합니다.

#### Cloudflare 사용 중인 경우
Cloudflare는 PTR 설정을 직접 지원하지 않습니다. 원본 서버의 IP 소유자(호스팅사)에게 요청해야 합니다.

### 설정 확인 방법
```bash
# 발신 IP의 PTR 확인
nslookup xxx.xxx.xxx.xxx
# 또는
host xxx.xxx.xxx.xxx

# 결과 예시 (정상):
# xxx.xxx.xxx.xxx.in-addr.arpa domain name pointer mail.yourdomain.co.kr
```

---

## 4. SPF 미설정 ❌

### 이게 왜 문제인가요?
SPF는 "이 도메인에서 이메일을 발송할 수 있는 IP 목록"을 DNS에 공개합니다. 없으면 수신 서버가 발신 서버를 검증할 방법이 없습니다.

### 조치 방법
DNS에 TXT 레코드 1개 추가:

#### Google Workspace 사용 중인 경우:
```dns
레코드 유형: TXT
호스트명:    @ (루트 도메인)
값:          v=spf1 include:_spf.google.com ~all
```

#### Microsoft 365 사용 중인 경우:
```dns
값: v=spf1 include:spf.protection.outlook.com ~all
```

#### AWS SES 사용 중인 경우:
```dns
값: v=spf1 include:amazonses.com ~all
```

#### 자체 서버 + 외부 서비스 혼용 중인 경우:
```dns
값: v=spf1 ip4:xxx.xxx.xxx.xxx include:_spf.google.com ~all
```
`ip4:`에 실제 발신 서버 IP를 추가합니다. 여러 IP는 공백으로 구분합니다.

> ⚠️ `~all` (소프트 페일)로 시작하세요. 정상 발송 확인 후 `-all` (하드 페일)로 강화합니다.
> ⚠️ SPF 레코드는 도메인당 1개만 허용됩니다. 기존 레코드가 있으면 합쳐야 합니다.

### 설정 확인 방법
```bash
nslookup -type=TXT yourdomain.co.kr
# v=spf1 으로 시작하는 레코드가 보이면 정상
```

---

## 5. DKIM 키 길이 부족 ⚠️ (1024비트 이하)

### 이게 왜 문제인가요?
1024비트 DKIM 키는 현재 보안 기준에서 취약합니다. Gmail을 포함한 주요 수신 서버는 2048비트 이상을 권장하며, 일부는 1024비트 키를 경고 처리합니다.

### 조치 방법
기존 셀렉터를 그대로 교체하면 서비스 중단 위험이 있습니다. **새 셀렉터를 추가한 후 전환**하는 방식을 권장합니다:

1. 새 셀렉터 이름 결정 (예: `mail2`, `2026` 등)
2. 2048비트 키로 새 DNS 레코드 추가
3. 메일 서버 설정에서 새 셀렉터로 전환
4. 48시간 후 기존 셀렉터 레코드 삭제

Google Workspace의 경우 Admin 콘솔에서 기존 DKIM 키를 회전(rotate)할 수 있습니다.

---

## 6. KISA 화이트도메인 등록 (선택)

### 이게 뭔가요?
KISA(한국인터넷진흥원)가 운영하는 화이트리스트입니다. 등록된 도메인은 국내 주요 메일 서버의 스팸 필터에서 신뢰도 가점을 받습니다.

### 등록 방법
- URL: `https://spam.kisa.or.kr/white/sub2.do`
- 무료, 온라인 신청
- 심사 기간: 약 1–2주
- 요건: SPF 설정 완료, 수신거부 처리 시스템 구축

---

## 조치 후 재점검

조치 완료 후 아래 명령으로 재점검하여 점수 개선을 확인하세요:
```bash
uv run check.py yourdomain.co.kr
```

DNS 변경은 전파에 최대 48시간이 소요됩니다. 변경 직후 점수가 반영 안 될 수 있습니다.

---

## 도움이 더 필요하신가요?

각 항목의 구체적인 설정 과정에서 막히는 부분이 있으시면 언제든 연락 주세요.
어떤 메일 서비스와 서버 환경을 사용하시는지 알려주시면 더 정확한 가이드를 드릴 수 있습니다.

**GitHub:** https://github.com/pon00050/korean-email-deliverability
