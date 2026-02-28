# 한국 B2B SaaS — 이메일 Deliverability 컨설팅 잠재 고객 리서치
**작성일:** 2026-02-28
**목적:** 한국 이메일 Deliverability 컨설팅 실천의 유료 고객 파이프라인 구축을 위한 타겟 기업 식별

---

## 전략적 전제

이메일 Deliverability 컨설팅의 구매 트리거는 항상 **고통(pain)**이다. 아래 세 가지 상황 중 하나가 있어야 구매가 일어난다:

1. **인지된 위기** — 이메일이 스팸으로 빠지거나 Gmail/Naver 블록을 맞았을 때
2. **성장 임계점** — 사용자 수 증가로 이메일 볼륨이 급증할 때 (Series A→B 전환기)
3. **글로벌 확장 시작** — US/Japan 진출 시 현지 inbox placement를 처음 직면할 때

한국 B2B SaaS의 이메일 의존 흐름: **회원가입 인증 → 온보딩 시퀀스 → 트라이얼 전환 독촉 → 결제/갱신 알림 → 기능 업데이트 뉴스레터**. 이 중 하나라도 막히면 ARR에 직접 타격이 온다.

---

## 섹터별 이메일 의존도 분류

| 섹터 | 이메일 의존도 | 이유 |
|---|---|---|
| CRM / 영업툴 | 최상 | 제품 자체가 이메일 발송을 포함하거나 이메일로 신규 유저 활성화 |
| HR SaaS | 상 | 온보딩, 급여명세서, 결재 알림이 이메일 경유 |
| 고객 커뮤니케이션 플랫폼 | 상 | 트랜잭션 알림이 이메일 fallback으로 존재 |
| 문서/협업툴 | 중-상 | 초대 메일, 댓글 알림, 공유 링크 이메일 |
| AI 글쓰기/생산성 | 중 | 무료 플랜→유료 전환 이메일 시퀀스 |
| 여행/커머스 SaaS | 상 | 예약 확인, 결제 영수증, 취소 알림 |
| 데이터 거버넌스/보안 | 중-하 | 알림 위주; 대규모 마케팅 이메일은 없음 |

---

## 1차 타겟: 10–15개 한국 B2B SaaS 기업

### Tier 1 — 즉시 접근 가능, 구매력 확인됨

---

#### 1. Channel Corp. (채널톡)

| 항목 | 내용 |
|---|---|
| 제품 | AI 고객 커뮤니케이션 플랫폼 (채팅 + CRM + 팀 메신저) |
| 펀딩 | Series C $40M + $30M 추가 라운드 (2024년 4월 Axios 보도) |
| 임직원 | 약 178명 |
| 글로벌 | 한국 + 일본 100,000개 기업 고객; 미국 확장 진행 중 |
| 연매출 | $71.1M (2024년) |
| **이메일 의존도** | **최상** — 제품 자체가 고객사의 이메일 마케팅/CRM을 처리; 자사 SaaS 가입자 온보딩에도 이메일 사용 |
| **구매 트리거** | 미국 진출 시 Gmail/Outlook inbox placement 미달; 일본에서 Naver-equivalent (Yahoo Japan Mail) 블록 리스크 |
| **서비스 티어** | 구현(Implementation) + 리테이너 |
| **접근 방법** | LinkedIn (마케팅팀 리드 또는 Product Growth 담당자); 채널톡 공식 파트너 프로그램 경유 warm intro |

---

#### 2. flex (플렉스)

