# 한국 이메일 Deliverability 생태계 지도 (Feb 2026)
## Korean Email Deliverability Ecosystem Map — Research Document

**목적:** 한국 이메일 발송률(deliverability) 생태계의 모든 주요 플레이어를 파악하고, 그들 간의 관계를 구조화하여, 생태계 내 "허브/인프라" 포지션으로 진입하기 위한 전략적 기반을 마련한다.

**작성일:** 2026-02-28
**연구 범위:** 규제기관, 국내 ESP, 글로벌 플레이어, 산업협회, 잠재 구매자/사용자, 컨설팅 공백, 허브 기회

---

## 1. 한국 이메일 Deliverability 생태계 구조도

```
[규제/정책 레이어]
     │
     ├── 과학기술정보통신부 (MSIT) ──────── 이메일 정책 총괄 주무부처
     ├── 방송통신위원회 (KCC) ─────────── 스팸 규제 집행권, 과태료 부과
     ├── 한국인터넷진흥원 (KISA) ─────── 화이트도메인 운영, 불법스팸대응센터, RBL
     └── 개인정보보호위원회 (PIPC) ────── 수신동의·개인정보 처리 규제

[인프라/전송 레이어]
     │
     ├── 국내 ESP (B2C/마케팅 중심)
     │    ├── 스티비 (Stibee) ─────────── 뉴스레터/마케팅. 압도적 B2C 점유
     │    ├── 타손 (TasOn) ─────────── 대량발송. 휴머스온 운영. AI메일 기능
     │    ├── 오즈메일러 (OzMailer) ──── 정액제 뉴스레터 플랫폼
     │    ├── 리캐치 (Recatch) ─────── B2B 콜드메일/CRM 특화
     │    ├── 마이메일러 (Mymailer) ─── 중소형 마케팅
     │    ├── 다이렉트센드 (DirectSend) ─ 대량발송 전문
     │    └── 썬더메일 (Thundermail) ─── 솔루션형 대량발송
     │
     ├── 국내 클라우드 이메일 인프라
     │    ├── Naver Cloud Outbound Mailer ── 월 100만건. API 기반. 기업개발자용
     │    ├── NHN Cloud Email ──────────── 150억건/년 메시지 발송 지원
     │    └── Cafe24 이메일 마케팅 ─────── 쇼핑몰 연동형. 스티비 제휴
     │
     ├── 글로벌 엔터프라이즈 (한국 현지법인/파트너 보유)
     │    ├── Braze (AB180 파트너) ────── Naver Webtoon, 당근마켓, SOCAR 등
     │    ├── Salesforce Marketing Cloud ── 트레슬(Trestle) 등 로컬 파트너
     │    └── Amazon SES ──────────────── 한국 AWS 리전. 개발자 직접 사용
     │
     └── 글로벌 인프라 (로컬 지원 없음)
          ├── Twilio SendGrid ─────────── 한국 지원팀 없음
          ├── Klaviyo ─────────────────── 한국 공식 지원 없음
          └── Oracle Responsys ─────────── 글로벌 기업 고객 일부

[수신 레이어 — Inbox Providers]
     │
     ├── 네이버 메일 ─────── 국내 점유율 1위 (약 40%+ 개인 이메일)
     ├── 카카오/다음 메일 ─── 통합운영. 2022년 9월부터 해외발신 스팸필터 강화
     ├── Gmail ──────────── 국내 기업·테크 유저 다수. Google 발신자 가이드라인 2024
     └── 네이버웍스/기업메일 ─ B2B 업무 이메일

[구매자/사용자 레이어]
     │
     ├── 이커머스 (Cafe24 입점몰, 쿠팡셀러 등)
     ├── 핀테크/금융 (뱅킹앱, 보험, 증권)
     ├── SaaS/스타트업
     ├── 교육 (학원, edtech, 대학)
     ├── 의료/병원
     ├── 공공기관/지자체
     └── 미디어/뉴스레터 발행인

[지금 존재하지 않는 레이어 — THE GAP]
     │
     └── 독립 Deliverability 전문가/인증기관
          (화이트도메인 대행 + SPF/DKIM/DMARC 구축 + 블랙리스트 모니터링 +
           네이버/카카오 inbox placement 최적화 + KISA 정책 해석 + 교육/인증)
```

**관계의 핵심:** 규제 레이어(KISA)와 수신 레이어(Naver/Kakao)와 전송 레이어(ESP) 사이에서 — **발신자가 "왜 내 메일이 안 들어가냐"고 물을 때 답을 줄 수 있는 전문가가 국내에 단 한 명도 없다.**

---

## 2. 규제 및 정부기관

### 2-1. 기관 일람표

