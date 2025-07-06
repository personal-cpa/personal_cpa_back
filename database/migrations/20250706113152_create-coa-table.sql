-- Create "chart_of_account" table
CREATE TABLE `chart_of_account` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT "사용자 ID",
  `code` varchar(255) NOT NULL COMMENT "계정과목 코드 (e.g. 자산 - 현금: 1-1, 자산 - 주식: 1-2, 부채 - 신용카드: 2-1, 부채 - 마이너스통장: 2-2, 자본 - 자기자본: 3-1, 수익 - 급여: 4-1, 비용 - 식비: 5-1)",
  `name` varchar(255) NOT NULL COMMENT "계정과목명 (e.g. 현금, 예금, 주식, 부동산, 차량, 선급금, 신용카드, 마이너스통장, 학자금대출, 전세보증금, 미지급세금, 자기자본, 자본금, 순이익 누계, 인출금, 유보이익)",
  `category` int NOT NULL COMMENT "계정과목 유형 (e.g. 1: ASSET, 2: LIABILITY, 3: EQUITY, 4: REVENUE, 5: EXPENSE)",
  `is_hidden` bool NOT NULL DEFAULT 0 COMMENT "계정과목 숨김 여부",
  `description` text NULL COMMENT "계정과목 설명",
  `parent_chart_of_account_id` int NULL COMMENT "상위 계정과목 ID",
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "생성 시간",
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "수정 시간",
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id_code` (`user_id`, `code`)
) CHARSET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT "계정과목";