| 항목 | 내용 |
|---|---|
| 제품 | HR 자동화 SaaS (연봉 계약, 근태, 급여, 온보딩) |
| 펀딩 | Series B $32M (2022, Greenoaks 리드) + Series B-1 $7.2M (2025, Han River Partners); 기업가치 $370M |
| 임직원 | 약 200명 추정 (ARR ₩30B 수준) |
| 글로벌 | 현재 국내 중심; AI SaaS 2.0 비전으로 글로벌 확장 준비 중 |
| **이메일 의존도** | **상** — 급여명세서 이메일 발송, 신규 임직원 온보딩 초대 메일, 결재 요청/승인 알림 |
| **구매 트리거** | 기업 고객 임직원 이메일 (회사 도메인)로 발송 시 IT 보안팀의 이메일 인증 요구; 고객사 중 대기업이 늘면 DMARC p=reject 환경에서 bounce 급증 |
| **서비스 티어** | 오딧(Audit) → 구현 |
| **접근 방법** | LinkedIn (CTO 또는 인프라 엔지니어링 담당); HRTECH 커뮤니티 밋업 |

---

#### 3. ProtoPie

| 항목 | 내용 |
|---|---|
| 제품 | 고충실도 인터랙션 디자인 프로토타이핑 툴 (B2B SaaS) |
| 펀딩 | Series B $21M (2025년 1월, LB Investment + KDB 공동 리드) |
| 임직원 | 약 85명; 서울 HQ + Austin / Amsterdam / Shenzhen 오피스 |
| 글로벌 | 전 세계 기업 고객 (184개국 진입한 Typed보다 더 글로벌 집중) |
| **이메일 의존도** | **중-상** — 트라이얼 전환 이메일, 팀 초대 이메일, 갱신 알림이 이메일 경유. 미국/유럽 고객 비중이 높아 Gmail/Outlook이 primary inbox |
| **구매 트리거** | US 오피스 확장 후 영어권 cold outreach 및 신규 가입 이메일의 Gmail 스팸 비율 증가; Austin 팀이 처음으로 이 문제를 인지하는 시점 |
| **서비스 티어** | 오딧(Audit) 원샷 → 구현 |
| **접근 방법** | LinkedIn (Growth/Marketing 담당자, Austin 오피스 기준); Product Hunt 커뮤니티; 영문 콘텐츠로 먼저 레퍼런스 확보 후 inbound |

---

#### 4. Relate (리레이트 / Pixelic)

| 항목 | 내용 |
|---|---|
| 제품 | B2B 스타트업 전용 CRM (YC 배치) |
| 펀딩 | ₩3.6B 누적; YC 포함 Base Investment, Translink, Von Angels |
| 임직원 | 20–40명 추정 (초기 스타트업) |
| 글로벌 | 한국 + 미국 YC 네트워크 고객; 미국 마케팅 진행 중 |
| **이메일 의존도** | **최상** — CRM 제품 자체가 이메일 시퀀스를 발송하는 기능을 포함할 가능성 높음; 자사 SaaS 신규 가입자 온보딩 이메일은 확실 |
| **구매 트리거** | 미국 고객 온보딩 이메일이 Gmail 스팸으로 빠지는 순간; YC 데모데이 이후 US 리드 급증 시점 |
| **서비스 티어** | 오딧(Audit) — 소규모이므로 저가 패키지로 시작 |
| **접근 방법** | Relate 블로그/뉴스레터 (이미 콘텐츠 마케팅 활발); LinkedIn 직접 메일; YC 커뮤니티 내 한국 창업자 네트워크 |

---

#### 5. QueryPie (CHEQUER Inc.)

| 항목 | 내용 |
|---|---|
| 제품 | 클라우드 데이터 거버넌스 플랫폼 (CDPP) |
| 펀딩 | 누적 $27.82M (2024년 5월 기준); Salesforce Ventures, Atinum, Murex, ZVC 참여 |
| 임직원 | 50–100명 추정 (실리콘밸리 창업, 서울 개발 거점) |
| 글로벌 | 한국 (Kakao, Karrot, MUSINSA, HYBE) + 글로벌 확장 중 |
| **이메일 의존도** | **중** — 엔터프라이즈 고객 알림, 접근 권한 승인/거부 이메일, 보안 알럿. 마케팅 이메일보다 트랜잭션 비중 |
| **구매 트리거** | Salesforce Ventures 투자 이후 미국 엔터프라이즈 세일즈 강화 시점; 미국 고객사 IT 팀이 발신 도메인 SPF/DKIM 확인 요청 |
| **서비스 티어** | 오딧(Audit) — 기술 지향적이므로 DIY 구현을 선호, 오딧 보고서가 최적 |
| **접근 방법** | LinkedIn (DevOps/Infra 엔지니어링 리드); CHEQUER 테크 블로그 기고 후 inbound |