| 기관 | 영문 | 이메일 관련 권한 | 발신자와의 접점 | 민간 협업 여부 |
|---|---|---|---|---|
| 과학기술정보통신부 | MSIT | 정보통신망법 소관 주무부처. 스팸 규제 정책 수립 | 간접(KCC·KISA에 위임) | 제한적 |
| 방송통신위원회 | KCC | 불법 스팸 조사·단속. 과태료 부과. 통신사업자 제재 | 법 위반 기업 직접 처분 | 공시·캠페인 협력 |
| 한국인터넷진흥원 | KISA | **화이트도메인 운영** + **불법스팸대응센터** + RBL(실시간차단리스트) + 정보통신망법 안내서 발행 | 발신자 직접 등록·심사 | 일부 공공기관 협력 |
| 개인정보보호위원회 | PIPC | 수신동의·개인정보 처리 규제. 위반 시 제재 | 이메일 마케팅 리스트 관리 감독 | 교육·가이드라인 |

### 2-2. 기관별 심층 분석

#### 한국인터넷진흥원 (KISA) — 가장 중요한 기관

**화이트도메인 (White Domain) 제도**
- 운영처: KISA 불법스팸대응센터 (spam.kisa.or.kr)
- 기능: 정상적인 대량 이메일 발신자가 사전 등록을 통해 국내 주요 포털(네이버, 카카오 등)로의 이메일 전송을 보장받는 제도. 미등록 IP/도메인은 RBL에 잡힐 경우 국내 주요 수신 서버에서 차단될 수 있음
- 등록 절차: 신청 → 약 2주 심사(스팸 발송 이력 검토) → 등록 또는 거부
- 모니터링: 등록 후에도 스팸 이력 발생 시 즉각 차단 및 삭제 가능
- **핵심 공백:** 화이트도메인 등록을 대행해주는 민간 서비스가 현재 사실상 없음. 일부 호스팅사(Cafe24 등)가 도움말 제공 수준

**불법스팸대응센터**
- 기능: 스팸 신고 접수, RBL 운영, 통신사업자와 협력하여 스팸 발신 IP 차단
- 민간 협력: K-ISMS 등 정보보호 인증체계는 민간 참여가 있으나, 이메일 특화 민간 파트너십 프로그램은 미확인
- **핵심 공백:** 미국의 M3AAWG, 독일의 CSA(Certified Senders Alliance)처럼 민간 전문기관이 KISA와 협력하여 발신자를 대신 교육·인증하는 체계가 없음

**정보통신망법 안내서 (제6차 개정판)**
- KISA + 방통위 공동 발간
- 핵심 규정:
  - 모든 광고성 이메일: 사전 수신 동의 원칙
  - 제목에 "(광고)" 표시 의무
  - 불법 스팸 발송자: 3년 이하 징역 또는 3천만 원 이하 벌금 (기존 1천만 원에서 강화)
  - 통신사업자 스팸 방지 의무 미이행: 과태료 3천만 원 (기존 1천만 원에서 강화)

#### 방송통신위원회 (KCC)
- 스팸 단속·조사는 전국 방송통신사무소를 통해 집행
- 발신자 입장에서는 "규제 리스크"의 원천. 컨설팅 수요를 만드는 기관
- **기회:** 법령 준수 컨설팅(광고 표시 의무, 수신동의 관리 등)은 현재 전문 서비스 공백

#### 개인정보보호위원회 (PIPC)
- 2025년 9월부터 시행 강화: 서비스 계약과 무관한 개인정보(마케팅 수신동의 등)는 별도 명시적 동의 필수
- 이메일 리스트 관리, 수신 동의 기록 보존이 컨플라이언스 과제로 부상
- **기회:** 이메일 리스트 위생(list hygiene) + 동의 관리 시스템 컨설팅

### 2-3. 규제 레이어 총평

현재 한국 이메일 규제 생태계는 **"처벌은 있지만 교육·인증은 없다"** 구조다. KISA는 화이트도메인이라는 강력한 인프라를 운영하지만, 기업이 이를 어떻게 활용해야 하는지 안내하는 민간 전문가는 없다. 독일의 CSA(Certified Senders Alliance)가 eco 협회 + DDV(다이얼로그마케팅협회)와 결합하여 KISA 역할의 민간 보완재로 자리잡은 것처럼, 한국에서도 이 공백이 비어 있다.

---

## 3. 국내 ESP 및 이메일 인프라 기업

### 3-1. 국내 ESP 비교표

