# content/ — 콘텐츠 마케팅 허브

이 폴더는 go-to-market용 한국어 콘텐츠 자산 전체를 관리합니다.
도구 배포 패키지에 포함되지 않습니다.

## 하위 폴더

| 폴더 | 설명 |
|------|------|
| [`drafts/`](drafts/) | 초안 완료된 기사, 커뮤니티 포스트, 가이드 |
| [`ideas/`](ideas/) | 초안 작성 전 아이디어 백로그 (`IDEAS.md`) |

---

## 채널 전략 (우선순위 순)

| 순위 | 채널 | 특성 | 월 방문자 | 의사결정권자 도달 확률 |
|------|------|------|-----------|----------------------|
| 1 | **GeekNews** (news.hada.io) | 링크 제출, 즉각 노출 | 500,000+ | ★★★★★ |
| 2 | **요즘IT** (yozm.wishket.com) | 편집 심사 기고, 뉴스레터 85K | 460,000 | ★★★★☆ |
| 3 | **콜드 이메일** (직접 발송) | 명단 타겟 개인 발송 | 30–50건 | ★★★★☆ |
| 4 | **OKKY** (okky.kr) | 개발자 Q&A 커뮤니티 | 170,000 회원 | ★★★★☆ |
| 5 | **네이버 블로그** | 장기 SEO, 검색 유입 | — | ★★★☆☆ |
| 6 | **티스토리** | Google SEO | — | ★★★☆☆ |

**제외 채널:** LinkedIn(직장인 밀도 낮음), Threads(라이프스타일 스큐), KakaoTalk 오픈채팅(단편화)

---

## 런치 순서

```
1. 요즘IT 기고 신청 (7일 응답 대기)
   ↓ 동시에
2. Article 1 네이버 블로그 발행
   ↓ 발행 직후
3. GeekNews 제출 (drafts/geeknews_submission.md)
   ↓ 첫 반응 확인 후
4. OKKY 커뮤니티 포스트 (drafts/okky_post.md)
   ↓ 병행
5. 콜드 이메일 30–50건 (cold_email_template.md)
   ↓
6. Articles 2–5 격주 발행
```

---

## 초안 완료 파일 목록 (`drafts/`)

| 순서 | 파일 | 제목 | 주 채널 | 상태 |
|------|------|------|---------|------|
| 1 | [`drafts/article1_세금계산서_스팸_7가지_이유.md`](drafts/article1_세금계산서_스팸_7가지_이유.md) | 세금계산서 이메일이 스팸함에 들어가는 진짜 이유 7가지 | 요즘IT + 네이버 블로그 | 초안 완료 |
| 2 | [`drafts/article2_네이버_메일_차단_기준.md`](drafts/article2_네이버_메일_차단_기준.md) | 네이버 메일이 우리 이메일을 차단하는 기준은? | 요즘IT 또는 네이버 블로그 | 초안 완료 |
| 3 | [`drafts/article3_KISA_RBL_블랙리스트.md`](drafts/article3_KISA_RBL_블랙리스트.md) | KISA 블랙리스트에 등록됐는지 모르는 이유 | 네이버 블로그 + 티스토리 | 초안 완료 |
| 4 | [`drafts/article4_DMARC_한국_1.8퍼센트.md`](drafts/article4_DMARC_한국_1.8퍼센트.md) | 한국 기업의 DMARC 설정률이 1.8%인 이유와 당장 해야 할 이유 | 요즘IT 스타일 | 초안 완료 |
| 5 | [`drafts/article5_도구_데모_실제_도메인_분석.md`](drafts/article5_도구_데모_실제_도메인_분석.md) | 이메일 발송률 진단 도구로 실제 도메인을 분석해봤습니다 | 전 채널 | 초안 완료 |
| — | [`drafts/geeknews_submission.md`](drafts/geeknews_submission.md) | GeekNews 링크 제출 | GeekNews | 초안 완료 |
| — | [`drafts/okky_post.md`](drafts/okky_post.md) | OKKY 커뮤니티 포스트 | OKKY | 초안 완료 |
| — | [`drafts/remediation_guide.md`](drafts/remediation_guide.md) | 이메일 인증 설정 가이드 | 기술 참고자료 | 초안 완료 |

---

## 채널별 투고 전 체크리스트

### 요즘IT
- [ ] being.oopy.io에서 기고 신청 완료
- [ ] Article 1을 샘플 피치로 첨부
- [ ] 편집자 피드백 반영 후 최종본 작성

### GeekNews
- [ ] GitHub 저장소 제출 (`drafts/geeknews_submission.md` 참조)
- [ ] 화요일 또는 수요일 오전 KST 제출 (피드 활성 시간)
- [ ] 기술 배경 댓글 선제 작성 (제출 후 즉시)

### OKKY
- [ ] `drafts/okky_post.md` 참조하여 자유게시판 또는 Q&A 게시
- [ ] 홍보성 언어 없이 문제/해결 구조로 작성
- [ ] 댓글 질문에 성실히 답변 (커뮤니티 신뢰 구축)

### 콜드 이메일
- [ ] 발송 전 해당 도메인 스캔 실행 (`uv run check.py targetdomain.co.kr`)
- [ ] 실제 스캔 결과를 이메일 본문에 포함
- [ ] `cold_email_template.md` 참조
- [ ] 1차 타겟: 바로빌, 이카운트, 더존비즈온 IT 담당자
- [ ] 발송량: 30–50건 (대량 발송 금지)

### 네이버 블로그
- [ ] 이미지 3–5장 포함 (Naver C-Rank 가중치)
- [ ] SPF/DKIM/DMARC 흐름 다이어그램 첨부
- [ ] 네이버 서치어드바이저에 블로그 등록

### 티스토리
- [ ] 구글 서치콘솔 연동
- [ ] Article 3 Google 키워드 최적화 확인

---

## KISA 공급기업 채널

유기적 콘텐츠 GTM과 별개로 운영되는 정부 지원 수요 채널.

| 항목 | 내용 |
|------|------|
| 채널 성격 | KISA ICT 중소기업 정보보호 지원사업 — 정부가 비용의 80% 보조 (SME당 최대 ₩4.4M) |
| 활성화 조건 | Phase 2 라이브 (클라우드 호스팅 + 스케줄러 + 이메일 알림) + 법인 등록 완료 (~2026년 4월) |
| 유기적 GTM과의 관계 | Phase 2 개발 기간 동안 유기적 채널과 병행 진행 — 충돌 없음 |
| 신청 카테고리 | 네트워크 위협탐지 및 대응 또는 스팸차단 (SECaaS) — "이메일 보안" 카테고리 사용 금지 |
| 일정 | 설명회 4월 중순 → 신청 마감 5월 28일 → 수요기업 공고 6월 20일 |

자세한 신청 절차 및 자격 요건은 `pricing_strategy_research.md` Part E 참조.

---

## CTA 표준 문구
```
무료 진단 도구로 직접 확인하세요 → https://github.com/pon00050/korean-email-deliverability
```