---

#### 6. Typed (Business Canvas)

| 항목 | 내용 |
|---|---|
| 제품 | AI 문서 협업 툴 (지식 관리 / 리서치 워크스페이스) |
| 펀딩 | ₩5B (Sui Generis, Shinhan Venture, Kakao Ventures 등); 이후 추가 라운드 |
| 임직원 | 30–60명 추정 |
| 글로벌 | 184개국 사용자; Product Hunt Golden Kitty 노미네이션; AppSumo 론칭 |
| **이메일 의존도** | **중-상** — 팀 초대 이메일, 댓글 알림, 문서 공유 링크 이메일. 글로벌 사용자 비중이 높아 Gmail/Outlook 비중 큼 |
| **구매 트리거** | AppSumo 딜 이후 대규모 가입자 이메일 발송 시 bounce/스팸 급증; 미국 고객이 "이메일이 안 온다"는 지원 티켓 발생 시점 |
| **서비스 티어** | 오딧(Audit) → 구현 |
| **접근 방법** | Product Hunt 커뮤니티; LinkedIn; AppSumo 리뷰 섹션에서 pain point 확인 후 콜드 메일 |

---

### Tier 2 — 확실한 구매력, 접근에 노력 필요

---

#### 7. Sendbird

| 항목 | 내용 |
|---|---|
| 제품 | 채팅/음성/영상 API 플랫폼 (B2B SaaS) |
| 펀딩 | 총 $218M; Series D $100M (2021); 유니콘 ($1B+) |
| 임직원 | 약 300명; San Mateo HQ + 서울 + London |
| 글로벌 | 4,000개+ 기업 고객 (DoorDash, Reddit, Yahoo Sports 등); 미국 중심 |
| **이메일 의존도** | **중** — 자사 제품이 이메일 채널도 지원하기 시작; 신규 개발자 온보딩 이메일, 트라이얼 전환 이메일 |
| **구매 트리거** | 이메일 채널 기능 출시 후 고객사의 inbox placement 문제가 Sendbird 책임 이슈가 될 때; 또는 자사 마케팅 이메일의 Gmail 스팸 비율 |
| **서비스 티어** | 리테이너 (규모가 크므로 지속적 모니터링 적합) |
| **접근 방법** | LinkedIn (이미 US 기반이므로 영어로 접근); DevRel 팀 또는 Growth Marketing 담당 |

---

#### 8. Wrtn (뤼튼테크놀로지스)

| 항목 | 내용 |
|---|---|
| 제품 | AI 생성 플랫폼 (글쓰기, Vrew 영상편집, VFlat 스캐너, VOC Studio) |
| 펀딩 | 누적 ₩130B ($88.5M); Series B ₩108B (2025년 3월, Goodwater Capital 참여) |
| 임직원 | 200명+ 추정 |
| 글로벌 | 한국 (2024 말 런칭) + 일본 (2025 중반); 미국 진출 목표 2026년 6월 |
| ARR | $70M annualized (2025 말 기준) |
| **이메일 의존도** | **중-상** — 무료→유료 전환 이메일 시퀀스, 일일/주간 사용량 알림, 일본/미국 신규 가입자 온보딩 |
| **구매 트리거** | 미국 진출 직전/직후 — Gmail의 대량 발송 정책과 DMARC 요구사항 처음 직면; 일본에서 Yahoo Japan Mail 블록 가능성 |
| **서비스 티어** | 구현(Implementation) — 글로벌 확장 전 기반 구축형 |
| **접근 방법** | LinkedIn (Growth Marketing 또는 International Expansion 담당); 뤼튼 뉴스레터/블로그 기고자와 관계 구축 |

---

#### 9. MyRealTrip (마이리얼트립)