| 플랫폼 | 운영사 | 포지셔닝 | 주요 고객층 | Deliverability 지원 깊이 | 공백/갭 |
|---|---|---|---|---|---|
| **스티비 (Stibee)** | 슬로워크 | 뉴스레터/마케팅 이메일. 국내 1위 B2C | 미디어, 스타트업, 브랜드 | SPF/DKIM 설정 가이드 제공. 스팸 표시 구독자 자동 삭제. 화이트도메인 권고 | DMARC 모니터링 없음. 블랙리스트 알림 없음. 도메인 평판 컨설팅 없음 |
| **타손 (TasOn)** | 휴머스온 | 대량발송. AI 최적시간 발송(STO). 국내 최저가 | 중대형 기업 마케팅팀, Cafe24 입점몰 | AI 발송 최적화. 실패율 리포트 제공 | 인증 설정 지원 미흡. deliverability 컨설팅 없음 |
| **오즈메일러 (OzMailer)** | (독립법인) | 정액제 뉴스레터. NGO 특화 요금 존재 | NGO, 교육기관, 중소기업 | 기본 발송 통계 | 인증·평판 지원 없음 |
| **리캐치 (Recatch)** | (스타트업) | B2B 아웃바운드 콜드메일/CRM | B2B 스타트업 영업팀 | 콜드메일 오픈율 최적화 가이드 | 도메인 평판, SPF/DKIM/DMARC 구축 지원 없음 |
| **마이메일러 (Mymailer)** | (독립) | 소규모 이메일 마케팅 | 소상공인, 개인 | 미확인 | 미확인 |
| **다이렉트센드 (DirectSend)** | (독립) | 대량발송 전문. 템플릿 제공 | 중소기업 | 기본 발송 성공률 리포트 | 인증·평판 지원 없음 |
| **썬더메일 (Thundermail)** | (독립) | 솔루션형 대량발송 | 기업 IT팀 | 화이트도메인 안내 가이드 있음 | 대행 서비스 없음 |

### 3-2. 국내 클라우드 이메일 인프라

| 플랫폼 | 운영사 | 포지셔닝 | 발송 규모 | Deliverability 지원 | 공백 |
|---|---|---|---|---|---|
| **Naver Cloud Outbound Mailer** | Naver Cloud Platform | API 기반 트랜잭션/마케팅 이메일. 공공기관용(gov-ncloud), 금융용(fin-ncloud) 분리 운영 | 월 기본 100만건, 상향 가능 | 발송 통계, 수신/미수신/거부 상태 제공. 예약 발송 | 도메인 평판 모니터링 없음. DMARC 설정 지원 없음. 블랙리스트 모니터링 없음 |
| **NHN Cloud Email** | NHN Cloud | 기업용 알림/마케팅 이메일 API | 연 150억건 메시지(모든 채널 합산) 지원 | 발송 결과 조회, 통계 | deliverability 컨설팅 없음 |
| **Cafe24 이메일 마케팅** | Cafe24(NHN Commerce) | 쇼핑몰 연동형. 스티비·타손 앱 제공 | Cafe24 입점몰 ~180만개 | 스티비 제휴를 통한 기본 지원 | 쇼핑몰 도메인 인증 설정 지원 없음 |
| **더존비즈온 그룹웨어** | 더존비즈온 | 기업 그룹웨어 내 이메일 | 대기업·중견기업 다수 | 보안 중심(스팸 수신 차단) | 아웃바운드 deliverability 지원 없음 |
| **가비아 기업메일** | 가비아 | 도메인·호스팅·기업메일 묶음 | 중소기업 다수 | DKIM 가이드 문서 있음 | 설정 대행 없음. 모니터링 없음 |

### 3-3. 국내 ESP/인프라 레이어 총평

한국의 모든 국내 ESP와 클라우드 이메일 인프라는 **"발송 도구"**이지 **"deliverability 서비스"**가 아니다. 발송은 해주지만 "왜 네이버에 안 들어가는가", "내 IP가 RBL에 올라갔는가", "DMARC 리포트가 뭘 말하는가"를 분석해주는 서비스는 없다. 이것이 시장 공백의 핵심이다.

---

## 4. 글로벌 플레이어의 한국 현황

### 4-1. 글로벌 ESP/CRM 플레이어

