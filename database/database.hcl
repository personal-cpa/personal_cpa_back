schema "personal_cpa" {}

table "chart_of_accounts" {
  schema = schema.personal_cpa
  comment = "계정과목"

  column "id" {
    type = int
    null = false
    auto_increment = true

  }

  column "user_id" {
    type = int
    null = false
    comment = "사용자 ID"
  }

  column "code" {
    type = varchar(255)
    null = false
    comment = "계정과목 코드 (e.g. 자산 - 현금: 1-1, 자산 - 주식: 1-2, 부채 - 신용카드: 2-1, 부채 - 마이너스통장: 2-2, 자본 - 자기자본: 3-1, 수익 - 급여: 4-1, 비용 - 식비: 5-1)"
  }

  column "name" {
    type = varchar(255)
    null = false
    comment = "계정과목명 (e.g. 현금, 예금, 주식, 부동산, 차량, 선급금, 신용카드, 마이너스통장, 학자금대출, 전세보증금, 미지급세금, 자기자본, 자본금, 순이익 누계, 인출금, 유보이익)"
  }

  column "category" {
    type = int
    null = false
    comment = "계정과목 유형 (e.g. 1: ASSET, 2: LIABILITY, 3: EQUITY, 4: REVENUE, 5: EXPENSE)"
  }

  column "is_hidden" {
    type = bool
    null = false
    default = false
    comment = "계정과목 숨김 여부"
  }

  column "description" {
    type = text
    null = true
    comment = "계정과목 설명"
  }

  column "parent_chart_of_account_id" {
    type = int
    null = true
    comment = "상위 계정과목 ID"
  }

  column "created_at" {
    type = timestamp
    null = false
    default = sql("CURRENT_TIMESTAMP")
    comment = "생성 시간"
  }

  column "updated_at" {
    type = timestamp
    null = false
    default = sql("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    comment = "수정 시간"
  }

  primary_key {
    columns = [column.id]
  }

  index "user_id_code" {
    columns = [column.user_id, column.code]
    unique = true
  }
}