| 항목 | 내용 |
|---|---|
| 제품 | 여행 OTA + 투어/액티비티 플랫폼 (B2C이지만 파트너 공급사와 B2B 연결) |
| 펀딩 | Series F $56.7M (2024년 1월, BlueRun + IMM + Korelya + Vanderbilt 참여) |
| 임직원 | 약 300명 |
| 글로벌 | 일본인 인바운드 + 한국인 아웃바운드; IPO 준비 중 |
| **이메일 의존도** | **최상** — 예약 확인, 취소 알림, 결제 영수증, 여행 전 리마인더, 리뷰 요청이 모두 이메일 |
| **구매 트리거** | Series F 후 고객수 급증 시 transactional 이메일 bounce 증가; 일본 고객의 Yahoo Japan Mail / Docomo Mail 도달률 이슈 |
| **서비스 티어** | 구현(Implementation) + 리테이너 |
| **접근 방법** | LinkedIn (이메일마케팅 담당 또는 CRM 팀); 스티비(Stibee) 파트너 네트워크 경유 warm intro 가능성 |

---

#### 10. Specter (스펙터)

| 항목 | 내용 |
|---|---|
| 제품 | 클라우드 기반 인재 검증 / HR 레퍼런스 체크 플랫폼 |
| 펀딩 | 누적 $8.4M (Pre-Series B); 미국 Storm Ventures + 베트남 Do Ventures 참여 |
| 임직원 | 30–60명 추정 |
| 글로벌 | 한국 + 미국/베트남 투자자; 글로벌 확장 의도 명확 |
| **이메일 의존도** | **상** — 레퍼런스 체크 요청 이메일이 핵심 제품 플로우. 채용 담당자가 이메일을 못 받으면 제품 자체가 동작하지 않음 |
| **구매 트리거** | 미국 기업 HR 팀에게 발송하는 레퍼런스 체크 이메일이 Outlook/Gmail 스팸으로 분류되는 순간 — 이는 즉각적 매출 손실 |
| **서비스 티어** | 오딧(Audit) → 구현 (제품 이메일이 핵심 기능이므로 빠른 결정 가능) |
| **접근 방법** | LinkedIn 직접 메일 (CTO 또는 COO); Storm Ventures 포트폴리오 네트워크 |

---

#### 11. Ringle (링글잉글리시에듀케이션)

| 항목 | 내용 |
|---|---|
| 제품 | 1:1 화상 영어 튜터링 플랫폼 (MIT/Harvard 강사 매칭) |
| 펀딩 | Series A $18M (2021); K-Global Silicon Valley 2024 참가 |
| 임직원 | 11–50명 (플랫폼 모델; 튜터 2,000명은 별도) |
| 글로벌 | 한국 + 미국 + 일본 + 싱가포르; Silicon Valley / Boston 오피스 |
| **이메일 의존도** | **상** — 수업 예약 확인, 리마인더, 피드백 이메일, 튜터-학생 연결 이메일 |
| **구매 트리거** | 미국/일본 학생의 수업 예약 이메일이 스팸으로 분류되면 no-show 급증 → LTV 직접 타격 |
| **서비스 티어** | 오딧(Audit) → 구현 |
| **접근 방법** | LinkedIn (마케팅/오퍼레이션 팀); Ringle 블로그 독자층 (영문 콘텐츠 활발) |

---

#### 12. Vrew (보이저엑스 / VoyagerX)

| 항목 | 내용 |
|---|---|
| 제품 | AI 영상 편집 툴 (Wrtn 생태계 편입 전 독립 제품으로도 존재); 글로벌 사용자층 |
| 펀딩 | 보이저엑스 독립 시절 ₩8.4B; Wrtn Series B 이후 생태계 통합 |
| 임직원 | 50–100명 (뤼튼 통합 포함) |
| 글로벌 | 글로벌 다운로드 500만+ |
| **이메일 의존도** | **중** — 무료→Pro 전환 이메일, 기능 업데이트 뉴스레터, 비밀번호 재설정 |
| **구매 트리거** | 글로벌 사용자가 많아 Gmail/Outlook에서 이미 스팸 이슈 발생 가능; 마케팅 이메일 발송 정책 구축 필요 시점 |
| **서비스 티어** | 오딧(Audit) |
| **접근 방법** | Wrtn/보이저엑스 통합 후 마케팅팀 리드에 접근; 또는 영문 콘텐츠로 inbound |