| 플레이어 | 한국 현지화 수준 | 한국 주요 고객 | 한국어 지원 | 로컬 Deliverability 전문가 | 특이사항 |
|---|---|---|---|---|---|
| **Braze** | 높음 | Naver Webtoon, 당근마켓, SOCAR, 카카오스타일, 마이리얼트립, 케이카 | 한국어 제품 페이지, 한국어 리포트 | 없음 (AB180이 파트너) | AB180이 Braze 글로벌 최다 고객 보유 리셀러. KakaoTalk 채널 연동 출시 |
| **Salesforce Marketing Cloud** | 중간 | 대기업 중심 | 한국어 제품 페이지, 트레슬(Trestle) 등 로컬 파트너 | 없음 | 이메일보다 CRM 전체 플랫폼으로 포지셔닝 |
| **Amazon SES** | 높음 (인프라) | 한국 개발자·스타트업 | 한국어 문서 | 없음 | AWS 서울 리전 운영. 트랜잭션 이메일 저비용. 하지만 설정·최적화는 사용자 자책 |
| **Twilio SendGrid** | 낮음 | 일부 글로벌 SaaS | 영문만 | 없음 | 한국 전용 지원 없음. 국내 기업들은 주로 Naver Cloud나 NHN Cloud 선택 |
| **Klaviyo** | 낮음 | 한국 진출 글로벌 이커머스 일부 | 미흡 | 없음 | Shopify 연동이 핵심. 한국 Shopify 생태계 성장에 따라 사용 늘 수 있음 |
| **Oracle Responsys** | 낮음 | 글로벌 대기업 일부 | 영문 중심 | 없음 | 실질적 한국 시장 영향력 미미 |

### 4-2. 글로벌 Deliverability 전문업체

| 플레이어 | 서비스 | 한국 존재감 | 네이버/카카오 데이터 보유 | 평가 |
|---|---|---|---|---|
| **Validity (= Return Path + 250ok + Litmus)** | 발신자 인증, 블랙리스트 모니터링, 이메일 미리보기 | 없음 | 없음 | 한국 수신함 데이터(네이버·카카오) 전혀 없음 |
| **GlockApps** | 스팸 필터 테스트, inbox placement | 없음 | 없음 | 네이버/카카오 테스트 계정 없음 |
| **MXToolbox** | DNS/SPF/DMARC 진단 | 기술 유저 일부 사용 | 없음 | 도구로는 사용 가능하나 한국 도메인 특화 해석 없음 |
| **PowerDMARC** | DMARC 모니터링·관리 | 없음 | 없음 | 한국 시장 진출 없음 |
| **Warmy.io** | 이메일 워밍업 자동화 | 없음 | 없음 | |

### 4-3. 글로벌 레이어 총평

글로벌 deliverability 도구들은 **Gmail, Outlook, Yahoo를 기준으로 만들어졌다.** 네이버와 카카오/다음은 이들의 inbox placement 테스트 패널에 없고, 한국어 스팸 필터 로직 데이터도 없다. 이것이 글로벌 전문가가 한국 발신자를 완전히 도울 수 없는 구조적 이유다.

---

## 5. 산업협회 및 자율규제 기관

### 5-1. 현황 조사 결과

| 기관명 | 이메일 deliverability 관련 활동 | 평가 |
|---|---|---|
| **한국온라인광고협회 (KOAA)** | 광고성 정보 관련 가이드라인 일부. 이메일 기술 표준 활동 미확인 | 이메일 deliverability 전문화 없음 |
| **한국광고산업협회 (KAAA)** | 광고 산업 전반. 이메일 특화 없음 | 미해당 |
| **한국디지털마케팅협회 (가칭)** | 검색 결과에서 이메일 표준 워킹그룹 확인 안 됨 | 없음 또는 비활성 |
| **한국이메일마케팅협회** | 공식 존재 **확인되지 않음** | 공백 |
| **M3AAWG 한국 회원** | M3AAWG에 한국 기업 참여 여부 미확인 | 연구 필요 |
| **CSA (Certified Senders Alliance) 한국** | 없음. CSA는 독일 기반, 한국 inbox provider 미포함 | 공백 |

### 5-2. 자율규제 생태계 총평

**한국에는 이메일 deliverability에 특화된 산업 자율규제 기관이 전혀 없다.** 미국·유럽에는:
- **M3AAWG:** ESP, ISP, 보안 기업이 참여하는 기술 표준 기관
- **EEC (Email Experience Council):** 이메일 마케터 교육·인증
- **CSA (독일):** mailbox provider + 발신자 연결 인증 기관
- **Signal Spam (프랑스):** 스팸 신고 + 인증 통합

한국에는 이 중 어느 것도 없다. KISA의 화이트도메인이 CSA의 기능 일부를 대체하고 있지만, 민간 교육·인증·컨설팅 레이어가 완전히 비어 있다.

---

## 6. 구매자/사용자 세그먼트 — 누가 이 서비스를 필요로 하는가

### 6-1. 세그먼트별 분석표