---

#### 13. Swing2App (스윙투앱)

| 항목 | 내용 |
|---|---|
| 제품 | 노코드 앱 빌더 SaaS (소상공인, SMB 타겟) |
| 글로벌 | 글로벌 사용자 존재 (omail.io에 도메인 등록됨) |
| **이메일 의존도** | **중** — 가입 인증, 앱 배포 완료 알림, 결제 영수증 |
| **구매 트리거** | 글로벌 사용자 가입 이메일의 Gmail 스팸 분류 |
| **서비스 티어** | 오딧(Audit) — 소규모이므로 저가 패키지 |
| **접근 방법** | 직접 이메일 (웹사이트 contact) |

---

#### 14. 비즈플레이 (Bizplay)

| 항목 | 내용 |
|---|---|
| 제품 | 법인카드 비용관리 SaaS |
| 펀딩 | 야놀자로부터 ₩3B 시리즈A (2024) |
| **이메일 의존도** | **중-상** — 지출 승인 이메일, 월별 비용 리포트, 결제 알림 |
| **구매 트리거** | 고객사 IT 팀이 외부 도메인 이메일 인증 요구; 기업 고객이 늘수록 DMARC p=reject 충돌 |
| **서비스 티어** | 오딧(Audit) → 구현 |
| **접근 방법** | LinkedIn; 야놀자 파트너 네트워크 |

---

#### 15. CreatorLink (크리에이터링크)

| 항목 | 내용 |
|---|---|
| 제품 | 모듈형 웹빌더 SaaS; Gabia(가비아) 파트너십 |
| 사용자 | 80,000명 (국내 중심) |
| **이메일 의존도** | **중** — 가입 인증, 플랜 만료 경고, 결제 영수증 |
| **구매 트리거** | Gabia 사용자풀 기반으로 규모 성장 시 이메일 인증 문제 노출 |
| **서비스 티어** | 오딧(Audit) |
| **접근 방법** | Gabia 파트너 네트워크 or 직접 이메일 |

---

## 접근 가능성 매트릭스

| 기업 | 의사결정자 | 최적 접근 채널 | 따뜻함(온도) |
|---|---|---|---|
| Channel Corp. (채널톡) | 마케팅/Growth Lead | LinkedIn DM + 스티비 파트너 네트워크 | 중 |
| flex | CTO 또는 인프라 엔지니어 | LinkedIn DM + HRTECH 밋업 | 중 |
| ProtoPie | Growth Marketing (Austin) | LinkedIn; Product Hunt 커뮤니티 | 중 |
| Relate | 공동창업자 (소규모) | LinkedIn + Relate 블로그 댓글/뉴스레터 | 높음 |
| QueryPie | DevOps/Infra 리드 | LinkedIn + 기술 블로그 기고 후 inbound | 중 |
| Typed (Business Canvas) | 마케팅 또는 제품팀 | Product Hunt + AppSumo 커뮤니티 | 높음 |
| Sendbird | Growth Marketing (US) | LinkedIn (영어); DevRel 행사 | 낮음-중 |
| Wrtn | 글로벌 확장 담당 | LinkedIn + 뉴스레터 구독 기반 관계 | 중 |
| MyRealTrip | CRM/이메일마케팅 팀 | LinkedIn + 스티비 파트너 warm intro | 중 |
| Specter | CTO / COO | LinkedIn 직접 메일 | 높음 |
| Ringle | 오퍼레이션/마케팅 | LinkedIn + Ringle 영문 블로그 | 중-높음 |
| Vrew (보이저엑스) | 마케팅 리드 | Wrtn 통합 후 LinkedIn | 중 |
| Swing2App | 대표 직통 | 웹사이트 contact 이메일 | 높음 |
| 비즈플레이 | IT/인프라 또는 마케팅 | LinkedIn; 야놀자 네트워크 | 중 |
| CreatorLink | 대표 직통 | 가비아 파트너 경유 | 중-높음 |

**온도 해석:**
- **높음** = 소규모 또는 커뮤니티 접점 있어 콜드 메일도 읽힘
- **중** = LinkedIn + 레퍼런스 콘텐츠 선행 필요
- **낮음** = 대기업 구조, inbound 전략 또는 warm intro 필수

---

## 구매 트리거 패턴 정리

| 트리거 유형 | 설명 | 해당 기업 예시 |
|---|---|---|
| **글로벌 진출 임박** | 미국/일본 진출 발표 후 6개월 이내가 골든 타임 | Wrtn (US 2026 6월), ProtoPie (Austin 오피스 기확장), Ringle |
| **신규 투자 후 성장 가속** | Series A/B 이후 MAU 급증 → 이메일 볼륨 급증 → 문제 수면 위로 | Specter (Pre-Series B), 비즈플레이 (Series A), Typed |
| **제품 기능 확장** | 이메일 관련 기능 신규 출시 (이메일 마케팅 모듈, 알림 시스템 강화) | Channel.io (AI 알프), Sendbird (이메일 채널 추가) |
| **고객 이탈/지원 티켓** | "이메일이 안 왔다" 지원 티켓이 반복 발생 | Typed, Ringle, Swing2App |
| **엔터프라이즈 고객 요구** | B2B 대기업 고객이 이메일 인증 정책 요구 (DMARC p=reject 환경) | flex, QueryPie, 비즈플레이 |

---

## 서비스 티어 배분

| 티어 | 설명 | 적합 기업 | 예상 단가 |
|---|---|---|---|
| **오딧 (Audit)** | 1회성: SPF/DKIM/DMARC 진단 + 개선 로드맵 보고서 | Relate, Typed, ProtoPie, QueryPie, Specter, Swing2App, 크리에이터링크 | ₩1–3M/건 |
| **구현 (Implementation)** | 오딧 후 실제 설정 변경, 도메인 인증 구성, ESP 세팅 지원 | flex, ProtoPie, Wrtn, Specter, Ringle, 비즈플레이, Typed | ₩3–8M/프로젝트 |
| **리테이너 (Retainer)** | 월간 모니터링: bounce rate, spam rate, DMARC 보고서 해석, 알럿 대응 | Channel Corp., MyRealTrip, Sendbird, Wrtn (글로벌 확장 후) | ₩1–2M/월 |
| **인박스 패널 (Inbox Panel)** | Naver/Kakao inbox placement 데이터 제공 (향후) | 전체 (차별화 핵심 자산, 장기 수익 모델) | TBD (데이터 구독) |

---

## 우선순위 접근 순서 (2026년 3–6월)

### 즉시 (3월): 콘텐츠 선행 + 소규모 warm target

1. **Relate** — 블로그 뉴스레터 구독 + LinkedIn 연결 → 오딧 패키지 첫 번째 유료 고객 목표
2. **Specter** — LinkedIn 직접 메일: "레퍼런스 체크 이메일이 Outlook에서 스팸으로 빠지면 어떻게 되나요?" pitch
3. **Typed** — Product Hunt 커뮤니티 댓글에서 관계 형성 → 오딧 제안

### 단기 (4–5월): 중간 규모 + 글로벌 확장 트리거

4. **ProtoPie** — Series B 직후 Austin 오피스 Gmail 문제 레퍼런스로 접근
5. **Ringle** — 영문 블로그 기고(deliverability for tutoring platforms) 후 inbound 유도
6. **Wrtn** — 미국 진출 6월 전 "Gmail 준비 완료 체크리스트" 콘텐츠로 접근

### 중기 (6–7월): 규모 있는 구현/리테이너 타겟