| 세그먼트 | 이메일 발송 규모 | 주요 Pain Point | 현재 솔루션 | 지불 의향 | 우선순위 |
|---|---|---|---|---|---|
| **이커머스 (Cafe24 입점몰, 독립몰)** | 높음. Cafe24 입점몰 약 180만개. 스티비/타손 주요 사용층 | 네이버 수신함 미착신. 장바구니 이탈 메일 스팸 처리. 발송률 저하 불명확한 원인 | 타손/스티비 사용. 문제 발생 시 ESP 고객지원 접촉 → 대부분 미해결 | 중~고. ROI 직결 | ★★★★★ |
| **핀테크/금융 (인터넷은행, 증권, 보험)** | 매우 높음. 거래 알림, 공지, 마케팅 복합 발송 | 금융거래 알림 스팸 처리 시 고객 불만·규제 리스크. DMARC 미설정으로 피싱 위험 노출 | Naver Cloud, NHN Cloud, Amazon SES. 내부 IT팀 관리 | 고. 규제·신뢰 직결 | ★★★★★ |
| **SaaS/스타트업** | 중간. 트랜잭션(가입 확인, 비밀번호 재설정) + 마케팅 | 가입 확인 메일 스팸 처리 → 회원가입 전환율 저하. 초기 IP 평판 관리 미숙 | Amazon SES 또는 Naver Cloud. 대부분 설정 후 방치 | 중. 성장에 직결 | ★★★★ |
| **교육 (학원, edtech, 대학)** | 중간. 수강신청 확인, 마케팅 | 수강생 모집 이메일 스팸 처리. 학생 이메일(다음/네이버) 미착신 | 오즈메일러, 타손 | 중. 마케팅 예산 있음 | ★★★ |
| **의료/병원** | 중간. 예약 확인, 건강 정보 | 예약 확인 메일 미착신. HIPAA 유사 개인정보 규제 적용 | 병원 정보시스템(HIS) 내장 메일, 또는 범용 ESP | 중. 환자 경험 직결 | ★★★ |
| **공공기관/지자체** | 높음. 민원 안내, 공고 | 국민 이메일(네이버·카카오) 미착신. 스팸 신고 증가 | 공공기관용 Naver Cloud (gov-ncloud) | 낮~중. 예산 사이클 느림 | ★★ |
| **미디어/뉴스레터 발행인** | 낮~중. 수천~수십만 구독자 | 오픈율 저하의 원인 불명확. 네이버 스팸 처리 빈발 | 스티비 주 사용층. ESP 내 가이드 의존 | 낮. 예산 소규모 | ★★ |
| **이메일 마케팅 대행사** | 클라이언트 대신 발송 | 클라이언트별 도메인 평판 관리 어려움. deliverability 설명 불가 | 없음. 클라이언트 탓으로 돌리거나 모름 | 중. B2B 수수료 가능 | ★★★★ |

### 6-2. 핵심 Pain Point 상세

**스티비 2025 이메일 마케팅 리포트 데이터:**
- 기업 회원 평균 오픈율: 13.9% (클릭률 1.1%)
- 개인 회원 평균 오픈율: 25.4% (클릭률 3.0%)
- Gmail, Naver 수신 정책 강화 이후 스팸 분류 위험 급증
- 자동화 이메일 클릭률: 비자동화 대비 3.8배

**네이버/카카오 고유 문제:**
- 카카오(다음) 메일: 2022년 9월부터 해외 발신 이메일에 스팸필터 강화
- 네이버: SPF/DKIM 미설정 발신자 속도 저하·차단·스팸 처리
- 네이버: KISA 화이트도메인 등록을 발신자에게 권고하지만 등록 절차 복잡
- 서명 포함 이메일(Gmail → Naver/Kakao)이 스팸 처리되는 사례 다수 보고

---

## 7. 기존 컨설팅/에이전시 현황

### 7-1. 현재 시장에서 deliverability를 다루는 주체들

| 유형 | 현황 | 한계 |
|---|---|---|
| **ESP 고객지원 (스티비·타손 등)** | 발송 도구 사용법 안내. 스팸 처리 시 "SPF/DKIM 확인하세요" 수준 | 도메인 평판 진단·복구, DMARC 분석, 블랙리스트 제거 대응 불가 |
| **디지털 마케팅 대행사** | DISRUPT, WithIt 등은 이메일+SMS 마케팅 통합 대행 | 이메일 콘텐츠·전략은 하지만 인프라·deliverability는 미지원 |
| **호스팅/도메인사 (가비아, 카페24)** | DKIM 설정 가이드 문서 제공 | 설정 대행, 모니터링, 최적화 없음 |
| **IT 컨설팅사 (SI)** | 기업 이메일 서버 구축 경험 있으나 deliverability 특화 없음 | DNS 설정은 하지만 수신함 최적화 개념 없음 |
| **Adobe/Salesforce 파트너** | 트레슬 등 MarTech 컨설팅. 이메일 채널 포함 | 엔터프라이즈 CRM 중심. SMB deliverability 비용 대비 과도 |