7. **Channel Corp.** — 스티비 파트너 네트워크 통해 warm intro 시도
8. **flex** — HRTECH 밋업 또는 LinkedIn: DMARC p=reject 시나리오 교육 콘텐츠 선행
9. **MyRealTrip** — 여행 플랫폼 이메일 deliverability 케이스스터디 작성 후 접근

---

## 스티비(Stibee) 파트너 경유 Warm Intro 전략

스티비는 한국 B2B SaaS 이메일 마케터들이 가장 많이 사용하는 국내 ESP다. 스티비와 파트너십을 맺거나 스티비 공식 에이전시/파트너로 등록되면:

- **Channel Corp., MyRealTrip, Wrtn, flex** 등이 스티비를 사용 중일 가능성 높음
- 스티비 고객 담당자가 "이메일이 스팸으로 가요"라는 고객 컴플레인을 받을 때 deliverability 전문가로 소개받을 수 있음
- 스티비 블로그/웨비나에 기고자(기여자)로 참여하면 스티비 고객사 전체에 노출 가능

**행동 지침:** 스티비 파트너 프로그램 또는 공식 블로그 기고 문의를 2026년 3월 중 진행.

---

## 핵심 포지셔닝 메시지 (cold outreach용)

```
안녕하세요, [이름]님.

[회사명]이 [미국/일본] 시장으로 확장하는 시점에 맞춰 연락드립니다.

한국 기업이 글로벌 확장 시 처음 직면하는 문제 중 하나가 이메일 도달률입니다.
Gmail과 Outlook은 DMARC 정책을 강화했고, 한국에서 발송하는 이메일이
미국 inbox에 들어가지 못하는 경우가 많습니다.

저는 한국어/영어 이중언어 이메일 deliverability 전문가로,
특히 Naver Mail의 필터링 로직과 글로벌 inbox placement에 특화되어 있습니다.

[회사명]의 온보딩/트랜잭션 이메일이 현재 어디로 가고 있는지
무료 진단 결과를 30분 안에 보내드릴 수 있습니다.
관심 있으시면 말씀해주세요.
```

---

## 주요 출처

- [Channel Corp. raising $30M extension (Axios, 2024)](https://www.axios.com/pro/retail-deals/2024/04/24/korean-startup-channel-corp-raising-30m-extension)
- [flex Series B-1 funding (WowTale, 2025)](https://en.wowtale.net/2025/06/12/231327/)
- [ProtoPie secures $21M Series B (ProtoPie Blog, 2025)](https://www.protopie.io/blog/protopie-secures-series-b-funding)
- [Wrtn targets US expansion and 2028 IPO (Yahoo Finance)](https://finance.yahoo.com/news/south-korea-ai-startup-wrtn-aims-to-enter-us-market-targets-ipo-as-early-as-2028-160556486.html)
- [MyRealTrip raises $56.7M Series F (TechCrunch, 2024)](https://techcrunch.com/2024/01/18/koreas-myrealtrip-cashes-in-on-travel-rebound-with-56m-in-new-funding/)
- [Specter $8.4M total funding (WowTale, 2024)](https://en.wowtale.net/2024/12/13/228496/)
- [YC-backed Relate: growth in 2024 (KED Global)](https://www.kedglobal.com/korean-startups/newsView/ked202408260015)
- [QueryPie $27.82M cumulative (PR Newswire, 2024)](https://www.prnewswire.com/news-releases/chequer-inc-querypie-secures-investment-to-accelerate-growth-302076995.html)
- [South Korea's SaaS Innovations at Japan IT Week 2024 (KoreaTechDesk)](https://www.koreatechdesk.com/south-koreas-saas-innovations-shine-at-japan-it-week-2024-strengthening-tech-ties-with-japan/)
- [Korean SaaS Titans $100M Revenue Silicon Valley showcase (KoreaTechDesk)](https://koreatechdesk.com/korean-saas-titans-with-100m-revenue-to-showcase-in-silicon-valley-exclusive-two-day-event-announced/)