### 7-2. 결론

**현재 한국 시장에 독립 이메일 deliverability 전문가 또는 전문 컨설팅 서비스가 존재하지 않는다.** 검색 결과에서 "이메일 발송률 컨설팅", "deliverability specialist 한국", "화이트도메인 등록 대행"에 대한 전문 서비스가 확인되지 않는다. 이는 미국/유럽 시장과 극명하게 다르다 — 미국에는 Postbox Services, Engage.Guru, Unspam, Campaign Refinery 등 수십 개의 독립 컨설팅 펌이 존재한다.

---

## 8. 허브 기회 분석

### 8-1. 지금 존재하지 않는 서비스

| 서비스 | 현재 공급자 | 공백 원인 |
|---|---|---|
| 화이트도메인 등록 대행 | 없음 (KISA만 직접 접수) | 절차 이해 및 IT 지식 필요 → 기업들이 자체 처리 포기 |
| SPF/DKIM/DMARC 구축 대행 | 없음 (각사 문서만 있음) | 도메인 관리사 ≠ 이메일 인증 전문가 |
| 네이버·카카오 inbox placement 테스트 | 없음 | 글로벌 deliverability 툴에 네이버·카카오 없음 |
| 도메인/IP 평판 모니터링 (한국 특화) | 없음 | KISA RBL은 조회 가능하나 알림·리포트 없음 |
| 블랙리스트 제거 대응 | 없음 | 국내 RBL + 국제 RBL 이중 관리 필요 |
| 이메일 발송 인프라 설계 컨설팅 | 없음 | ESP 선택 + 인증 + 워밍업 + 모니터링 통합 서비스 없음 |
| Deliverability 교육/인증 | 없음 | KISA 안내서 = 법령 중심. 기술 교육 없음 |
| 수신 동의·리스트 위생 컨설팅 | 없음 | PIPC 가이드라인만 존재. 실무 대행 없음 |

### 8-2. 허브 포지션이 왜 "컨설턴트"가 아닌 "인프라"가 되는가

단순 컨설턴트와 허브 인프라의 차이:

```
[단순 컨설턴트]
   고객 → 프로젝트 단위 고용 → 종료 → 교체 가능

[허브 인프라]
   고객의 도메인 평판 데이터 보유
   KISA 화이트도메인 등록 관계 보유
   네이버·카카오 수신 데이터 패널 구축
   ESP들의 deliverability 파트너 포지션
   → 교체하면 수년간의 축적 데이터 사라짐 → 교체 불가
```

허브가 되는 조건:
1. **데이터 독점**: 고객사 도메인 평판 이력, 국내 inbox placement 결과 데이터
2. **관계 독점**: KISA와의 화이트도메인 처리 관계, Naver/Kakao 담당자 관계
3. **표준 독점**: 내가 만든 체크리스트·프레임워크가 업계 표준이 됨
4. **교육 독점**: 스티비·타손 등 ESP가 자사 고객 교육을 나에게 위탁

### 8-3. 다른 시장의 허브 포지셔닝 모델

#### 독일 — Certified Senders Alliance (CSA)
- 설립: 2004년. eco(인터넷산업협회) + DDV(다이얼로그마케팅협회) 공동 설립
- 구조: mailbox provider(GMX, Web.de, T-Online 등) + 발신자 + 인증 기관 3자 구조
- 기능: 발신자 인증 → CSA IP 화이트리스트 → 참여 mailbox provider에서 자동 우대 처리
- 수익: 발신자 연간 인증 수수료 (규모별 차등)
- **한국 적용 가능성**: KISA 화이트도메인의 민간 보완재. 네이버·카카오가 파트너로 참여한다면 직접 모델 복제 가능

#### 미국 — Validity Sender Certification (구 Return Path)
- 구조: IP 인증 → 참여 ISP에서 긍정적 신호. 독립 수익 모델
- 한국 적용 한계: 글로벌 서비스로 네이버·카카오 미포함

#### 프랑스 — Signal Spam
- 구조: 정부 + ISP + 발신자 협력 기관. 스팸 신고 + 발신자 평판 공유
- **한국 적용 가능성**: KISA + 네이버 + 카카오 + ESP 연합 기관으로 발전 가능

#### 일본 — JPAAWG + JEAG
- 일본은 M3AAWG의 일본 지부(JPAAWG)와 JEAG(Japan Email Anti-Abuse Group)가 존재
- **한국 적용 시사점**: 동아시아 최초 독립 이메일 deliverability 인증 기관 가능성

### 8-4. 허브 포지션의 수익 모델

| 수익 스트림 | 모델 | 예상 단가 |
|---|---|---|
| 화이트도메인 등록 대행 | 건당 서비스 | 30~100만원/건 |
| SPF/DKIM/DMARC 구축 패키지 | 프로젝트 | 100~300만원/프로젝트 |
| 월간 도메인 평판 모니터링 | 구독형 | 30~100만원/월 |
| 블랙리스트 대응 서비스 | 건당 + 유지보수 | 50~200만원/건 |
| ESP 파트너십 (스티비·타손 고객 교육) | B2B 위탁 | 협상 |
| 기업 교육/워크숍 | 건당 | 100~300만원/회 |
| deliverability 감사 리포트 | 프로젝트 | 200~500만원/프로젝트 |
| 법령 준수 컨설팅 (정보통신망법) | 시간제 또는 유지보수 | 15~30만원/시간 |

---

## 9. 허브 진입을 위한 권장 포지셔닝 — 5단계 전략

### Step 1: 공개 레퍼런스 자산 구축 (즉시~3개월)

**목표:** "한국 이메일 deliverability의 유일한 공개 지식 소스"가 되기

- **네이버/카카오 메일 발신자 가이드** 작성 (영어로도 — 글로벌 ESP들이 가장 필요로 함)
  - 존재하지 않는 콘텐츠: "How to get your email into Naver inbox"
  - Email on Acid의 Naver 아티클이 유일한 영문 자료 → 여기서 인용받는 사람이 됨
- **화이트도메인 등록 완전 가이드** (한국어 + 영어)
- **KISA RBL 진단 및 제거 절차** 문서화
- **정보통신망법 이메일 규정 실무 해석** 가이드

**플랫폼:** LinkedIn(영문) + 브런치/티스토리(한국어) + GitHub(기술 스펙)

### Step 2: KISA와의 관계 구축 (1~6개월)

**목표:** 화이트도메인 등록 대행의 비공식 민간 창구가 되기

- 불법스팸대응센터에 민간 교육 파트너 제안 검토
- 화이트도메인 등록 절차를 직접 대량 경험하면서 노하우 축적
- KISA가 발행하는 정보통신망법 안내서 개정 과정에 코멘트 제출
- K-ISMS 또는 관련 심사위원 자격 취득 검토

### Step 3: ESP 파트너십 확보 (3~9개월)

**목표:** 스티비·타손·NHN Cloud의 "공식 deliverability 파트너"가 되기

- 스티비 사용자들이 겪는 네이버 스팸 처리 문제를 스티비 팀에 솔루션 제안
- 타손의 AI 발송 최적화에 deliverability 레이어 추가 제안
- Naver Cloud Platform의 Outbound Mailer 사용 기업 대상 deliverability 컨설팅 공식화
- AB180(Braze 파트너)과 협력 — Braze 고객사의 이메일 채널 deliverability 전담

**핵심:** ESP 파트너십은 "고객 채널"이 아니라 "공급망 내 포지션"이다. ESP가 내 서비스를 자사 상품의 일부처럼 추천하면, 나는 마케팅 없이 고객이 온다.

### Step 4: 데이터 자산 구축 (6~18개월)

**목표:** 한국 최초 inbox placement 데이터셋 보유자가 되기

- 네이버·카카오·Gmail 테스트 계정 패널 구축 (글로벌 deliverability 툴들이 없는 것)
- 주요 한국 산업별(이커머스, 금융, 교육) 평균 발송률·오픈율 벤치마크 데이터 축적
- KISA RBL, 주요 국제 블랙리스트(Spamhaus, Barracuda, SORBS) 한국 도메인 현황 모니터링
- 이 데이터를 연간 "한국 이메일 deliverability 리포트"로 공개 → 권위 구축

### Step 5: 인증/표준 기관화 (18개월~3년)

**목표:** 개인 → 기관화. "한국 이메일 발신자 인증 프로그램" 운영자가 되기

- 독일 CSA 모델을 벤치마크하여 "Korea Certified Email Senders" 프로그램 설계
- 파트너: KISA + 네이버 + 카카오 + 주요 ESP
- 인증 요건: 화이트도메인 등록 + SPF/DKIM/DMARC 완전 설정 + 정기 모니터링 + 정보통신망법 준수
- 인증 획득 기업은 네이버·카카오 수신 서버에서 우대 처리 (네이버·카카오 설득이 핵심)
- **이것이 허브 인프라화의 최종 형태**: 인증 기관이 되면 모든 대량 이메일 발신자가 나를 통해야 한다

---

## 10. 부록: 주요 참고 자료 및 출처

### 규제/정책
- [KISA 공식 사이트](https://www.kisa.or.kr/EN/103) — 화이트도메인, 불법스팸대응센터 운영
- [화이트도메인 등록 가이드 — ITEasy](https://www.iteasy.co.kr/solution/whitedomain) — 민간 측 화이트도메인 설명
- [불법 스팸 방지를 위한 정보통신망법 안내서 (KISA)](https://www.kisa.or.kr/401/form?postSeq=3256) — 제6차 개정판
- [방송통신위원회 불법 스팸 조사·단속](https://www.kcc.go.kr/user.do?page=A04100207&dc=K04100207)
- [KISA, 정보통신망법 안내서 개정 — 보안뉴스](https://m.boannews.com/html/detail.html?idx=128266)
- [개인정보보호위원회 개인정보 처리방침 작성지침 2025](https://www.privacy.go.kr/front/bbs/bbsView.do?bbsNo=BBSMSTR_000000000049&bbscttNo=20806)

### 국내 ESP/인프라
- [스티비 공식 사이트](https://stibee.com/)
- [스티비 2025 이메일 마케팅 리포트](https://report.stibee.com/2025/)
- [스티비 스팸 방지 가이드](https://help.stibee.com/tip/prevent-email-spam-marking)
- [타손(TasOn) 공식 사이트](https://www.tason.com/)
- [오즈메일러 공식 사이트](https://www.ozmailer.com/)
- [리캐치(Recatch) B2B 이메일 가이드](https://www.recatch.cc/ko/blog/b2b-email-marketing/)
- [다이렉트센드 공식 사이트](https://directsend.co.kr/index.php/introduce/mail)
- [Naver Cloud Outbound Mailer](https://www.ncloud.com/v2/product/applicationService/cloudOutboundMailer)
- [NHN Cloud 이메일 서비스](https://www.nhncloud.com/kr/service/notification/email)
- [NHN Cloud 2025년 150억건 메시지 지원 — 중앙이코노미뉴스](https://www.joongangenews.com/news/articleView.html?idxno=484050)

### 글로벌 플레이어
- [Braze 한국어 이메일 제품 페이지](https://www.braze.com/kr/product/email)
- [AB180 — Braze 공식 파트너 (한국)](https://www.ab180.co/solutions/braze)
- [2025 한국 고객 인게이지먼트 리뷰 — AB180](https://www.ab180.co/library/korea-customer-engagement-review-2025)
- [Salesforce Marketing Cloud Korea](https://www.salesforce.com/kr/marketing/)

### 수신 서버 및 기술
- [Naver Mail 소개 — Inquivix (영문)](https://inquivix.com/naver-mail/)
- [Naver best practices Salesforce Trailhead](https://trailhead.salesforce.com/trailblazer-community/feed/0D54S00000A8bhzSAB)
- [내가 보낸 이메일이 스팸으로 분류된다면 — 스티비 블로그](https://blog.stibee.com/eb-82-b4-ea-b0-80-eb-b3-b4-eb-82-b8-ec-9d-b4-eb-a9-94-ec-9d-bc-ec-9d-b4-ec-8a-a4-ed-8c-b8-eb-a9-94-ec-9d-bc-eb-a1-9c-eb-b6-84-eb-a5-98-eb-90-9c-eb-8b-a4-eb-a9-b4/)
- [G메일·네이버 수신 정책 변경 대응 — 스티비](https://blog.stibee.com/gmail-sender-guidelines-2/)
- [서명 포함 메일이 네이버·카카오에서 스팸 처리되는 문제 — Gmail Community](https://support.google.com/mail/thread/280577969)
- [Naver Webmail Testing — Email on Acid](https://www.emailonacid.com/blog/article/email-development/naver-webmail-testing-what-you-need-to-know/)

### 해외 허브 모델
- [Certified Senders Alliance (CSA) 공식 사이트](https://certified-senders.org/)
- [CSA 인증 프로세스](https://certified-senders.org/certification-process/)
- [CSA란 무엇인가 — EmailVendorSelection](https://www.emailvendorselection.com/certified-senders-alliance/)
- [Top 7 Email Deliverability Consulting Agencies 2025 — Postbox Services](https://postboxservices.com/top-7-email-deliverability-consulting-agencies-to-watch-in-2025)
- [EasyDMARC 2025 DMARC Adoption Report](https://easydmarc.com/blog/ebook/easydmarc-dmarc-adoption-report-2025/)
- [The state of DMARC in 2026 — Spam Resource](https://www.spamresource.com/2026/02/the-state-of-dmarc-in-2026.html)

---

*이 문서는 2026년 2월 기준 웹 조사 및 공개 데이터 기반으로 작성되었습니다. 일부 시장 통계(특히 한국 특화 DMARC 채택률 등)는 공개 데이터의 한계로 추정치를 포함합니다.*
